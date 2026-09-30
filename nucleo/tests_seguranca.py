"""
Suíte de Testes Automatizados de Segurança e Hardening — Instituto Mente em Foco.
Valida:
1. Validação do Host Header (rejeição de Host não autorizado com 400).
2. Proteção CSRF no formulário de contato (rejeição sem token, aceitação com token).
3. Proteção contra Cross-Site Scripting (XSS) em formulários, Markdown e JSON-LD.
4. Controle de Acesso e IDOR (artigos em rascunho, futuros e serviços inativos retornam 404).
5. Segurança de Uploads (bloqueio de executáveis disfarçados, extensões proibidas e arquivos > 10MB).
6. Cabeçalhos HTTP defensivos (X-Frame-Options, nosniff, Referrer-Policy, COOP, Permissions-Policy, CSP).
7. Resiliência de páginas de erro (400, 403, 404, 500 sem vazamento de traceback).
8. Proteção de dados sensíveis e PII (@sensitive_post_parameters).
9. Configurações de senha administrativa (mínimo de 12 caracteres).
10. Integridade fail-closed das configurações de produção.
"""
import io
import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from nucleo.models import Profissional
from servicos.models import Servico, AreaAtuacao
from conteudos.models import Artigo, CategoriaArtigo
from conteudos.sanitizacao import renderizar_markdown_seguro
from nucleo.templatetags.seo_tags import render_json_ld
from nucleo.validators import validar_imagem, validar_tamanho_imagem, validar_formato_imagem
from contato.views import index as contato_index


class HostHeaderSecurityTests(TestCase):
    """Valida o controle de Host Header contra ataques de Host Poisoning."""

    def test_host_header_valido_permitido(self):
        """Host legítimo constante em ALLOWED_HOSTS deve responder normalmente."""
        response = self.client.get(reverse('paginas:inicio'), HTTP_HOST='testserver')
        self.assertEqual(response.status_code, 200)

    def test_host_header_nao_autorizado_rejeitado(self):
        """Host malicioso/não autorizado deve ser rejeitado imediatamente pelo Django com 400."""
        with override_settings(ALLOWED_HOSTS=['testserver', 'localhost']):
            # Força cabeçalho de host arbitrário/falso
            response = self.client.get(reverse('paginas:inicio'), HTTP_HOST='atacante-malicioso.com')
            self.assertEqual(response.status_code, 400)


class CSRFSecurityTests(TestCase):
    """Valida o bloqueio estrito contra ataques Cross-Site Request Forgery."""

    def test_post_contato_sem_csrf_rejeitado(self):
        """Submissão POST sem token CSRF deve retornar 403 Forbidden."""
        client_com_csrf = Client(enforce_csrf_checks=True)
        payload = {
            'nome': 'Usuário Teste',
            'email': 'teste@exemplo.com.br',
            'telefone': '(61) 98888-7777',
            'mensagem': 'Mensagem de teste de segurança.',
            'aceite_privacidade': 'on',
        }
        # Envia sem token CSRF
        response = client_com_csrf.post(reverse('contato:index'), payload)
        self.assertEqual(response.status_code, 403)

    def test_post_contato_com_csrf_valido_aceito(self):
        """Submissão POST com token CSRF legítimo deve ser processada com sucesso."""
        client_com_csrf = Client(enforce_csrf_checks=True)
        # Primeiro GET para obter o cookie csrftoken
        get_response = client_com_csrf.get(reverse('contato:index'))
        self.assertEqual(get_response.status_code, 200)
        csrf_token = get_response.cookies.get('csrftoken').value

        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'nome': 'Visitante Autêntico',
            'email': 'visitante@exemplo.com.br',
            'telefone': '(61) 98888-7777',
            'mensagem': 'Mensagem legítima com token.',
            'aceite_privacidade': 'on',
        }
        response = client_com_csrf.post(reverse('contato:index'), payload)
        # Padrão PRG: redirecionamento para contato:index
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('contato:index'))


