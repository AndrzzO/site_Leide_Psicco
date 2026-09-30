"""
Testes automatizados completos para SEO Técnico (Prompt 12):
- Robots.txt (dinâmico por ambiente, sem vazar admin)
- Sitemap.xml (django.contrib.sitemaps, exclusão de rascunhos, busca, admin, health)
- Metadados, Canonical, Open Graph e Twitter Cards
- Políticas de rota (Busca com noindex, follow; Políticas legais)
- Governança de ambientes (SEOMiddleware, X-Robots-Tag)
- Verificações de integridade de sistema (System Checks seo.E001, seo.E002, seo.W001)
- Dados estruturados Schema.org (JSON-LD seguro, sanitizado e anti-XSS)
"""
import json
import re
from datetime import timedelta
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from django.core.checks import run_checks

from nucleo.models import ConfiguracaoSite, Profissional
from nucleo.checks import verificar_configuracoes_seo
from nucleo.templatetags.seo_tags import render_json_ld, build_absolute_url
from servicos.models import Servico, AreaAtuacao
from conteudos.models import Artigo, CategoriaArtigo


class RobotsTxtTests(TestCase):
    """Testes da rota /robots.txt dinâmica e segura."""

    def setUp(self):
        self.client = Client()

    @override_settings(SEO_ALLOW_INDEXING=False)
    def test_robots_txt_when_indexing_disabled(self):
        """Em ambiente sem autorização de indexação, bloqueia todos os bots com Disallow: /."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response['Content-Type'])
        content = response.content.decode('utf-8')
        self.assertIn('User-agent: *', content)
        self.assertIn('Disallow: /', content)
        self.assertNotIn('Sitemap:', content)

    @override_settings(SEO_ALLOW_INDEXING=True, SITE_URL='https://institutomenteemfoco.com.br')
    def test_robots_txt_when_indexing_enabled(self):
        """Em ambiente com indexação autorizada, permite rastreamento e indica sitemap.xml."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('User-agent: *', content)
        self.assertIn('Allow: /', content)
        self.assertIn('Sitemap: https://institutomenteemfoco.com.br/sitemap.xml', content)

    @override_settings(DJANGO_ADMIN_URL='painel-secreto-admin/', SEO_ALLOW_INDEXING=True)
    def test_robots_txt_does_not_reveal_private_admin_path(self):
        """Garante que rotas administrativas privadas NÃO são vazadas no robots.txt."""
        response = self.client.get('/robots.txt')
        content = response.content.decode('utf-8')
        self.assertNotIn('painel-secreto-admin', content)


