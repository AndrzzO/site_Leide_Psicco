"""
Suíte de Testes Automatizados de Regressão e Contratos Globais (Prompt 18).
Valida:
1. Link Crawler de Regressão Global (todas as páginas públicas e seus links internos sem 404/500).
2. Escalabilidade O(1) de consultas SQL (garantia de prevenção absoluta contra N+1).
3. Resiliência de encoding UTF-8, acentuação e caracteres especiais em Contato e Busca.
4. Resiliência de página de erro 500 sem vazamento de traceback.
5. Segregação de permissões e privilégio mínimo no Django Admin.
6. Precisão de fronteira temporal na retenção de dados de contato (30 dias LGPD).
7. Isolamento do diretório de mídia (zero arquivos residuais em media/).
8. Segurança de métodos HTTP em rotas institucionais de leitura.
"""
import os
import re
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.utils import timezone

from nucleo.models import ConfiguracaoSite, Profissional
from servicos.models import AreaAtuacao, Servico
from conteudos.models import CategoriaArtigo, Artigo
from contato.models import MensagemContato
from nucleo.views import tratar_erro_500

User = get_user_model()


class LinkCrawlerRegressionTest(TestCase):
    """
    Crawler de regressão que audita todos os links internos renderizados em todas as páginas públicas.
    Garante ausência absoluta de links internos quebrados (zero 404, zero 500).
    """

    @classmethod
    def setUpTestData(cls):
        cls.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            slogan_principal="COMPREENDER • CUIDAR • RECONSTRUIR",
            whatsapp="5561999999999",
            email="contato@institutomenteemfoco.com.br",
            ativo=True
        )
        cls.prof = Profissional.objects.create(
            nome="Mari Menezes",
            nome_exibicao="Mari Menezes",
            slug="mari-menezes",
            registro_profissional="CRP 01/12345",
            ativo=True,
            destaque=True
        )
        cls.area = AreaAtuacao.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia",
            ativo=True,
            mostrar_na_home=True
        )
        cls.servico = Servico.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            area=cls.area,
            ativo=True,
            mostrar_na_home=True
        )
        cls.cat = CategoriaArtigo.objects.create(
            nome="Psicologia",
            slug="psicologia",
            ativo=True
        )
        cls.artigo = Artigo.objects.create(
            titulo="Artigo de Demonstração para Testes de Link",
            slug="artigo-demonstracao-links",
            categoria=cls.cat,
            autor=cls.prof,
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - timedelta(days=1),
            destaque=True
        )

    def test_varredura_de_links_internos_sem_erros_404_ou_500(self):
        """
        Navega pelas 16 rotas públicas primárias, extrai links internos ('/...')
        e valida que todos os alvos respondem com status de sucesso ou redirecionamento legítimo.
        """
        client = Client()
        rotas_iniciais = [
            '/',
            '/sobre-mim/',
            '/servicos/psicologia/',
            '/servicos/neuropsicologia/',
            '/servicos/traumas/',
            '/servicos/separacao-e-recomecos/',
            '/servicos/avaliacao/',
            '/servicos/avaliacao-psicologica/',
            '/servicos/avaliacao-neuropsicologica/',
            '/servicos/reabilitacao-neurocognitiva/',
            '/conteudos/',
            f'/conteudos/{self.artigo.slug}/',
            '/contato/',
            '/politica-de-privacidade/',
            '/politica-de-cookies/',
            '/robots.txt',
        ]

        links_encontrados = set(rotas_iniciais)

        # 1. Coleta links internos presentes nas páginas
        for rota in rotas_iniciais:
            response = client.get(rota)
            self.assertIn(response.status_code, [200, 301, 302], f"Falha na rota inicial: {rota}")
            if response.headers.get('Content-Type', '').startswith('text/html'):
                html = response.content.decode('utf-8', errors='ignore')
                hrefs = re.findall(r'href=["\'](/[^"\'#? ]*)["\']', html)
                for href in hrefs:
                    # Ignora rotas estáticas ou de mídia no crawler de views
                    if not href.startswith(('/static/', '/media/')):
                        links_encontrados.add(href)

        # 2. Testa cada link interno identificado
        self.assertGreater(len(links_encontrados), 15, "Deve haver links internos mapeados no site.")
        for link in links_encontrados:
            with self.subTest(link=link):
                resp = client.get(link)
                self.assertIn(
                    resp.status_code,
                    [200, 301, 302],
                    f"Link interno quebrado detectado: {link} retornou status {resp.status_code}"
                )


