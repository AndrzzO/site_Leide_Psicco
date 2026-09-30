"""
Testes automatizados de SEO Editorial e On-Page (Prompt 13).
Valida hierarquia semântica de headings (1 H1 por página), títulos padronizados,
meta descrições, integridade de links internos (zero 404), zero páginas órfãs,
isolamento de rascunhos do blog e presença de atributo alt em imagens.
"""
from django.test import TestCase, Client
from django.utils import timezone
from html.parser import HTMLParser
import re

from nucleo.models import ConfiguracaoSite, Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import CategoriaArtigo, Artigo


class SEOParser(HTMLParser):
    """Parser auxiliar para extrair elementos semânticos do HTML."""
    def __init__(self):
        super().__init__()
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.headings_order = []
        self.title = []
        self.meta_description = None
        self.meta_robots = None
        self.links = []
        self.images = []
        self.current_tag = None
        self.text_buf = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']:
            self.current_tag = tag
            self.text_buf = []
            self.headings_order.append(tag)
        elif tag == 'meta':
            if attrs_dict.get('name') == 'description':
                self.meta_description = attrs_dict.get('content', '')
            elif attrs_dict.get('name') == 'robots':
                self.meta_robots = attrs_dict.get('content', '')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            if href:
                self.links.append((href, attrs_dict.get('aria-label', '')))
        elif tag == 'img':
            self.images.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt'),
                'has_alt': 'alt' in attrs_dict
            })

    def handle_endtag(self, tag):
        if tag == self.current_tag:
            text = ' '.join(''.join(self.text_buf).split())
            if tag == 'h1':
                self.h1.append(text)
            elif tag == 'h2':
                self.h2.append(text)
            elif tag == 'h3':
                self.h3.append(text)
            elif tag == 'title':
                self.title.append(text)
            self.current_tag = None
            self.text_buf = []

    def handle_data(self, data):
        if self.current_tag:
            self.text_buf.append(data)