class SitemapXmlTests(TestCase):
    """Testes do gerador de sitemap.xml dinâmico."""

    def setUp(self):
        self.client = Client()
        self.area = AreaAtuacao.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica-area",
            titulo="Área de Psicologia",
            resumo="Resumo da área",
            ativo=True
        )
        self.servico = Servico.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            titulo="Psicoterapia Individual",
            resumo="Espaço de escuta e acolhimento",
            area=self.area,
            ativo=True
        )
        self.categoria = CategoriaArtigo.objects.create(
            nome="Psicoterapia",
            slug="psicoterapia",
            ativo=True
        )
        self.categoria_vazia = CategoriaArtigo.objects.create(
            nome="Categoria Sem Artigos",
            slug="sem-artigos",
            ativo=True
        )
        self.artigo_publicado = Artigo.objects.create(
            titulo="Artigo Publicado no Ar",
            slug="artigo-publicado-no-ar",
            resumo="Resumo do artigo publicado",
            conteudo="Conteúdo textual",
            categoria=self.categoria,
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - timedelta(days=2)
        )
        self.artigo_rascunho = Artigo.objects.create(
            titulo="Artigo em Rascunho",
            slug="artigo-em-rascunho",
            resumo="Resumo rascunho",
            conteudo="Conteúdo rascunho",
            status=Artigo.STATUS_RASCUNHO
        )
        self.artigo_futuro = Artigo.objects.create(
            titulo="Artigo Agendado para o Futuro",
            slug="artigo-agendado-futuro",
            resumo="Resumo futuro",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + timedelta(days=5)
        )

    def test_sitemap_status_and_content_type(self):
        """Retorna HTTP 200 com XML válido."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'xml' in response['Content-Type'],
            f"Esperado tipo XML, recebido: {response['Content-Type']}"
        )

    def test_sitemap_includes_static_pages_and_services(self):
        """Sitemap deve conter páginas institucionais e páginas de serviços ativos."""
        response = self.client.get('/sitemap.xml')
        content = response.content.decode('utf-8')
        # Páginas estáticas
        self.assertIn('/sobre-mim/', content)
        self.assertIn('/contato/', content)
        # Serviços
        self.assertIn('/servicos/psicologia/', content)
        self.assertIn('/servicos/neuropsicologia/', content)
        self.assertIn('/servicos/avaliacao/', content)

    def test_sitemap_includes_published_articles_and_excludes_drafts_and_future(self):
        """Sitemap inclui apenas artigos publicados e exclui rascunhos e futuros."""
        response = self.client.get('/sitemap.xml')
        content = response.content.decode('utf-8')
        self.assertIn('/conteudos/artigo-publicado-no-ar/', content)
        self.assertNotIn('/conteudos/artigo-em-rascunho/', content)
        self.assertNotIn('/conteudos/artigo-agendado-futuro/', content)

    def test_sitemap_includes_only_active_categories_with_published_articles(self):
        """Apenas categorias com artigos publicados devem estar no sitemap."""
        response = self.client.get('/sitemap.xml')
        content = response.content.decode('utf-8')
        self.assertIn('/conteudos/categoria/psicoterapia/', content)
        self.assertNotIn('/conteudos/categoria/sem-artigos/', content)

    def test_sitemap_excludes_private_and_utility_routes(self):
        """Sitemap não deve conter rotas de admin, health, design-system ou busca."""
        response = self.client.get('/sitemap.xml')
        content = response.content.decode('utf-8')
        self.assertNotIn('admin', content)
        self.assertNotIn('/health/', content)
        self.assertNotIn('/design-system/', content)
        self.assertNotIn('?q=', content)


class SEOMetadataAndCanonicalTests(TestCase):
    """Testes de tags canônicas, metadados, Open Graph e Twitter Cards."""

    def setUp(self):
        self.client = Client()
        self.categoria = CategoriaArtigo.objects.create(
            nome="Relacionamentos",
            slug="relacionamentos",
            ativo=True
        )
        self.artigo = Artigo.objects.create(
            titulo="Compreendendo Novos Começos",
            slug="compreendendo-novos-comecos",
            resumo="Uma análise reflexiva sobre recomeços afetivos.",
            status=Artigo.STATUS_PUBLICADO,
            categoria=self.categoria,
            data_publicacao=timezone.now() - timedelta(days=1)
        )

    def test_canonical_absolute_url_on_home(self):
        """Home possui tag canônica absoluta correta."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<link rel="canonical" href="http://localhost:8000/">', content)

    def test_canonical_absolute_url_on_article(self):
        """Página de artigo possui tag canônica absoluta correta."""
        response = self.client.get(self.artigo.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(
            f'<link rel="canonical" href="http://localhost:8000{self.artigo.get_absolute_url()}">',
            content
        )

    def test_open_graph_tags_on_article(self):
        """Artigo exibe tags Open Graph com og:type=article."""
        response = self.client.get(self.artigo.get_absolute_url())
        content = response.content.decode('utf-8')
        self.assertIn('<meta property="og:type" content="article">', content)
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:description"', content)
        self.assertIn('property="og:url"', content)
        self.assertIn('property="og:image"', content)

    def test_twitter_cards_present(self):
        """Páginas exibem metadados de Twitter Cards com summary_large_image."""
        response = self.client.get('/sobre-mim/')
        content = response.content.decode('utf-8')
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', content)
        self.assertIn('name="twitter:title"', content)
        self.assertIn('name="twitter:description"', content)
        self.assertIn('name="twitter:image"', content)

    def test_search_results_have_noindex_follow(self):
        """Busca interna (/conteudos/?q=termo) deve ter noindex, follow e canonical limpo."""
        response = self.client.get('/conteudos/?q=termo')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<meta name="robots" content="noindex, follow">', content)
        self.assertIn('<link rel="canonical" href="http://localhost:8000/conteudos/">', content)

    def test_privacy_and_cookies_pages_have_noindex_follow(self):
        """Páginas de políticas devem conter noindex, follow e canonical estável."""
        response = self.client.get('/politica-de-privacidade/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<meta name="robots" content="noindex, follow">', content)
        self.assertIn(
            '<link rel="canonical" href="http://localhost:8000/politica-de-privacidade/">',
            content
        )

        response_cookies = self.client.get('/politica-de-cookies/')
        self.assertEqual(response_cookies.status_code, 200)
        content_cookies = response_cookies.content.decode('utf-8')
        self.assertIn('<meta name="robots" content="noindex, follow">', content_cookies)
        self.assertIn(
            '<link rel="canonical" href="http://localhost:8000/politica-de-cookies/">',
            content_cookies
        )


class SEOMiddlewareAndIndexingGovernanceTests(TestCase):
    """Testes do middleware de governança e proteção HTTP X-Robots-Tag."""

    def setUp(self):
        self.client = Client()

    @override_settings(SEO_ALLOW_INDEXING=False)
    def test_x_robots_tag_header_when_indexing_disabled(self):
        """Quando SEO_ALLOW_INDEXING for False, qualquer resposta recebe X-Robots-Tag restritivo."""
        response = self.client.get('/')
        self.assertEqual(
            response.headers.get('X-Robots-Tag'),
            'noindex, nofollow, noarchive'
        )

    @override_settings(SEO_ALLOW_INDEXING=True)
    def test_x_robots_tag_header_on_search_when_indexing_enabled(self):
        """Em produção, resultados de pesquisa recebem X-Robots-Tag: noindex, follow."""
        response = self.client.get('/conteudos/?q=teste')
        self.assertEqual(
            response.headers.get('X-Robots-Tag'),
            'noindex, follow'
        )

    @override_settings(SEO_ALLOW_INDEXING=True)
    def test_x_robots_tag_header_on_404_when_indexing_enabled(self):
        """Em produção, páginas de erro recebem X-Robots-Tag: noindex, nofollow."""
        response = self.client.get('/rota-inexistente-404/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get('X-Robots-Tag'),
            'noindex, nofollow'
        )


class SEOSystemChecksTests(TestCase):
    """Testes dos checks de integridade do Django (System Checks)."""

    @override_settings(SEO_ALLOW_INDEXING=False, DEBUG=True, SITE_URL='http://localhost:8000')
    def test_check_passes_in_development(self):
        """Em desenvolvimento normal com SEO_ALLOW_INDEXING=False, nenhum erro é emitido."""
        erros = verificar_configuracoes_seo(None)
        self.assertEqual(len(erros), 0)

    @override_settings(SEO_ALLOW_INDEXING=True, DEBUG=True, SITE_URL='https://institutomenteemfoco.com.br')
    def test_check_e001_indexing_with_debug_true(self):
        """SEO_ALLOW_INDEXING=True com DEBUG=True dispara erro crítico seo.E001."""
        erros = verificar_configuracoes_seo(None)
        ids = [e.id for e in erros]
        self.assertIn('seo.E001', ids)

    @override_settings(SEO_ALLOW_INDEXING=True, DEBUG=False, SITE_URL='http://localhost:8000')
    def test_check_e002_indexing_with_local_site_url(self):
        """SEO_ALLOW_INDEXING=True com localhost dispara erro crítico seo.E002."""
        erros = verificar_configuracoes_seo(None)
        ids = [e.id for e in erros]
        self.assertIn('seo.E002', ids)

    @override_settings(SEO_ALLOW_INDEXING=True, DEBUG=False, SITE_URL='http://institutomenteemfoco.com.br')
    def test_check_w001_indexing_without_https(self):
        """SEO_ALLOW_INDEXING=True com HTTP (não HTTPS) dispara aviso seo.W001."""
        erros = verificar_configuracoes_seo(None)
        ids = [e.id for e in erros]
        self.assertIn('seo.W001', ids)

    @override_settings(SEO_ALLOW_INDEXING=True, DEBUG=False, SITE_URL='https://institutomenteemfoco.com.br')
    def test_check_passes_with_correct_production_settings(self):
        """Configuração correta de produção passa 100% sem erros ou avisos."""
        erros = verificar_configuracoes_seo(None)
        self.assertEqual(len(erros), 0)


class StructuredDataJSONLDTests(TestCase):
    """Testes dos esquemas Schema.org (JSON-LD) e sanitização anti-XSS."""

    def setUp(self):
        self.client = Client()
        self.config_site = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            whatsapp="5561999999999",
            email="contato@institutomenteemfoco.com.br",
            endereco_texto="Asa Sul, Brasília - DF",
            ativo=True
        )
        self.profissional = Profissional.objects.create(
            nome="Mari Menezes",
            registro_profissional="CRP 01/12345",
            ativo=True,
            destaque=True
        )
        self.categoria = CategoriaArtigo.objects.create(
            nome="Psicologia",
            slug="psicologia",
            ativo=True
        )
        self.artigo = Artigo.objects.create(
            titulo="Artigo com Teste de Script",
            slug="artigo-teste-script",
            resumo="Resumo seguro",
            status=Artigo.STATUS_PUBLICADO,
            categoria=self.categoria,
            data_publicacao=timezone.now() - timedelta(hours=1)
        )

    def test_global_schema_on_home(self):
        """Home deve conter JSON-LD com WebSite, Organization e Person."""
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        self.assertIn('<script type="application/ld+json">', content)
        
        # Extrai o JSON-LD
        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        self.assertIsNotNone(match)
        json_data = json.loads(match.group(1))
        
        # Validações estruturais
        self.assertEqual(json_data.get('@context'), 'https://schema.org')
        graph = json_data.get('@graph', [])
        types = [item.get('@type') for item in graph]
        self.assertIn('WebSite', types)
        self.assertIn('Organization', types)
        self.assertIn('Person', types)

    def test_article_schema_on_article_page(self):
        """Página de artigo deve conter schema BlogPosting e BreadcrumbList."""
        response = self.client.get(self.artigo.get_absolute_url())
        content = response.content.decode('utf-8')
        
        # Localiza blocos JSON-LD
        scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        self.assertTrue(len(scripts) >= 1)
        
        combined_json = " ".join(scripts)
        self.assertIn('BlogPosting', combined_json)
        self.assertIn('BreadcrumbList', combined_json)

    def test_service_schema_on_service_page(self):
        """Página de psicologia deve conter schema Service."""
        response = self.client.get('/servicos/psicologia/')
        content = response.content.decode('utf-8')
        scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        self.assertTrue(len(scripts) >= 1)
        combined_json = " ".join(scripts)
        self.assertIn('Service', combined_json)
        self.assertIn('Psicoterapia Clínica', combined_json)

    def test_anti_xss_protection_in_json_ld(self):
        """
        Garante que qualquer tentativa de injetar tags script de fechamento
        em dados serializados seja neutralizada (</script> escapado).
        """
        payload_malicioso = {
            "titulo": "</script><script>alert('XSS')</script>",
            "descricao": "<img src=x onerror=alert(1)>"
        }
        tag_html = render_json_ld(payload_malicioso)
        
        # Não pode conter literal </script> exceto a tag final do bloco
        script_closers = tag_html.count('</script>')
        self.assertEqual(script_closers, 1, "Houve fechamento indevido da tag de script!")
        
        # O payload interno deve conter \u003c ou \u002F
        self.assertIn(r'\u003c', tag_html)
        self.assertNotIn("<script>alert('XSS')</script>", tag_html)

    def test_zero_fake_ratings_or_reviews(self):
        """Garante a ausência absoluta de esquemas de avaliação falsa em qualquer página."""
        rotas = ['/', '/sobre-mim/', '/servicos/psicologia/', '/servicos/neuropsicologia/', '/contato/']
        for rota in rotas:
            res = self.client.get(rota)
            html = res.content.decode('utf-8')
            self.assertNotIn('AggregateRating', html, f"AggregateRating encontrado na rota {rota}")
            self.assertNotIn('reviewRating', html, f"reviewRating encontrado na rota {rota}")
            self.assertNotIn('starRating', html, f"starRating encontrado na rota {rota}")
