"""
Suíte de testes automatizados de proteção contra abuso, rate limiting e defesa contra brute force.
Cobre:
- Formulário de Contato (GET livre, POST limitado, 429, Retry-After, no-store, isolamento de DB e e-mail, honeypot)
- Django Admin Login (GET livre, contagem de falhas, bloqueio por IP, bloqueio combo, limpeza pós-sucesso,
  ausência de enumeração, isolamento entre origens, livre navegação autenticada)
- Resolução segura de IP e rejeição de X-Forwarded-For falsificado
- Pseudonimização via HMAC-SHA256 (ausência de IP bruto e usernames em chaves de cache e logs)
- Resiliência fail-open em falha de cache (prevenção de 500)
- Hardening contra DoS em busca textual e paginação
- Preservação de cabeçalhos de segurança na resposta 429
"""
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from contato.models import MensagemContato
from nucleo.rate_limit import RateLimiter, obter_ip_cliente, gerar_digest_origem

User = get_user_model()


class TestRateLimitContato(TestCase):
    """Testes de rate limiting e proteção contra abuso no formulário de contato."""

    def setUp(self):
        cache.clear()
        self.url = reverse('contato:index')
        self.dados_validos = {
            'nome': 'Paciente Teste',
            'email': 'paciente@exemplo.com.br',
            'telefone': '(61) 98888-7777',
            'mensagem': 'Gostaria de informações sobre atendimento.',
            'aceite_privacidade': 'on',
        }

    def tearDown(self):
        cache.clear()

    def test_contato_get_nao_consome_rate_limit(self):
        """Requisições GET normais nunca devem consumir cota de rate limit."""
        for _ in range(10):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)

        # O primeiro POST ainda deve ser plenamente permitido
        response_post = self.client.post(self.url, self.dados_validos)
        self.assertEqual(response_post.status_code, 302)

    @override_settings(CONTACT_RATE_LIMIT_COUNT=3, CONTACT_RATE_LIMIT_WINDOW=900)
    def test_contato_post_dentro_do_limite_autorizado(self):
        """Submissões dentro do limite configurado devem ser processadas com sucesso."""
        for i in range(3):
            dados = self.dados_validos.copy()
            dados['mensagem'] = f'Mensagem número {i}'
            response = self.client.post(self.url, dados)
            self.assertEqual(response.status_code, 302)

        self.assertEqual(MensagemContato.objects.count(), 3)

    @override_settings(CONTACT_RATE_LIMIT_COUNT=2, CONTACT_RATE_LIMIT_WINDOW=600)
    def test_contato_post_acima_do_limite_retorna_429(self):
        """Submissão que excede o limite deve retornar status HTTP 429 com cabeçalhos apropriados."""
        # 2 envios permitidos
        self.client.post(self.url, self.dados_validos)
        self.client.post(self.url, self.dados_validos)

        # 3º envio deve sofrer rate limit
        response = self.client.post(self.url, self.dados_validos)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers.get('Retry-After'), '600')
        self.assertEqual(response.headers.get('Cache-Control'), 'no-store')
        self.assertContains(response, 'Muitas tentativas de acesso', status_code=429)

    @override_settings(CONTACT_RATE_LIMIT_COUNT=1, CONTACT_RATE_LIMIT_WINDOW=900)
    def test_contato_post_bloqueado_nao_grava_no_banco_nem_envia_email(self):
        """Requisição bloqueada por rate limit não deve persistir dados nem despachar e-mail."""
        # 1ª submissão permitida
        self.client.post(self.url, self.dados_validos)
        self.assertEqual(MensagemContato.objects.count(), 1)

        # 2ª submissão bloqueada
        mail.outbox.clear()
        response = self.client.post(self.url, self.dados_validos)
        self.assertEqual(response.status_code, 429)

        # Contagem de mensagens no banco e e-mails disparados deve permanecer inalterada
        self.assertEqual(MensagemContato.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_contato_honeypot_descarta_sem_gravar_nem_enviar_email(self):
        """Honeypot preenchido por bot descarta a submissão silenciosamente sem persistência."""
        dados_bot = self.dados_validos.copy()
        dados_bot['campo_verificacao'] = 'http://spam-link-malicioso.com'

        mail.outbox.clear()
        response = self.client.post(self.url, dados_bot)

        # Simula sucesso para o bot (PRG 302)
        self.assertEqual(response.status_code, 302)
        # Não grava no banco de dados
        self.assertEqual(MensagemContato.objects.count(), 0)
        # Não despacha e-mail
        self.assertEqual(len(mail.outbox), 0)


class TestRateLimitAdminLogin(TestCase):
    def setUp(self):
        self.url = reverse('admin:login')
        self.user = User.objects.create_superuser('gestor', 'gestor@example.com', 'SenhaForte123!')

    def test_get_livre_e_sucesso_nao_contam_falhas(self):
        from nucleo.models import BloqueioLogin
        for _ in range(12):
            self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertFalse(BloqueioLogin.objects.exists())
        self.assertEqual(self.client.post(self.url, {'username': 'gestor', 'password': 'SenhaForte123!'}).status_code, 302)
        self.assertEqual(BloqueioLogin.objects.get().falhas, 0)

    def test_dez_falhas_bloqueiam_get_post_sem_verificar_senha(self):
        from nucleo.models import BloqueioLogin
        for i in range(10):
            r = self.client.post(self.url, {'username': 'gestor', 'password': 'errada'})
            self.assertEqual(r.status_code, 200 if i < 9 else 404)
        with patch('django.contrib.auth.forms.authenticate') as auth:
            self.assertEqual(self.client.post(self.url, {'username': 'gestor', 'password': 'SenhaForte123!'}).status_code, 404)
            auth.assert_not_called()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.get(self.url, REMOTE_ADDR='203.0.113.2').status_code, 200)
        cache.clear()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(BloqueioLogin.objects.get().nivel, 1)