class SEOEditorialTestCase(TestCase):
    """Suíte de testes de validação editorial e on-page."""

    @classmethod
    def setUpTestData(cls):
        # Configuração Singleton
        cls.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            slogan_principal="COMPREENDER • CUIDAR • RECONSTRUIR",
            whatsapp="5561999999999",
            email="contato@institutomenteemfoco.com.br",
            endereco_texto="Brasília - DF",
            modalidade_atendimento="Presencial e Online"
        )
        # Profissional ativa
        cls.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Psicóloga Mari Menezes",
            titulo_profissional="Psicóloga Clínica",
            ativo=True
        )
        # Categoria e Artigo publicado para testes
        cls.categoria = CategoriaArtigo.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            ativo=True,
            ordem=1
        )
        cls.artigo_pub = Artigo.objects.create(
            titulo="Quando Procurar Ajuda Psicológica",
            slug="quando-procurar-ajuda-psicologica",
            resumo="Um guia acolhedor para identificar o momento certo de iniciar terapia.",
            conteudo="A psicoterapia é um espaço seguro de cuidado.",
            status="publicado",
            categoria=cls.categoria,
            data_publicacao=timezone.now() - timezone.timedelta(days=1),
            meta_titulo="Quando Procurar Ajuda Psicológica | Instituto Mente em Foco",
            meta_descricao="Saiba quando iniciar acompanhamento psicológico com acolhimento profissional."
        )
        # Artigo em rascunho para testar isolamento
        cls.artigo_draft = Artigo.objects.create(
            titulo="Artigo Privado em Rascunho",
            slug="artigo-privado-rascunho",
            resumo="Rascunho não deve ser indexado.",
            conteudo="Texto não publicado.",
            status="rascunho",
            categoria=cls.categoria
        )

        cls.urls_publicas = [
            '/credenciamento/',
            *['/servicos/avaliacao/' + slug + '/' for slug in ['burnout', 'cirurgia-bariatrica', 'esterilizacao', 'inss', 'processos-judiciais', 'ansiedade-depressao']],
            '/',
            '/sobre-mim/',
            '/servicos/psicologia/',
            '/servicos/neuropsicologia/',
            '/servicos/traumas/',
            '/servicos/separacao-e-recomecos/',
            '/servicos/novos-relacionamentos/',
            '/servicos/avaliacao/',
            '/servicos/avaliacao-psicologica/',
            '/servicos/avaliacao-neuropsicologica/',
            '/servicos/reabilitacao-neurocognitiva/',
            '/conteudos/',
            f'/conteudos/categoria/{cls.categoria.slug}/',
            f'/conteudos/{cls.artigo_pub.slug}/',
            '/contato/',
            '/politica-de-privacidade/',
            '/politica-de-cookies/',
        ]

    def setUp(self):
        self.client = Client()

    def test_todas_as_paginas_publicas_retornam_status_200(self):
        """Valida que todas as URLs públicas retornam 200 OK."""
        for url in self.urls_publicas:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"URL {url} retornou {res.status_code}")

    def test_todas_as_paginas_tem_exatamente_um_h1(self):
        """Regra estrita: cada página deve ter exatamente 1 única tag H1 em tempo de execução."""
        for url in self.urls_publicas:
            res = self.client.get(url)
            parser = SEOParser()
            parser.feed(res.content.decode('utf-8'))
            self.assertEqual(
                len(parser.h1), 1,
                f"Página {url} deve ter exatamente 1 tag H1, mas possui {len(parser.h1)}: {parser.h1}"
            )
            self.assertTrue(len(parser.h1[0]) > 3, f"H1 da página {url} não deve ser vazio.")

    def test_todas_as_paginas_tem_title_e_meta_description_validos(self):
        """Valida que o title está padronizado e a meta description tem tamanho aceitável."""
        for url in self.urls_publicas:
            res = self.client.get(url)
            parser = SEOParser()
            parser.feed(res.content.decode('utf-8'))
            
            # Title
            self.assertTrue(len(parser.title) >= 1, f"Página {url} não possui tag <title>.")
            title = parser.title[0]
            self.assertIn(
                "Instituto Mente em Foco", title,
                f"Title da página {url} deve conter a marca 'Instituto Mente em Foco': '{title}'"
            )
            self.assertTrue(30 <= len(title) <= 90, f"Title de {url} tem tamanho incomum: {len(title)} chars.")

            # Meta Description
            self.assertIsNotNone(parser.meta_description, f"Página {url} não possui <meta name='description'>.")
            desc = parser.meta_description
            self.assertTrue(
                40 <= len(desc) <= 250,
                f"Meta description da página {url} tem tamanho fora da faixa recomendada ({len(desc)} chars): '{desc}'"
            )

    def test_integridade_dos_links_internos(self):
        """Extrai todos os links internos de todas as páginas e valida status HTTP 200."""
        links_testados = set()
        for url in self.urls_publicas:
            res = self.client.get(url)
            parser = SEOParser()
            parser.feed(res.content.decode('utf-8'))
            
            for href, aria in parser.links:
                clean_href = href.split('?')[0].split('#')[0]
                # Testa links internos que não sejam admin, media, estáticos ou externos
                if clean_href.startswith('/') and not clean_href.startswith(('/admin', '/media', '/static', '/health', '/design-system')):
                    if clean_href not in links_testados:
                        links_testados.add(clean_href)
                        link_res = self.client.get(clean_href)
                        self.assertEqual(
                            link_res.status_code, 200,
                            f"Link interno quebrado encontrado em {url}: '{clean_href}' retornou {link_res.status_code}"
                        )

    def test_zero_paginas_orfas(self):
        """Valida que todas as páginas públicas recebem pelo menos 1 link de entrada."""
        inbound_count = {url: 0 for url in self.urls_publicas}
        
        for url in self.urls_publicas:
            res = self.client.get(url)
            parser = SEOParser()
            parser.feed(res.content.decode('utf-8'))
            
            destinos_unicos = set(href.split('?')[0].split('#')[0] for href, aria in parser.links)
            for dest in destinos_unicos:
                if dest in inbound_count:
                    inbound_count[dest] += 1
                    
        for url, count in inbound_count.items():
            self.assertGreater(
                count, 0,
                f"Página órfã detectada! {url} não possui nenhum link interno apontando para si."
            )

    def test_artigos_em_rascunho_sao_completamente_invisiveis(self):
        """Assegura que artigos em rascunho não são linkados e retornam 404 para público geral."""
        # 1. Não aparece na listagem do blog
        res_blog = self.client.get('/conteudos/')
        self.assertNotContains(res_blog, self.artigo_draft.slug)
        self.assertNotContains(res_blog, self.artigo_draft.titulo)

        # 2. Acesso anônimo direto à URL do rascunho retorna 404
        res_detalhe = self.client.get(f'/conteudos/{self.artigo_draft.slug}/')
        self.assertEqual(res_detalhe.status_code, 404)

    def test_imagens_possuem_atributo_alt(self):
        """Valida que nenhuma tag <img> é renderizada sem o atributo alt nas páginas públicas."""
        for url in self.urls_publicas:
            res = self.client.get(url)
            parser = SEOParser()
            parser.feed(res.content.decode('utf-8'))
            
            for img in parser.images:
                self.assertTrue(
                    img['has_alt'],
                    f"Imagem na página {url} com src '{img['src']}' não possui o atributo 'alt'."
                )