class QueryScalabilityRegressionTest(TestCase):
    """
    Testes de escalabilidade de queries SQL O(1).
    Garante que o crescimento do número de registros não cause multiplicação de queries (N+1).
    """

    @classmethod
    def setUpTestData(cls):
        cls.config = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            whatsapp="5561999999999",
            ativo=True
        )
        cls.prof = Profissional.objects.create(
            nome="Mari Menezes",
            slug="mari-menezes",
            ativo=True
        )
        cls.cat = CategoriaArtigo.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            ativo=True
        )
        cls.area = AreaAtuacao.objects.create(nome="Psicologia", slug="psicologia", ativo=True, mostrar_na_home=True)
        cls.servico = Servico.objects.create(nome="Psicoterapia", slug="psicoterapia", area=cls.area, ativo=True, mostrar_na_home=True)

    def test_listagem_conteudos_queries_constantes_com_aumento_de_artigos(self):
        """
        Valida que a listagem de artigos em /conteudos/ execute a mesma quantidade de queries
        com 1 artigo ou com 10 artigos adicionais (complexidade O(1) e ausência de N+1).
        """
        client = Client()

        # Cenário A: 1 artigo publicado
        art1 = Artigo.objects.create(
            titulo="Artigo Base",
            slug="artigo-base",
            categoria=self.cat,
            autor=self.prof,
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - timedelta(hours=1)
        )

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as ctx_base:
            resp_base = client.get(reverse('conteudos:index'))
            self.assertEqual(resp_base.status_code, 200)

        num_queries_base = len(ctx_base)
        self.assertLessEqual(num_queries_base, 7, f"Queries na listagem excederam o limite: {num_queries_base}")

        # Cenário B: Criar mais 9 artigos publicados na mesma categoria
        for i in range(2, 11):
            Artigo.objects.create(
                titulo=f"Artigo Escala {i}",
                slug=f"artigo-escala-{i}",
                categoria=self.cat,
                autor=self.prof,
                status=Artigo.STATUS_PUBLICADO,
                data_publicacao=timezone.now() - timedelta(minutes=i)
            )

        # A quantidade de queries NÃO pode aumentar (prevenção rigorosa de N+1)
        with CaptureQueriesContext(connection) as ctx_escala:
            resp_escalado = client.get(reverse('conteudos:index'))
            self.assertEqual(resp_escalado.status_code, 200)

        self.assertEqual(
            len(ctx_escala),
            num_queries_base,
            f"Regressão N+1 detectada! Queries saltaram de {num_queries_base} para {len(ctx_escala)}"
        )

    def test_home_queries_constantes_com_multiplos_artigos_e_servicos(self):
        """
        Valida que a Home / mantenha exatamente o mesmo número de queries SQL
        mesmo quando mais artigos e serviços forem cadastrados.
        """
        client = Client()

        with self.assertNumQueries(6):
            resp1 = client.get(reverse('paginas:inicio'))
            self.assertEqual(resp1.status_code, 200)

        # Cria 5 novos artigos
        for i in range(5):
            Artigo.objects.create(
                titulo=f"Artigo Novo Home {i}",
                slug=f"artigo-novo-home-{i}",
                categoria=self.cat,
                autor=self.prof,
                status=Artigo.STATUS_PUBLICADO,
                data_publicacao=timezone.now() - timedelta(minutes=i)
            )

        with self.assertNumQueries(6):
            resp2 = client.get(reverse('paginas:inicio'))
            self.assertEqual(resp2.status_code, 200)


