"""
Testes automatizados completos do app conteudos (Blog / Conteúdos Educativos).
Cobre modelos, QuerySet de publicação, sanitização anti-XSS, views (index, busca,
categorias, detalhe, rascunho 404), paginação, admin e integração com a Home.
"""
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from nucleo.models import Profissional
from servicos.models import Servico, AreaAtuacao
from conteudos.models import CategoriaArtigo, Artigo
from conteudos.sanitizacao import renderizar_markdown_seguro

User = get_user_model()


class SanitizacaoMarkdownTest(TestCase):
    """Testes de segurança anti-XSS e sanitização de Markdown."""

    def test_markdown_basico_formatado_com_sucesso(self):
        md = "## Subtítulo do Artigo\n\nEste é um parágrafo com **negrito** e *itálico*."
        html = renderizar_markdown_seguro(md)
        self.assertIn("<h2>Subtítulo do Artigo</h2>", html)
        self.assertIn("<p>Este é um parágrafo com <strong>negrito</strong> e <em>itálico</em>.</p>", html)

    def test_bloqueio_estrito_de_tags_script_e_eventos_on(self):
        md_malicioso = (
            "<script>alert('xss');</script>\n"
            "<img src='x' onerror='alert(1)'>\n"
            "<a href='javascript:alert(2)'>Clique aqui</a>"
        )
        html = renderizar_markdown_seguro(md_malicioso)
        self.assertNotIn("<script>", html)
        self.assertNotIn("</script>", html)
        self.assertNotIn("onerror", html)
        self.assertNotIn("javascript:", html)
        self.assertNotIn("<img", html)

    def test_bloqueio_de_h1_no_corpo_para_proteger_hierarquia_seo(self):
        md = "# Título Indevido no Corpo\n\n## Subtítulo Correto"
        html = renderizar_markdown_seguro(md)
        self.assertNotIn("<h1>", html)
        self.assertIn("<h2>Subtítulo Correto</h2>", html)

    def test_conteudo_vazio_ou_nulo(self):
        self.assertEqual(renderizar_markdown_seguro(""), "")
        self.assertEqual(renderizar_markdown_seguro(None), "")


class CategoriaArtigoModelTest(TestCase):
    """Testes do modelo CategoriaArtigo."""

    def test_criacao_e_slug_automatico(self):
        cat = CategoriaArtigo.objects.create(
            nome="Psicologia Clínica e Saúde",
            descricao="Artigos sobre psicoterapia."
        )
        self.assertEqual(cat.slug, "psicologia-clinica-e-saude")
        self.assertEqual(str(cat), "Psicologia Clínica e Saúde")

    def test_slug_unico_em_nomes_duplicados(self):
        cat1 = CategoriaArtigo.objects.create(nome="Relacionamentos")
        cat2 = CategoriaArtigo.objects.create(nome="Relacionamentos")
        self.assertEqual(cat1.slug, "relacionamentos")
        self.assertEqual(cat2.slug, "relacionamentos-1")