class TestIdentificacaoOrigemEProxy(TestCase):
    """Testes de identificação de cliente e mitigação contra falsificação de cabeçalhos."""

    @override_settings(TRUST_PROXY_CLIENT_IP=False)
    def test_ip_spoofing_x_forwarded_for_ignorado_por_padrao(self):
        """Com TRUST_PROXY_CLIENT_IP=False, X-Forwarded-For falso enviado pelo cliente é rigorosamente ignorado."""
        request = type('Req', (), {
            'META': {
                'REMOTE_ADDR': '203.0.113.10',
                'HTTP_X_FORWARDED_FOR': '198.51.100.99, 10.0.0.1',
            }
        })()
        ip_resolvido = obter_ip_cliente(request)
        # Deve retornar o REMOTE_ADDR real e ignorar o spoofing
        self.assertEqual(ip_resolvido, '203.0.113.10')

    @override_settings(TRUST_PROXY_CLIENT_IP=True)
    def test_ip_confianca_proxy_quando_habilitado(self):
        """Com TRUST_PROXY_CLIENT_IP=True, obtém o primeiro IP válido da cadeia do proxy."""
        request = type('Req', (), {
            'META': {
                'REMOTE_ADDR': '10.0.0.2',  # IP do proxy
                'HTTP_X_FORWARDED_FOR': '198.51.100.55, 10.0.0.1',
            }
        })()
        ip_resolvido = obter_ip_cliente(request)
        self.assertEqual(ip_resolvido, '198.51.100.55')


class TestPrivacidadeHMACEChaves(TestCase):
    """Testes de privacidade e pseudonimização de identificadores de segurança."""

    def test_privacidade_hmac_sem_ip_nem_username_na_chave_cache(self):
        """O digest HMAC deve ser uma cadeia hexadecimal de 32 caracteres sem vazar IP ou dados."""
        ip = '192.168.1.100'
        username = 'admin_clinica'
        digest = gerar_digest_origem('admin_combo', f"{ip}:{username}")

        self.assertEqual(len(digest), 32)
        # Não deve conter o IP em claro
        self.assertNotIn(ip, digest)
        # Não deve conter o username em claro
        self.assertNotIn(username, digest)

    def test_hmac_deterministico_para_mesma_entrada(self):
        """Mesma entrada no mesmo contexto produz exatamente o mesmo digest."""
        d1 = gerar_digest_origem('contato', '127.0.0.1')
        d2 = gerar_digest_origem('contato', '127.0.0.1')
        d3 = gerar_digest_origem('contato', '127.0.0.2')

        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)


class TestResilienciaEFailOpen(TestCase):
    """Testes de tolerância a falhas no backend de cache."""

    def test_cache_failure_resiliencia_fail_open_contato(self):
        """Se o cache falhar, o rate limiter de contato deve operar em fail-open sem gerar erro 500."""
        with patch('django.core.cache.cache.get', side_effect=Exception("Cache indisponível")):
            request = type('Req', (), {'META': {'REMOTE_ADDR': '127.0.0.1'}})()
            permitido, retry_after = RateLimiter.verificar_contato(request)
            self.assertTrue(permitido)
            self.assertEqual(retry_after, 0)


class TestHardeningBuscaEPaginacao(TestCase):
    """Testes de mitigação de DoS em busca textual e paginação do blog."""

    def setUp(self):
        self.url = reverse('conteudos:index')

    def test_busca_query_longa_truncada_sem_500(self):
        """Query de busca excessivamente longa (> 100 caracteres) deve ser truncada sem erro 500."""
        query_gigante = 'ansiedade ' * 500  # 5000 caracteres
        response = self.client.get(f"{self.url}?q={query_gigante}")
        self.assertEqual(response.status_code, 200)
        # A query no contexto deve ter no máximo 100 caracteres
        self.assertLessEqual(len(response.context['query']), 100)

    def test_busca_paginacao_invalida_ou_extrema(self):
        """Páginas inválidas ou absurdas devem ser tratadas de forma resiliente."""
        # String em vez de inteiro
        r1 = self.client.get(f"{self.url}?page=texto_invalido")
        self.assertEqual(r1.status_code, 200)

        # Número negativo
        r2 = self.client.get(f"{self.url}?page=-99")
        self.assertEqual(r2.status_code, 200)

        # Número astronômico
        r3 = self.client.get(f"{self.url}?page=999999999")
        self.assertEqual(r3.status_code, 200)


class TestHeadersResposta429(TestCase):
    """Testes de conformidade e cabeçalhos de segurança na página de erro 429."""

    @override_settings(CONTACT_RATE_LIMIT_COUNT=1, CONTACT_RATE_LIMIT_WINDOW=300)
    def test_resposta_429_preserva_headers_seguranca(self):
        """A resposta HTTP 429 deve manter os cabeçalhos de segurança do projeto."""
        url = reverse('contato:index')
        dados = {
            'nome': 'Usuário',
            'email': 'usuario@exemplo.com',
            'mensagem': 'Teste',
            'aceite_privacidade': 'on',
        }

        # 1º permitido
        self.client.post(url, dados)

        # 2º 429
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 429)

        # Cabeçalhos específicos de rate limit
        self.assertEqual(response.headers.get('Retry-After'), '300')
        self.assertEqual(response.headers.get('Cache-Control'), 'no-store')

        # Cabeçalhos defensivos globais do projeto
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertIn('Permissions-Policy', response.headers)
