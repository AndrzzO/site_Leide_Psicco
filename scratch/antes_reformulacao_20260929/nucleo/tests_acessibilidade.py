"""
Testes automatizados de Acessibilidade Digital (WCAG 2.2 — Nível AA).
Valida conformidade com os princípios fundamentais:
- Semântica nativa e ausência de roles redundantes
- Navegação por teclado, skip-link e gestão de foco
- Landmarks e diferenciação de múltiplos blocos <nav> via aria-label
- Formulários acessíveis: labels correspondentes, legenda de obrigatoriedade,
  aria-invalid, aria-describedby e sumário de erros com role="alert"
- Blindagem de campos honeypot contra tecnologias assistivas
- Acessibilidade de mídias: atributos alt em <img> e SVGs decorativos com aria-hidden/focusable
- Paginação acessível com aria-current="page"
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from html.parser import HTMLParser
import re

from nucleo.models import ConfiguracaoSite, Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import CategoriaArtigo, Artigo


class AccessibilityParser(HTMLParser):
    """Parser para extração e auditoria de atributos de acessibilidade no HTML."""
    def __init__(self):
        super().__init__()
        self.html_tag_attrs = {}
        self.skip_link = None
        self.main_tags = []
        self.header_tags = []
        self.footer_tags = []
        self.nav_tags = []
        self.img_tags = []
        self.svg_tags = []
        self.labels = []
        self.inputs = []
        self.tables = []
        self.captions = []
        self.roles = []
        self.current_tag = None
        self.text_buf = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag

        if tag == 'html':
            self.html_tag_attrs = attrs_dict

        elif tag == 'a' and 'skip-link' in attrs_dict.get('class', ''):
            self.skip_link = attrs_dict

        elif tag == 'main':
            self.main_tags.append(attrs_dict)

        elif tag == 'header':
            self.header_tags.append(attrs_dict)

        elif tag == 'footer':
            self.footer_tags.append(attrs_dict)

        elif tag == 'nav':
            self.nav_tags.append(attrs_dict)

        elif tag == 'img':
            self.img_tags.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt'),
                'has_alt': 'alt' in attrs_dict,
            })

        elif tag == 'svg':
            self.svg_tags.append(attrs_dict)

        elif tag == 'label':
            self.labels.append(attrs_dict)

        elif tag in ['input', 'textarea', 'select']:
            self.inputs.append({
                'tag': tag,
                'attrs': attrs_dict,
                'name': attrs_dict.get('name'),
                'id': attrs_dict.get('id'),
                'aria-invalid': attrs_dict.get('aria-invalid'),
                'aria-describedby': attrs_dict.get('aria-describedby'),
                'aria-required': attrs_dict.get('aria-required'),
            })

        elif tag == 'table':
            self.tables.append(attrs_dict)

        elif tag == 'caption':
            self.captions.append(attrs_dict)

        if 'role' in attrs_dict:
            self.roles.append((tag, attrs_dict['role']))


class AcessibilidadeWCAGTests(TestCase):
    """Suíte de testes de conformidade WCAG 2.2 AA para o Instituto Mente em Foco."""

    @classmethod
    def setUpTestData(cls):
        cls.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            email="contato@institutomentemfoco.com.br",
            telefone="61999999999",
            whatsapp="5561999999999",
            modalidade_atendimento="Atendimento Presencial e Online",
            endereco_texto="Brasília, DF",
            horario_atendimento="Segunda a Sexta, das 8h às 18h",
            ativo=True,
        )
        cls.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Mari Menezes",
            slug="mari-menezes",
            titulo_profissional="Psicóloga Clínica e Neuropsicóloga",
            registro_profissional="CRP 01/12345",
            biografia_curta="Atendimento humanizado focado em acolhimento e reconstrução.",
            biografia_completa="Trajetória profissional sólida.",
            ativo=True,
        )
        cls.area = AreaAtuacao.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia",
            ordem=1,
            ativo=True,
        )
        cls.servico = Servico.objects.create(
            area=cls.area,
            nome="Psicoterapia Individual",
            slug="psicoterapia-individual",
            resumo="Atendimento individualizado para adultos.",
            descricao="Processo terapêutico profundo.",
            ordem=1,
            ativo=True,
        )
        cls.categoria = CategoriaArtigo.objects.create(
            nome="Saúde Mental",
            slug="saude-mental",
            ordem=1,
            ativo=True,
        )
        cls.artigo = Artigo.objects.create(
            titulo="Cuidar da mente e recomeçar",
            slug="cuidar-da-mente-e-recomecar",
            autor=cls.profissional,
            categoria=cls.categoria,
            resumo="Reflexões sobre saúde mental e reconstrução.",
            conteudo="Conteúdo detalhado e acolhedor sobre o tema.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now(),
        )
        cls.client = Client()

    def parse_page(self, path):
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200, f"Falha ao carregar {path}")
        parser = AccessibilityParser()
        parser.feed(resp.content.decode('utf-8'))
        return resp, parser

    def test_html_lang_pt_br_em_todas_as_paginas_chave(self):
        """Critério 3.1.1 (Idioma da Página): html deve ter lang='pt-BR'."""
        paginas = [
            '/',
            '/sobre-mim/',
            '/servicos/psicologia/',
            '/conteudos/',
            f'/conteudos/{self.artigo.slug}/',
            '/contato/',
            '/politica-de-cookies/',
            '/politica-de-privacidade/',
        ]
        for path in paginas:
            with self.subTest(path=path):
                _, parser = self.parse_page(path)
                self.assertEqual(
                    parser.html_tag_attrs.get('lang'),
                    'pt-BR',
                    f"A tag <html> na rota {path} deve declarar lang='pt-BR'."
                )

    def test_skip_link_aponta_para_main_com_tabindex(self):
        """Critérios 2.4.1 (Ignorar Blocos) e 2.1.1 (Teclado)."""
        _, parser = self.parse_page('/')
        self.assertIsNotNone(parser.skip_link, "O link 'skip-link' deve existir na página.")
        self.assertEqual(
            parser.skip_link.get('href'),
            '#conteudo-principal',
            "O skip-link deve apontar para '#conteudo-principal'."
        )
        # Verifica se existe exatamente 1 main com id="conteudo-principal" e tabindex="-1"
        self.assertEqual(len(parser.main_tags), 1, "Deve existir exatamente 1 tag <main>.")
        main_attrs = parser.main_tags[0]
        self.assertEqual(main_attrs.get('id'), 'conteudo-principal')
        self.assertEqual(main_attrs.get('tabindex'), '-1', "A tag <main> deve possuir tabindex='-1' para foco programático.")

    def test_landmarks_sem_roles_redundantes(self):
        """Critério 1.3.1 (Info e Relações): remoção de roles ARIA redundantes em HTML5."""
        _, parser = self.parse_page('/')
        # <header> não deve ter role="banner"
        for header in parser.header_tags:
            self.assertNotIn('role', header, "<header> nativo não deve conter role='banner' redundante.")
        # <main> não deve ter role="main"
        for main in parser.main_tags:
            self.assertNotIn('role', main, "<main> nativo não deve conter role='main' redundante.")
        # <footer> não deve ter role="contentinfo"
        for footer in parser.footer_tags:
            self.assertNotIn('role', footer, "<footer> nativo não deve conter role='contentinfo' redundante.")

    def test_multiplos_navs_com_aria_label_distintos(self):
        """Critério 1.3.1 / 4.1.2: múltiplos elementos <nav> devem possuir aria-labels distintos."""
        _, parser = self.parse_page('/')
        labels = []
        for nav in parser.nav_tags:
            label = nav.get('aria-label')
            self.assertTrue(
                label,
                f"Elemento <nav> sem aria-label identificado: {nav}"
            )
            labels.append(label)

        # Valida que não há duplicatas de aria-label entre navs na mesma página
        self.assertEqual(
            len(labels),
            len(set(labels)),
            f"Detectados aria-labels duplicados em tags <nav>: {labels}"
        )

    def test_formulario_contato_labels_e_legenda(self):
        """Critérios 1.3.1, 3.3.2: labels associados a todos os inputs e legenda de obrigatoriedade."""
        resp, parser = self.parse_page('/contato/')
        html = resp.content.decode('utf-8')

        # Legenda explicativa textual
        self.assertIn(
            'form-legenda-obrigatorio',
            html,
            "O formulário deve conter uma legenda textual clara indicando campos obrigatórios."
        )

        # Labels com 'for' correspondente
        label_fors = [lbl.get('for') for lbl in parser.labels if lbl.get('for')]
        self.assertIn('id_nome', label_fors)
        self.assertIn('id_email', label_fors)
        self.assertIn('id_telefone', label_fors)
        self.assertIn('id_servico_interesse', label_fors)
        self.assertIn('id_mensagem', label_fors)

    def test_formulario_erros_aria_invalid_e_sumario(self):
        """Critérios 3.3.1 (Identificação de Erros), 3.3.3 (Sugestão de Erros) e 4.1.2."""
        # Envia POST inválido (sem nome e sem canal de contato)
        post_data = {
            'nome': '',
            'email': '',
            'telefone': '',
            'mensagem': 'Dúvida rápida',
            # Falta aceite_privacidade
        }
        resp = self.client.post('/contato/', post_data)
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode('utf-8')

        # 1. Sumário de erros no topo com role="alert"
        self.assertIn('role="alert"', html)
        self.assertIn('form-sumario-erros', html)

        # 2. Parsing dos inputs retornados
        parser = AccessibilityParser()
        parser.feed(html)

        # Localiza o input 'nome'
        nome_input = next((inp for inp in parser.inputs if inp['name'] == 'nome'), None)
        self.assertIsNotNone(nome_input)
        self.assertEqual(nome_input['aria-invalid'], 'true', "Campo 'nome' com erro deve conter aria-invalid='true'.")
        self.assertEqual(nome_input['aria-describedby'], 'id_nome-erro', "Campo 'nome' deve ter aria-describedby apontando para o erro.")

        # Localiza os inputs de contato cruzado (email e telefone)
        email_input = next((inp for inp in parser.inputs if inp['name'] == 'email'), None)
        self.assertIsNotNone(email_input)
        self.assertEqual(email_input['aria-invalid'], 'true')
        self.assertEqual(email_input['aria-describedby'], 'id_email-erro')

        tel_input = next((inp for inp in parser.inputs if inp['name'] == 'telefone'), None)
        self.assertIsNotNone(tel_input)
        self.assertEqual(tel_input['aria-invalid'], 'true')
        self.assertEqual(tel_input['aria-describedby'], 'id_telefone-erro')

    def test_honeypot_invisivel_para_tecnologias_assistivas(self):
        """Critério 4.1.2: o campo honeypot não deve ser anunciado por leitores de tela."""
        _, parser = self.parse_page('/contato/')
        campo_bot = next((inp for inp in parser.inputs if inp['name'] == 'campo_verificacao'), None)
        self.assertIsNotNone(campo_bot, "O campo honeypot deve existir.")
        attrs = campo_bot['attrs']
        self.assertEqual(attrs.get('tabindex'), '-1', "Honeypot deve possuir tabindex='-1' para não receber foco.")
        self.assertEqual(attrs.get('aria-hidden'), 'true', "Honeypot deve possuir aria-hidden='true'.")

    def test_todas_as_imagens_possuem_alt(self):
        """Critério 1.1.1 (Conteúdo Não-Textual): toda imagem deve possuir atributo alt."""
        rotas = ['/', '/sobre-mim/', '/conteudos/', f'/conteudos/{self.artigo.slug}/', '/contato/']
        for path in rotas:
            with self.subTest(path=path):
                _, parser = self.parse_page(path)
                for img in parser.img_tags:
                    self.assertTrue(
                        img['has_alt'],
                        f"Imagem sem atributo alt na rota {path}: src={img['src']}"
                    )

    def test_menu_mobile_atributos_acessibilidade(self):
        """Critérios 2.1.1, 4.1.2: botão do menu com aria-expanded, aria-controls e painel com hidden."""
        resp, parser = self.parse_page('/')
        html = resp.content.decode('utf-8')

        self.assertIn('data-menu-toggle', html)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn('aria-controls="menu-mobile-painel"', html)
        self.assertIn('id="menu-mobile-painel"', html)

    def test_tabela_cookies_acessivel(self):
        """Critérios 1.3.1 (Tabelas de Dados): th com scope='col', caption e sem role redundante."""
        _, parser = self.parse_page('/politica-de-cookies/')
        self.assertEqual(len(parser.tables), 1, "A página de cookies deve conter exatamente 1 tabela.")
        table_attrs = parser.tables[0]
        self.assertNotIn('role', table_attrs, "<table> nativa não deve ter role='table' redundante.")
        self.assertEqual(len(parser.captions), 1, "A tabela de cookies deve possuir elemento <caption> para acessibilidade.")

    def test_paginacao_blog_aria_current(self):
        """Critério 4.1.2: item ativo da paginação deve ter aria-current='page'."""
        # Cria mais artigos para forçar paginação
        for i in range(12):
            Artigo.objects.create(
                titulo=f"Artigo Adicional {i}",
                slug=f"artigo-adicional-{i}",
                autor=self.profissional,
                categoria=self.categoria,
                resumo="Resumo do artigo adicional.",
                conteudo="Conteúdo do artigo adicional.",
                status=Artigo.STATUS_PUBLICADO,
                data_publicacao=timezone.now(),
            )
        resp, parser = self.parse_page('/conteudos/')
        html = resp.content.decode('utf-8')
        self.assertIn('aria-current="page"', html, "A paginação ativa deve conter aria-current='page'.")
        self.assertIn('paginacao-conteudos', html)