class ArtigoModelTest(TestCase):
    """Testes do modelo Artigo e ciclo de vida editorial."""

    def setUp(self):
        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Psicóloga Mari Menezes",
            slug="mari-menezes-teste"
        )
        self.categoria = CategoriaArtigo.objects.create(
            nome="Psicologia",
            slug="psicologia-teste"
        )

    def test_criacao_padrao_como_rascunho(self):
        artigo = Artigo.objects.create(
            titulo="Artigo Inicial de Teste",
            autor=self.profissional,
            categoria=self.categoria
        )
        self.assertEqual(artigo.status, Artigo.STATUS_RASCUNHO)
        self.assertIsNone(artigo.data_publicacao)
        self.assertEqual(artigo.slug, "artigo-inicial-de-teste")

    def test_preenchimento_automatico_de_data_ao_publicar(self):
        artigo = Artigo.objects.create(
            titulo="Artigo Publicado Imediato",
            status=Artigo.STATUS_PUBLICADO,
            autor=self.profissional
        )
        self.assertIsNotNone(artigo.data_publicacao)
        self.assertLessEqual(artigo.data_publicacao, timezone.now())

    def test_calculo_tempo_de_leitura(self):
        texto_longo = "palavra " * 450  # 450 palavras / 200 = ~2.25 -> 3 minutos
        artigo = Artigo.objects.create(
            titulo="Artigo Leitura",
            conteudo=texto_longo,
            status=Artigo.STATUS_PUBLICADO
        )
        self.assertEqual(artigo.tempo_leitura_minutos, 3)

    def test_queryset_publicados_regras_estritas(self):
        agora = timezone.now()

        # 1. Artigo publicado e ativo (DEVE aparecer)
        art1 = Artigo.objects.create(
            titulo="Artigo Válido",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(days=1),
            categoria=self.categoria
        )

        # 2. Artigo rascunho (NÃO deve aparecer)
        Artigo.objects.create(
            titulo="Rascunho",
            status=Artigo.STATUS_RASCUNHO,
            data_publicacao=agora - timedelta(days=1),
            categoria=self.categoria
        )

        # 3. Artigo publicado com data no futuro / agendado (NÃO deve aparecer)
        Artigo.objects.create(
            titulo="Agendado Futuro",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora + timedelta(days=2),
            categoria=self.categoria
        )

        # 4. Artigo publicado em categoria inativa (NÃO deve aparecer)
        cat_inativa = CategoriaArtigo.objects.create(nome="Inativa", ativo=False)
        Artigo.objects.create(
            titulo="Em Categoria Inativa",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(days=1),
            categoria=cat_inativa
        )

        publicados = Artigo.objects.publicados()
        self.assertEqual(publicados.count(), 1)
        self.assertEqual(publicados.first(), art1)