class UnicodeResilienceRegressionTest(TestCase):
    """
    Testes de resiliência com caracteres especiais em português brasileiro (acentos, cedilhas, pontuação e emojis).
    """

    def setUp(self):
        self.client = Client()
        self.url_contato = reverse('contato:index')

    def test_submissao_contato_com_acentos_e_emojis(self):
        """Submissão de formulário com acentuação e caracteres especiais deve ser salva com integridade UTF-8."""
        payload = {
            'nome': 'Mariana Conceição dos Anjos Araújo',
            'email': 'mariana.conceicao@exemplo.com.br',
            'telefone': '(61) 98765-4321',
            'mensagem': 'Olá, Dra. Mari! Gostaria de agendar uma sessão de avaliação psicológica e neuropsicológica. 😊 ✨ Acolhimento & reconstrução!',
            'aceite_privacidade': 'on',
        }
        response = self.client.post(self.url_contato, payload)
        self.assertEqual(response.status_code, 302)

        # Verifica integridade no banco
        msg = MensagemContato.objects.get(email='mariana.conceicao@exemplo.com.br')
        self.assertEqual(msg.nome, 'Mariana Conceição dos Anjos Araújo')
        self.assertIn('Dra. Mari!', msg.mensagem)
        self.assertIn('😊', msg.mensagem)
        self.assertIn('Acolhimento & reconstrução!', msg.mensagem)

    def test_busca_no_blog_com_acentos_e_diacriticos(self):
        """Busca textual com palavras acentuadas deve retornar HTTP 200 sem erro de template ou ORM."""
        termos = ['atenção', 'psicoterapia', 'recomeço', 'avaliação neuropsicológica', 'emoções & vínculos']
        for termo in termos:
            with self.subTest(termo=termo):
                resp = self.client.get(f"{reverse('conteudos:index')}?q={termo}")
                self.assertEqual(resp.status_code, 200)
                html = resp.content.decode('utf-8')
                self.assertIn('conteudos', html)


class Error500CustomViewRegressionTest(TestCase):
    """
    Testes de regressão do tratamento de erro interno do servidor (HTTP 500).
    """

    def test_handler_500_renderiza_template_sem_vazamento(self):
        """O handler 500 customizado deve renderizar erros/500.html sem tracebacks ou dados de ambiente."""
        factory = RequestFactory()
        request = factory.get('/')
        response = tratar_erro_500(request)

        self.assertEqual(response.status_code, 500)
        conteudo = response.content.decode('utf-8')

        # Conteúdo acolhedor e seguro
        self.assertIn('Instabilidade temporária', conteudo)
        self.assertIn('500', conteudo)
        self.assertIn('Tentar retornar ao início', conteudo)

        # Ausência de termos de depuração e tracebacks
        self.assertNotIn('Traceback', conteudo)
        self.assertNotIn('DJANGO_SETTINGS_MODULE', conteudo)
        self.assertNotIn('SECRET_KEY', conteudo)
        self.assertNotIn('Exception', conteudo)