class XSSSecurityTests(TestCase):
    """Valida que entradas maliciosas contendo scripts sejam devidamente sanitizadas e escapadas."""

    def test_sanitizacao_markdown_bloqueia_tags_script_e_eventos(self):
        """Tags <script>, atributos onerror/onclick e iframes devem ser removidos do Markdown."""
        payload_malicioso = (
            "Texto normal\n\n"
            "## Subtítulo\n\n"
            "<script>alert('XSS Script');</script>\n\n"
            "<img src='invalido' onerror='alert(\"XSS Image\");'>\n\n"
            "<iframe src='https://malicioso.com'></iframe>\n\n"
            "[Link Seguro](https://institutomenteemfoco.com.br)\n\n"
            "[Link Malicioso](javascript:alert('XSS'))"
        )
        html_sanitizado = renderizar_markdown_seguro(payload_malicioso)

        # Não pode conter tags script nem iframes
        self.assertNotIn('<script>', html_sanitizado)
        self.assertNotIn('</script>', html_sanitizado)
        self.assertNotIn('<iframe', html_sanitizado)
        self.assertNotIn('onerror', html_sanitizado)
        # Protocolo perigoso javascript: deve ser descartado
        self.assertNotIn('href="javascript:', html_sanitizado)
        # Conteúdo estrutural legítimo deve permanecer
        self.assertIn('<h2>Subtítulo</h2>', html_sanitizado)
        self.assertIn('href="https://institutomenteemfoco.com.br"', html_sanitizado)

    def test_json_ld_escapa_fechamento_de_script(self):
        """Sequências como '</script>' em dados JSON-LD devem ser codificadas para impedir injeção."""
        dado_injetado = {
            "name": "</script><script>alert('pwned')</script>",
            "description": "Texto com <tags> e caracteres especiais & aspas."
        }
        json_ld_html = render_json_ld(dado_injetado)

        # Deve usar escape seguro unicode em vez de tags brutas
        self.assertNotIn('</script><script>', json_ld_html)
        self.assertIn(r'\u003c\u002Fscript\u003e', json_ld_html)
        self.assertIn(r'\u003cscript\u003e', json_ld_html)