class ConteudosViewsTest(TestCase):
    """Testes de rotas, listagem, filtros, busca, detalhe e segurança do app conteudos."""

    def setUp(self):
        self.client = Client()
        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Psicóloga Mari Menezes",
            slug="mari-menezes-view"
        )
        self.area = AreaAtuacao.objects.create(
            nome="Psicologia",
            slug="psicologia-area",
            ordem=1
        )
        self.servico = Servico.objects.create(
            nome="Psicoterapia",
            slug="psicoterapia",
            area=self.area,
            ordem=1
        )
        self.cat1 = CategoriaArtigo.objects.create(nome="Psicologia Clínica", slug="psicologia-clinica", ordem=1)
        self.cat2 = CategoriaArtigo.objects.create(nome="Neuropsicologia", slug="neuropsicologia", ordem=2)

    def test_listagem_vazia_exibe_estado_neutro_elegante_sem_erro(self):
        # Nenhum artigo publicado (apenas rascunhos podem existir)
        Artigo.objects.create(
            titulo="Tópico Rascunho",
            status=Artigo.STATUS_RASCUNHO,
            categoria=self.cat1
        )

        url = reverse('conteudos:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conteudos/index.html')
        self.assertContains(response, "Em breve novos conteúdos educativos serão publicados aqui")
        self.assertNotContains(response, "Tópico Rascunho")

    def test_listagem_com_artigos_publicados_e_destaque(self):
        agora = timezone.now()
        destaque = Artigo.objects.create(
            titulo="Artigo Principal em Destaque",
            resumo="Resumo do artigo em destaque.",
            conteudo="## Conteúdo Destaque\n\nTexto do destaque.",
            status=Artigo.STATUS_PUBLICADO,
            destaque=True,
            data_publicacao=agora - timedelta(hours=2),
            categoria=self.cat1
        )
        comum = Artigo.objects.create(
            titulo="Artigo Secundário Comum",
            resumo="Resumo do artigo comum.",
            conteudo="## Conteúdo Comum\n\nTexto comum.",
            status=Artigo.STATUS_PUBLICADO,
            destaque=False,
            data_publicacao=agora - timedelta(hours=1),
            categoria=self.cat2
        )

        response = self.client.get(reverse('conteudos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Artigo Principal em Destaque")
        self.assertContains(response, "Artigo Secundário Comum")
        self.assertEqual(response.context['artigo_destaque'], destaque)

    def test_busca_por_palavra_chave(self):
        agora = timezone.now()
        Artigo.objects.create(
            titulo="Compreendendo a Ansiedade e o Estresse",
            resumo="Como lidar com sobrecargas emocionais.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(hours=1),
            categoria=self.cat1
        )
        Artigo.objects.create(
            titulo="Memória e Funções Executivas",
            resumo="Avaliação cognitiva detalhada.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(hours=1),
            categoria=self.cat2
        )

        url = f"{reverse('conteudos:index')}?q=Ansiedade"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compreendendo a Ansiedade")
        self.assertNotContains(response, "Memória e Funções Executivas")

    def test_filtro_por_categoria(self):
        agora = timezone.now()
        Artigo.objects.create(
            titulo="Artigo de Psicologia",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(hours=1),
            categoria=self.cat1
        )
        Artigo.objects.create(
            titulo="Artigo de Neuropsicologia",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(hours=1),
            categoria=self.cat2
        )

        url = reverse('conteudos:categoria', kwargs={'categoria_slug': self.cat1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Artigo de Psicologia")
        self.assertNotContains(response, "Artigo de Neuropsicologia")

    def test_detalhe_artigo_publicado_retorna_200_com_dados_completos(self):
        agora = timezone.now()
        artigo = Artigo.objects.create(
            titulo="Guia Completo da Primeira Consulta",
            resumo="O que você precisa saber sobre o primeiro encontro.",
            conteudo="## O Primeiro Encontro\n\nNeste espaço de escuta sigilosa, acolhemos sua história.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=agora - timedelta(days=2),
            categoria=self.cat1,
            autor=self.profissional,
            servico_relacionado=self.servico
        )

        url = reverse('conteudos:detalhe', kwargs={'slug': artigo.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conteudos/detalhe.html')
        self.assertContains(response, "Guia Completo da Primeira Consulta")
        self.assertContains(response, "O Primeiro Encontro")
        self.assertContains(response, "Mari Menezes")
        self.assertContains(response, "Psicoterapia")

    def test_detalhe_artigo_rascunho_retorna_404(self):
        rascunho = Artigo.objects.create(
            titulo="Artigo Rascunho Confidencial",
            status=Artigo.STATUS_RASCUNHO,
            categoria=self.cat1
        )
        url = reverse('conteudos:detalhe', kwargs={'slug': rascunho.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detalhe_artigo_agendado_futuro_retorna_404(self):
        futuro = Artigo.objects.create(
            titulo="Artigo no Futuro",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + timedelta(days=5),
            categoria=self.cat1
        )
        url = reverse('conteudos:detalhe', kwargs={'slug': futuro.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ConteudosAdminTest(TestCase):
    """Testes de integração do Django Admin para CategoriaArtigo e Artigo."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_conteudos',
            email='admin@mentefoco.com.br',
            password='SenhaForteAdmin123!'
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_acesso_admin_categorias_e_artigos(self):
        url_cat = reverse('admin:conteudos_categoriaartigo_changelist')
        resp_cat = self.client.get(url_cat)
        self.assertEqual(resp_cat.status_code, 200)

        url_art = reverse('admin:conteudos_artigo_changelist')
        resp_art = self.client.get(url_art)
        self.assertEqual(resp_art.status_code, 200)


class HomeIntegracaoConteudosTest(TestCase):
    """Testes de integração da Home com o módulo de Conteúdos."""

    def setUp(self):
        self.client = Client()

    def test_home_renderiza_com_ou_sem_artigos_publicados(self):
        # Sem artigos publicados: deve exibir a prévia estática institucional sem quebrar
        resp_sem = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(resp_sem.status_code, 200)
        self.assertContains(resp_sem, "Informação que ajuda")

        # Com artigos publicados: deve renderizar artigos reais
        cat = CategoriaArtigo.objects.create(nome="Saúde Mental")
        Artigo.objects.create(
            titulo="Artigo Real da Home",
            resumo="Breve resumo para teste de integração da home.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - timedelta(hours=1),
            categoria=cat
        )

        resp_com = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(resp_com.status_code, 200)
        self.assertContains(resp_com, "Artigo Real da Home")
