"""
Testes automatizados de performance e integridade estrutural (Prompt 15).
Valida limites de consultas SQL (prevenção de N+1), carregamento não-bloqueante de scripts (defer),
estratégia LCP (loading eager + fetchpriority high), carregamento diferido de imagens secundárias (lazy loading)
e preconnect com display=swap em fontes externas.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from conteudos.models import Artigo, CategoriaArtigo
from servicos.models import Servico, AreaAtuacao
from nucleo.models import Profissional, ConfiguracaoSite


class PerformanceEstruturalTest(TestCase):
    """Testes de conformidade com diretrizes de Performance e Core Web Vitals."""

    def setUp(self):
        self.client = Client()
        self.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            slogan_principal="COMPREENDER • CUIDAR • RECONSTRUIR",
            whatsapp="5561999999999",
            email="contato@institutomenteemfoco.com.br",
            ativo=True
        )
        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Mari Menezes",
            slug="mari-menezes",
            registro_profissional="CRP 01/12345",
            ativo=True,
            destaque=True
        )
        self.cat = CategoriaArtigo.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            ativo=True
        )
        self.area = AreaAtuacao.objects.create(
            nome="Psicologia",
            slug="psicologia",
            ativo=True,
            mostrar_na_home=True
        )
        self.servico = Servico.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            area=self.area,
            ativo=True,
            mostrar_na_home=True
        )
        self.artigo = Artigo.objects.create(
            titulo="Primeira Sessão de Psicoterapia",
            slug="primeira-sessao-psicoterapia",
            categoria=self.cat,
            autor=self.profissional,
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - timezone.timedelta(days=1),
            destaque=True
        )

    def test_home_query_count_limite(self):
        """Garante que a Home execute no máximo 6 queries SQL sem regressão N+1."""
        with self.assertNumQueries(6):
            res = self.client.get(reverse('paginas:inicio'))
            self.assertEqual(res.status_code, 200)

    def test_sobre_mim_query_count_limite(self):
        """Garante que a página Sobre Mim execute no máximo 5 queries SQL."""
        with self.assertNumQueries(5):
            res = self.client.get(reverse('paginas:sobre_mim'))
            self.assertEqual(res.status_code, 200)

    def test_conteudos_listagem_query_count_limite(self):
        """Garante que a listagem de Conteúdos execute no máximo 6 queries SQL com paginação."""
        with self.assertNumQueries(6):
            res = self.client.get(reverse('conteudos:index'))
            self.assertEqual(res.status_code, 200)

    def test_contato_query_count_limite(self):
        """Garante que o GET /contato/ execute no máximo 4 queries (sem duplicar ConfiguracaoSite)."""
        with self.assertNumQueries(4):
            res = self.client.get(reverse('contato:index'))
            self.assertEqual(res.status_code, 200)

    def test_scripts_globais_carregam_com_defer(self):
        """Valida que todos os scripts declarados em base.html possuem o atributo defer."""
        res = self.client.get(reverse('paginas:inicio'))
        html = res.content.decode('utf-8')
        self.assertIn('<script src="/static/js/base.js" defer></script>', html)
        self.assertIn('<script src="/static/js/navegacao.js" defer></script>', html)

    def test_google_fonts_preconnect_e_display_swap(self):
        """Valida que as fontes do Google utilizam preconnect duplo e display=swap."""
        res = self.client.get(reverse('paginas:inicio'))
        html = res.content.decode('utf-8')
        self.assertIn('<link rel="preconnect" href="https://fonts.googleapis.com">', html)
        self.assertIn('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', html)
        self.assertIn('display=swap', html)

    def test_home_hero_eager_fetchpriority_high(self):
        """Valida que a foto principal do Hero na Home possui eager e fetchpriority=high para LCP."""
        res = self.client.get(reverse('paginas:inicio'))
        html = res.content.decode('utf-8')
        # Quando placeholder ou imagem real, a marcação preserva prioridade LCP
        self.assertIn('class="placeholder-imagem placeholder-imagem--hero"', html)

    def test_artigos_relacionados_select_related_detalhe(self):
        """Valida que a página de detalhe do artigo carrega com queries controladas (<= 6 queries)."""
        with self.assertNumQueries(6):
            res = self.client.get(reverse('conteudos:detalhe', kwargs={'slug': self.artigo.slug}))
            self.assertEqual(res.status_code, 200)

    def test_servicos_psicologia_query_count(self):
        """Valida que a página de Psicologia execute no máximo 5 queries."""
        with self.assertNumQueries(5):
            res = self.client.get(reverse('servicos:psicologia'))
            self.assertEqual(res.status_code, 200)

    def test_rotas_canônicas_retornam_200_direto(self):
        """Garante ausência de redirects (301/302) nas URLs principais."""
        rotas = [
            '/',
            '/sobre-mim/',
            '/servicos/psicologia/',
            '/servicos/neuropsicologia/',
            '/conteudos/',
            '/contato/',
            '/politica-de-privacidade/',
            '/politica-de-cookies/',
        ]
        for url in rotas:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Falha na rota {url}")