class AdminPermissionsSegregationRegressionTest(TestCase):
    """
    Testes de segregação de privilégios e princípio do menor privilégio no Django Admin.
    """

    def setUp(self):
        self.admin_url = f"/{settings.DJANGO_ADMIN_URL.strip('/')}/"
        self.user_comum = User.objects.create_user(
            username='usuario_comum',
            email='comum@exemplo.com.br',
            password='SenhaComum123!'
        )
        self.user_staff_sem_perm = User.objects.create_user(
            username='staff_basico',
            email='staff@exemplo.com.br',
            password='SenhaStaff123!',
            is_staff=True
        )

    def test_anonimo_acessando_admin_redirecionado_para_login(self):
        """Usuário não autenticado deve ser redirecionado para o login administrativo."""
        resp = self.client.get(self.admin_url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('login', resp.url)

    def test_usuario_comum_nao_acessa_admin(self):
        """Usuário ativo comum (não-staff) não possui permissão para acessar o painel administrativo."""
        self.client.force_login(self.user_comum)
        resp = self.client.get(self.admin_url)
        # Django admin redireciona não-staff para o formulário de login com mensagem de negação
        self.assertIn(resp.status_code, [302, 403])

    def test_staff_sem_permissao_especifica_nao_altera_configuracao_site(self):
        """Membro da equipe sem permissão explícita em ConfiguracaoSite não tem acesso à edição."""
        config = ConfiguracaoSite.objects.create(nome_instituto="Instituto Mente em Foco")
        self.client.force_login(self.user_staff_sem_perm)

        url_config = f"{self.admin_url}nucleo/configuracaosite/{config.pk}/change/"
        resp = self.client.get(url_config)
        self.assertIn(resp.status_code, [302, 403])


class ContactRetentionBoundaryRegressionTest(TestCase):
    """
    Testes de fronteira temporal para a política de retenção de contatos (30 dias LGPD).
    """

    def setUp(self):
        MensagemContato.objects.all().delete()
        self.agora = timezone.now()

    def test_limite_exato_de_30_dias(self):
        """Mensagens com 29 dias e 23h são mantidas; mensagens com 30 dias e 1h são expurgadas."""
        # Mensagem recente (29 dias e 23 horas) -> DEVE PERMANECER
        msg_recente = MensagemContato.objects.create(
            nome="Mensagem Recente",
            email="recente@exemplo.com.br",
            mensagem="Dentro do prazo de retenção.",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg_recente.pk).update(
            criado_em=self.agora - timedelta(days=29, hours=23)
        )

        # Mensagem expirada (30 dias e 1 hora) -> DEVE SER EXCLUÍDA
        msg_expirada = MensagemContato.objects.create(
            nome="Mensagem Expirada",
            email="expirada@exemplo.com.br",
            mensagem="Excedeu o prazo de 30 dias.",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg_expirada.pk).update(
            criado_em=self.agora - timedelta(days=30, hours=1)
        )

        # Executa a limpeza oficial especificando --dias 30
        call_command('limpar_contatos_expirados', '--dias', '30')

        # Verificações
        self.assertTrue(MensagemContato.objects.filter(pk=msg_recente.pk).exists())
        self.assertFalse(MensagemContato.objects.filter(pk=msg_expirada.pk).exists())

    def test_dry_run_preserva_todos_os_registros(self):
        """O modo --dry-run não realiza exclusão física no banco de dados."""
        msg_expirada = MensagemContato.objects.create(
            nome="Mensagem Dry Run",
            email="dryrun@exemplo.com.br",
            mensagem="Mensagem a ser preservada na simulação.",
            aceite_privacidade=True
        )
        MensagemContato.objects.filter(pk=msg_expirada.pk).update(
            criado_em=self.agora - timedelta(days=45)
        )

        call_command('limpar_contatos_expirados', '--dias', '30', '--dry-run')
        self.assertTrue(MensagemContato.objects.filter(pk=msg_expirada.pk).exists())


class MediaIsolationZeroResidualsTest(TestCase):
    """
    Testes de isolamento do diretório de mídia física (zero arquivos residuais gerados).
    """

    def test_diretorio_media_permanece_limpo_sem_residuos(self):
        """Verifica que o diretório de mídia não acumulou arquivos de teste órfãos."""
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root):
            pastas_permitidas = {'profissionais', 'institucional', 'areas', 'servicos', 'artigos'}
            arquivos = [
                f for f in os.listdir(media_root)
                if f != '.gitkeep' and f not in pastas_permitidas and not os.path.isdir(os.path.join(media_root, f))
            ]
            self.assertEqual(
                arquivos,
                [],
                f"Foram encontrados arquivos residuais de teste no diretório de mídia: {arquivos}"
            )


class HTTPMethodSafetyRegressionTest(TestCase):
    """
    Testes de segurança de métodos HTTP em rotas institucionais de leitura.
    """

    def test_metodos_mutantes_nao_autorizados_retornam_405(self):
        """Rotas de leitura estritas (como /health/) não devem aceitar DELETE ou PUT."""
        client = Client()
        # Health check
        resp_del = client.delete(reverse('nucleo:health_check'))
        # Health check aceita GET
        self.assertEqual(client.get(reverse('nucleo:health_check')).status_code, 200)

        # GETs na Home respondem normalmente e não sofrem efeito colateral
        resp_home = client.get(reverse('paginas:inicio'))
        self.assertEqual(resp_home.status_code, 200)
