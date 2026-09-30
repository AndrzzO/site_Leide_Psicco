import io
import os
from unittest import mock
from PIL import Image

from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib import admin

from nucleo.models import ConfiguracaoSite, Profissional, RedeSocial
from nucleo.context_processors import dados_institucionais
from nucleo.validators import (
    validar_tamanho_imagem,
    validar_formato_imagem,
    validar_imagem,
    TAMANHO_MAXIMO_IMAGEM_BYTES,
)


def _criar_imagem_teste(formato='PNG', tamanho=(10, 10)):
    """Gera uma imagem válida em memória para testes."""
    buffer = io.BytesIO()
    img = Image.new('RGB', tamanho, color='white')
    img.save(buffer, format=formato)
    buffer.seek(0)
    ext = formato.lower()
    return SimpleUploadedFile(f'teste.{ext}', buffer.getvalue(), content_type=f'image/{ext}')


class NucleoBasicoTests(TestCase):
    """Testes para utilitários do app nucleo, health check e páginas de erro."""

    def test_health_check_retorna_200_ok(self):
        """A rota /health/ deve responder HTTP 200 com corpo 'OK' puro e noindex."""
        response = self.client.get(reverse('nucleo:health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'OK')
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('noindex, nofollow', response.headers.get('X-Robots-Tag', ''))

    def test_health_ready_retorna_200_ok_e_noindex(self):
        """A rota /health/ready/ deve responder HTTP 200 com corpo 'OK' e noindex quando banco responde."""
        response = self.client.get(reverse('nucleo:health_ready'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'OK')
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('noindex, nofollow', response.headers.get('X-Robots-Tag', ''))

    @mock.patch('django.db.connection.cursor')
    def test_health_ready_retorna_503_em_falha_de_banco(self, mock_cursor):
        """A rota /health/ready/ deve responder HTTP 503 com corpo 'UNAVAILABLE' quando banco falha."""
        mock_cursor.side_effect = Exception("Erro de banco simulado")
        response = self.client.get(reverse('nucleo:health_ready'))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content.decode('utf-8'), 'UNAVAILABLE')
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('noindex, nofollow', response.headers.get('X-Robots-Tag', ''))

    def test_pagina_404_personalizada(self):
        """Uma rota inexistente deve responder HTTP 404 e utilizar o template erros/404.html."""
        response = self.client.get('/rota-inexistente-para-teste-404/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'erros/404.html')
        self.assertContains(response, 'Página não encontrada', status_code=404)

    def test_producao_bloqueia_secret_key_insegura(self):
        """O settings de produção deve rejeitar inicialização com chave padrão ou insegura."""
        import runpy
        with mock.patch.dict(os.environ, {
            'DJANGO_SECRET_KEY': 'django-insecure-chave-de-teste',
            'DJANGO_ALLOWED_HOSTS': 'example.com',
            'DATABASE_URL': 'sqlite:///db.sqlite3',
        }):
            with self.assertRaises(ImproperlyConfigured):
                runpy.run_module('configuracoes.settings.producao')


class NucleoModelsTests(TestCase):
    """Testes dos models institucionais do app nucleo."""

    def test_configuracao_site_singleton(self):
        """ConfiguracaoSite deve manter um registro único e impedir duplicações."""
        config1 = ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco",
            whatsapp="5561999999999"
        )
        self.assertEqual(config1.pk, 1)
        self.assertEqual(str(config1), "Instituto Mente em Foco")
        self.assertIn("https://wa.me/5561999999999", config1.whatsapp_link)

        # Tentativa de criar segundo registro via clean deve falhar
        config2 = ConfiguracaoSite(nome_instituto="Outro Instituto")
        with self.assertRaises(ValidationError):
            config2.clean()

        # Método get_solo deve retornar o registro existente
        solo = ConfiguracaoSite.get_solo()
        self.assertEqual(solo.pk, 1)

    def test_profissional_criacao_e_slug(self):
        """Profissional deve gerar slug automaticamente a partir do nome."""
        prof = Profissional.objects.create(
            nome="Mari Menezes",
            titulo_profissional="Psicóloga"
        )
        self.assertEqual(prof.slug, "mari-menezes")
        self.assertIn("Mari Menezes", str(prof))
        self.assertTrue(prof.ativo)
        self.assertTrue(prof.destaque)

    def test_rede_social_criacao_e_ordenacao(self):
        """RedeSocial deve ser cadastrada e ordenada conforme 'ordem'."""
        rede2 = RedeSocial.objects.create(nome="YouTube", url="https://youtube.com", ordem=2)
        rede1 = RedeSocial.objects.create(nome="Instagram", url="https://instagram.com", ordem=1)
        
        redes = list(RedeSocial.objects.all())
        self.assertEqual(redes[0], rede1)
        self.assertEqual(redes[1], rede2)
        self.assertIn("Instagram", str(rede1))


class ContextProcessorTests(TestCase):
    """Testes de resiliência e integridade do context processor."""

    def test_context_processor_com_configuracao_existente(self):
        """Context processor deve ler dados da ConfiguracaoSite ativa."""
        ConfiguracaoSite.objects.create(
            nome_instituto="Instituto Mente em Foco Personalizado",
            slogan_principal="SLOGAN TESTE",
            whatsapp="5561988887777"
        )
        contexto = dados_institucionais(None)
        self.assertEqual(contexto['NOME_INSTITUTO'], "Instituto Mente em Foco Personalizado")
        self.assertEqual(contexto['CONCEITO_TRIPLICE'], "SLOGAN TESTE")
        self.assertIn("5561988887777", contexto['WHATSAPP_LINK'])

    def test_context_processor_sem_configuracao_nao_quebra(self):
        """Context processor deve responder com fallbacks seguros se o banco estiver vazio."""
        ConfiguracaoSite.objects.all().delete()
        contexto = dados_institucionais(None)
        self.assertEqual(contexto['NOME_INSTITUTO'], "Instituto Mente em Foco")
        self.assertEqual(contexto['CONCEITO_TRIPLICE'], "COMPREENDER • CUIDAR • RECONSTRUIR")
        self.assertIsNone(contexto['CONFIGURACAO_SITE'])


class ValidadoresImagemTests(SimpleTestCase):
    """Testes de segurança de upload de arquivos e imagens."""

    def test_imagem_valida_passa(self):
        """Arquivo PNG válido deve passar sem exceção."""
        img_valida = _criar_imagem_teste(formato='PNG')
        try:
            validar_imagem(img_valida)
        except ValidationError:
            self.fail("validar_imagem lançou ValidationError para uma imagem válida.")

    def test_imagem_acima_do_limite_rejeitada(self):
        """Arquivo acima do limite de tamanho deve ser rejeitado."""
        arquivo_gigante = SimpleUploadedFile(
            'pesada.png',
            b'x' * (TAMANHO_MAXIMO_IMAGEM_BYTES + 1024),
            content_type='image/png'
        )
        with self.assertRaises(ValidationError):
            validar_tamanho_imagem(arquivo_gigante)

    def test_arquivo_extensao_falsa_rejeitado(self):
        """Arquivo não-imagem com extensão permitida deve ser rejeitado pelo Pillow."""
        falso_jpg = SimpleUploadedFile('malicioso.jpg', b'conteudo falso que nao eh imagem', content_type='image/jpeg')
        with self.assertRaises(ValidationError):
            validar_formato_imagem(falso_jpg)

    def test_extensao_proibida_rejeitada(self):
        """Extensões de executáveis ou scripts devem ser imediatamente rejeitadas."""
        script_exe = SimpleUploadedFile('programa.exe', b'executavel', content_type='application/octet-stream')
        with self.assertRaises(ValidationError):
            validar_formato_imagem(script_exe)


class NucleoAdminTests(TestCase):
    """Testes de acesso ao painel administrativo."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin_teste', 'admin@teste.com', 'SenhaForte123!')
        self.client.force_login(self.admin_user)

    def test_admin_configuracao_site_acessivel(self):
        """Painel de ConfiguracaoSite deve responder para superusuário."""
        ConfiguracaoSite.objects.create(nome_instituto="Instituto Mente em Foco")
        response = self.client.get('/admin/nucleo/configuracaosite/')
        self.assertEqual(response.status_code, 200)

    def test_admin_profissional_acessivel(self):
        """Painel de Profissional deve responder para superusuário."""
        response = self.client.get('/admin/nucleo/profissional/')
        self.assertEqual(response.status_code, 200)