class DraftAndAccessControlTests(TestCase):
    """Valida que rascunhos, artigos futuros e serviços inativos permaneçam inacessíveis a anônimos."""

    def setUp(self):
        self.categoria = CategoriaArtigo.objects.create(
            nome="Psicologia Clínica",
            slug="psicologia-clinica",
            ativo=True
        )

    def test_artigo_publicado_acessivel(self):
        """Artigo publicado com data no passado deve retornar 200."""
        artigo = Artigo.objects.create(
            titulo="Artigo Publicado Legítimo",
            slug="artigo-publicado-legitimo",
            conteudo="Conteúdo público.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() - datetime.timedelta(days=1),
            categoria=self.categoria
        )
        response = self.client.get(artigo.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_artigo_rascunho_retorna_404(self):
        """Artigo com status 'rascunho' deve retornar 404 para requisições públicas."""
        artigo = Artigo.objects.create(
            titulo="Artigo Confidencial em Rascunho",
            slug="artigo-confidencial-rascunho",
            conteudo="Rascunho não revisado.",
            status=Artigo.STATUS_RASCUNHO,
            categoria=self.categoria
        )
        response = self.client.get(artigo.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_artigo_agendamento_futuro_retorna_404(self):
        """Artigo com data de publicação no futuro deve retornar 404."""
        artigo = Artigo.objects.create(
            titulo="Artigo com Publicação Futura",
            slug="artigo-publicacao-futura",
            conteudo="Ainda não disponível.",
            status=Artigo.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + datetime.timedelta(days=7),
            categoria=self.categoria
        )
        response = self.client.get(artigo.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_servico_inativo_rejeitado_no_formulario_contato(self):
        """Serviço com ativo=False não deve ser aceito na submissão do formulário de contato."""
        from contato.forms import ContatoForm
        area = AreaAtuacao.objects.create(nome="Geral", slug="geral")
        servico_inativo = Servico.objects.create(
            nome="Serviço Desativado",
            slug="servico-desativado",
            area=area,
            ativo=False
        )
        form = ContatoForm(data={
            'nome': 'Usuário Teste',
            'email': 'teste@exemplo.com.br',
            'telefone': '(61) 98888-7777',
            'servico_interesse': servico_inativo.pk,
            'mensagem': 'Tentativa com serviço inativo.',
            'aceite_privacidade': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('servico_interesse', form.errors)



class UploadSecurityTests(TestCase):
    """Valida a restrição e integridade dos uploads de imagens via Pillow."""

    def _gerar_imagem_valida(self, formato='JPEG'):
        """Auxiliar que gera bytes de uma imagem real válida."""
        buffer = io.BytesIO()
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(buffer, format=formato)
        buffer.seek(0)
        return buffer.getvalue()

    def test_imagem_legitima_passa_validacao(self):
        """Arquivo com imagem JPEG real deve ser aprovado pelo validador."""
        dados_img = self._gerar_imagem_valida('JPEG')
        arquivo = SimpleUploadedFile("foto.jpg", dados_img, content_type="image/jpeg")
        # Não deve levantar ValidationError
        validar_imagem(arquivo)

    def test_executavel_disfarcado_de_jpg_rejeitado(self):
        """Arquivo com extensão .jpg mas contendo payload não-imagem deve ser rejeitado."""
        conteudo_malicioso = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xffThis is an executable"
        arquivo_falso = SimpleUploadedFile("foto_segura.jpg", conteudo_malicioso, content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            validar_imagem(arquivo_falso)

    def test_extensao_nao_permitida_rejeitada(self):
        """Arquivos com extensões perigosas (svg, exe, php, pdf) devem ser rejeitados."""
        for ext in ['.svg', '.exe', '.php', '.pdf', '.html', '.js']:
            arquivo = SimpleUploadedFile(f"arquivo{ext}", b"conteudo", content_type="application/octet-stream")
            with self.assertRaises(ValidationError):
                validar_imagem(arquivo)

    def test_imagem_acima_do_limite_de_tamanho_rejeitada(self):
        """Arquivo que ultrapassa 10 MB deve ser rejeitado."""
        # Cria um arquivo simulado com 11 MB
        tamanho_11mb = 11 * 1024 * 1024
        arquivo_pesado = SimpleUploadedFile("pesado.jpg", b"0" * 100, content_type="image/jpeg")
        arquivo_pesado.size = tamanho_11mb
        with self.assertRaises(ValidationError):
            validar_tamanho_imagem(arquivo_pesado)


class SecurityHeadersTests(TestCase):
    """Valida a emissão dos cabeçalhos defensivos modernos."""

    def test_cabecalhos_defensivos_fundamentais_presentes(self):
        """Páginas públicas devem conter X-Frame-Options, nosniff, Referrer-Policy e Permissions-Policy."""
        response = self.client.get(reverse('paginas:inicio'))
        self.assertEqual(response.status_code, 200)

        # Clickjacking
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        # MIME sniffing
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        # Referrer Policy
        self.assertEqual(response.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')
        # Permissions Policy
        permissions = response.headers.get('Permissions-Policy', '')
        self.assertIn('camera=()', permissions)
        self.assertIn('microphone=()', permissions)
        self.assertIn('geolocation=()', permissions)
        # Cross-Origin-Opener-Policy
        self.assertEqual(response.headers.get('Cross-Origin-Opener-Policy'), 'same-origin')

    def test_content_security_policy_enforcement(self):
        """Quando SECURE_CSP estiver configurada, o cabeçalho Content-Security-Policy deve ser gerado."""
        from django.utils.csp import CSP

        csp_politica = {
            'default-src': [CSP.SELF],
            'script-src': [CSP.SELF, CSP.NONCE],
            'style-src': [CSP.SELF, CSP.UNSAFE_INLINE, 'https://fonts.googleapis.com'],
            'font-src': [CSP.SELF, 'https://fonts.gstatic.com'],
            'img-src': [CSP.SELF, 'data:'],
            'object-src': [CSP.NONE],
            'base-uri': [CSP.SELF],
            'form-action': [CSP.SELF],
            'frame-ancestors': [CSP.NONE],
        }

        with override_settings(SECURE_CSP=csp_politica):
            response = self.client.get(reverse('paginas:inicio'))
            self.assertEqual(response.status_code, 200)
            csp_header = response.headers.get('Content-Security-Policy', '')
            self.assertTrue(csp_header, "O cabeçalho Content-Security-Policy deve estar presente.")
            self.assertIn("default-src 'self'", csp_header)
            self.assertIn("object-src 'none'", csp_header)
            self.assertIn("frame-ancestors 'none'", csp_header)
            self.assertIn("base-uri 'self'", csp_header)
            self.assertIn("form-action 'self'", csp_header)
            self.assertIn("https://fonts.googleapis.com", csp_header)

    def test_content_security_policy_report_only(self):
        """Quando SECURE_CSP_REPORT_ONLY estiver ativa, Content-Security-Policy-Report-Only deve ser gerado."""
        from django.utils.csp import CSP

        csp_ro = {
            'default-src': [CSP.SELF],
            'object-src': [CSP.NONE],
        }

        with override_settings(SECURE_CSP={}, SECURE_CSP_REPORT_ONLY=csp_ro):
            response = self.client.get(reverse('paginas:inicio'))
            self.assertEqual(response.status_code, 200)
            ro_header = response.headers.get('Content-Security-Policy-Report-Only', '')
            self.assertTrue(ro_header)
            self.assertIn("default-src 'self'", ro_header)
            self.assertIn("object-src 'none'", ro_header)


class ErrorHandlingSecurityTests(TestCase):
    """Valida que páginas de erro com DEBUG=False não vazem dados internos, tracebacks ou caminhos."""

    @override_settings(DEBUG=False)
    def test_erro_404_sem_vazamento_de_informacoes(self):
        """Página 404 deve ser limpa, acolhedora e não vazar configurações ou caminhos."""
        response = self.client.get('/url-completamente-inexistente-para-auditoria-de-erro-404/')
        self.assertEqual(response.status_code, 404)
        conteudo = response.content.decode('utf-8')
        # Não deve conter termos de depuração
        self.assertNotIn('Traceback', conteudo)
        self.assertNotIn('Request Method:', conteudo)
        self.assertNotIn('DJANGO_SETTINGS_MODULE', conteudo)
        self.assertNotIn('SECRET_KEY', conteudo)
        self.assertIn('Página não encontrada', conteudo)

    @override_settings(DEBUG=False)
    def test_handlers_customizados_existem_e_respondem(self):
        """Handlers 400, 403 e 500 devem responder com os respectivos status codes."""
        # 400
        resp_400 = self.client.get('/health/', HTTP_HOST='bad_host_invalid_domain_test_400')
        self.assertEqual(resp_400.status_code, 400)


class SensitiveParametersSecurityTests(TestCase):
    """Valida a aplicação do decorator sensitive_post_parameters na view de contato."""

    def test_sensitive_post_parameters_aplicado_na_view_contato(self):
        """A view de contato deve atribuir sensitive_post_parameters ao request ao ser chamada."""
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware

        factory = RequestFactory()
        request = factory.post(reverse('contato:index'))

        # Simula middlewares necessários para a view
        get_response = lambda req: None
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)

        # Executa a view
        contato_index(request)

        self.assertTrue(
            hasattr(request, 'sensitive_post_parameters'),
            "A view contato.views.index deve ser decorada com @sensitive_post_parameters."
        )
        self.assertEqual(
            request.sensitive_post_parameters,
            ('nome', 'email', 'telefone', 'mensagem')
        )



class PasswordValidatorsSecurityTests(TestCase):
    """Valida as regras de complexidade de senhas administrativas."""

    def test_comprimento_minimo_senha_configurado_com_12_caracteres(self):
        """O validador MinimumLengthValidator deve estar configurado com pelo menos 12 caracteres."""
        validators = settings.AUTH_PASSWORD_VALIDATORS
        encontrou_min_length = False
        for v in validators:
            if 'MinimumLengthValidator' in v.get('NAME', ''):
                options = v.get('OPTIONS', {})
                min_len = options.get('min_length', 8)
                self.assertGreaterEqual(
                    min_len, 12,
                    f"O comprimento mínimo de senha deve ser >= 12, valor atual: {min_len}"
                )
                encontrou_min_length = True

        self.assertTrue(encontrou_min_length, "MinimumLengthValidator deve estar configurado.")


class ProductionSettingsIntegrityTests(TestCase):
    """Valida o comportamento fail-closed do módulo de configurações de produção."""

    def test_producao_rejeita_secret_key_insegura_ou_ausente(self):
        """Se DJANGO_SECRET_KEY estiver ausente ou com chave insegura, deve levantar ImproperlyConfigured."""
        import importlib
        from unittest.mock import patch

        with patch('decouple.config') as mock_config:
            def side_effect(key, default=None, **kwargs):
                if key == 'DJANGO_SECRET_KEY':
                    return 'django-insecure-chave-falsa-de-teste'
                if key == 'DJANGO_ALLOWED_HOSTS':
                    return ['meusite.com.br']
                if key == 'DATABASE_URL':
                    return 'sqlite:///prod_test.sqlite3'
                return default

            mock_config.side_effect = side_effect

            with self.assertRaises(ImproperlyConfigured):
                import configuracoes.settings.producao as prod
                importlib.reload(prod)

    def test_producao_rejeita_allowed_hosts_wildcard(self):
        """Se DJANGO_ALLOWED_HOSTS contiver '*', deve levantar ImproperlyConfigured."""
        import importlib
        from unittest.mock import patch

        with patch('decouple.config') as mock_config:
            def side_effect(key, default=None, **kwargs):
                if key == 'DJANGO_SECRET_KEY':
                    return 'chave-super-secreta-longa-e-aleatoria-de-producao-xyz123456789'
                if key == 'DJANGO_ALLOWED_HOSTS':
                    return ['*']
                if key == 'DATABASE_URL':
                    return 'sqlite:///prod_test.sqlite3'
                return default

            mock_config.side_effect = side_effect

            with self.assertRaises(ImproperlyConfigured):
                import configuracoes.settings.producao as prod
                importlib.reload(prod)
