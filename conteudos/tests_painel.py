from datetime import timedelta
from unittest.mock import patch
from io import StringIO
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from nucleo.models import BloqueioLogin
from nucleo.rate_limit import gerar_digest_origem
from nucleo.sitemaps import ConteudosSitemap, CategoriasSitemap
from .models import Artigo, CategoriaArtigo
from .painel_forms import ArtigoEditorForm


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class PainelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('autora@example.com', password='SenhaTeste123!')
        self.user.user_permissions.add(Permission.objects.get(codename='gerenciar_blog'))
        self.login_url = reverse('painel:login')
        self.dados = {'titulo': 'Um novo olhar', 'resumo': 'Uma reflexão.', 'conteudo': '<p>Texto da autora.</p>', 'fonte': 'georgia', 'permanencia': 'permanente', 'acao': 'publicar'}

    def test_login_email_case_insensitive_e_permissao(self):
        self.assertEqual(self.client.post(self.login_url, {'username': 'AUTORA@EXAMPLE.COM', 'password': 'SenhaTeste123!'}).status_code, 302)
        self.assertEqual(self.client.get(reverse('painel:index')).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)
        self.assertFalse(self.user.is_staff)

    def test_sem_permissao_nao_edita(self):
        artigo = Artigo.objects.create(titulo='Privado')
        for route in [reverse('painel:index'), reverse('painel:novo'), reverse('painel:editar', args=[artigo.pk]), reverse('painel:excluir', args=[artigo.pk])]:
            self.assertEqual(self.client.get(route).status_code, 302)
        outro = get_user_model().objects.create_user('outro', password='senha')
        self.client.force_login(outro)
        self.assertEqual(self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados).status_code, 403)

    def test_publicar_editar_rascunho_e_excluir(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('painel:novo'), self.dados)
        self.assertEqual(r.status_code, 302)
        artigo = Artigo.objects.get()
        self.assertEqual(artigo.fonte, 'georgia')
        self.assertTrue(artigo.formato_html)
        self.assertContains(self.client.get(artigo.get_absolute_url()), 'fonte-georgia')
        self.assertContains(self.client.get(artigo.get_absolute_url()), '<p>Texto da autora.</p>', html=True)
        self.dados.update(acao='rascunho', titulo='Novo título')
        self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados)
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(reverse('painel:excluir', args=[artigo.pk])).status_code, 200)
        self.assertTrue(Artigo.objects.exists())
        self.client.post(reverse('painel:excluir', args=[artigo.pk]))
        self.assertFalse(Artigo.objects.exists())

    def test_sanitizacao_fontes_e_hierarquia(self):
        form = ArtigoEditorForm({**self.dados, 'conteudo': '<h1>Título</h1><p style="font-size:99px" onclick="alert(1)">Texto</p><script>alert(2)</script><a href="javascript:alert(1)">Link</a>'})
        self.assertTrue(form.is_valid(), form.errors)
        texto = form.cleaned_data['conteudo']
        for proibido in ['<h1', '<script', 'style=', 'onclick', 'javascript:']:
            self.assertNotIn(proibido, texto)
        form = ArtigoEditorForm({**self.dados, 'fonte': 'fonte-arbitraria'})
        self.assertFalse(form.is_valid())

    def test_expiracao_remove_de_todas_as_consultas_publicas_e_apaga(self):
        categoria = CategoriaArtigo.objects.create(nome='Teste')
        passado = timezone.now() - timedelta(seconds=1)
        artigo = Artigo.objects.create(titulo='Expirado', status='publicado', apagar_em=passado, categoria=categoria)
        permanente = Artigo.objects.create(titulo='Permanente', status='publicado')
        futuro = Artigo.objects.create(titulo='Futuro', status='publicado', apagar_em=timezone.now()+timedelta(days=1))
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('conteudos:index')), 'Expirado')
        self.assertNotIn(artigo, ConteudosSitemap().items())
        self.assertNotIn(categoria, CategoriasSitemap().items())
        call_command('apagar_artigos_expirados', stdout=StringIO())
        self.assertFalse(Artigo.objects.filter(pk=artigo.pk).exists())
        self.assertEqual(Artigo.objects.count(), 2)

    def test_data_invalida_e_permanente(self):
        for data in ['', '2020-01-01T12:00']:
            form = ArtigoEditorForm({**self.dados, 'permanencia': 'temporario', 'apagar_em': data})
            self.assertFalse(form.is_valid())
        form = ArtigoEditorForm({**self.dados, 'apagar_em': '2030-01-01T12:00'})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data['apagar_em'])

    def test_csrf_privacidade_logout_post(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.login_url, {}).status_code, 403)
        self.assertFalse(BloqueioLogin.objects.exists())
        self.client.force_login(self.user)
        r = self.client.get(reverse('painel:index'))
        self.assertIn('no-store', r.headers['Cache-Control'])
        self.assertIn('noindex', r.headers['X-Robots-Tag'])
        self.assertEqual(self.client.get(reverse('painel:sair')).status_code, 405)
        self.assertEqual(self.client.post(reverse('painel:sair')).status_code, 302)

    def test_progressao_compartilhada_e_permanente(self):
        agora = timezone.now()
        for nivel, horas in enumerate([2, 4, 8, 16, 32], start=1):
            with patch('nucleo.login_security.timezone.now', return_value=agora):
                for tentativa in range(10):
                    url = self.login_url if tentativa % 2 else reverse('admin:login')
                    r = self.client.post(url, {'username': 'inexistente@example.com', 'password': 'errada'})
                    self.assertEqual(r.status_code, 200 if tentativa < 9 else 404)
                registro = BloqueioLogin.objects.get()
                self.assertEqual(registro.nivel, nivel)
                self.assertEqual(registro.permanente, horas > 20)
                if horas <= 20:
                    self.assertEqual(registro.bloqueado_ate, agora + timedelta(hours=horas))
                for url in [self.login_url, reverse('admin:login')]:
                    self.assertEqual(self.client.get(url).status_code, 404)
            agora += timedelta(hours=horas, seconds=1)
        with patch('nucleo.login_security.timezone.now', return_value=agora+timedelta(days=999)):
            self.assertEqual(self.client.get(self.login_url).status_code, 404)
        call_command('desbloquear_login', '127.0.0.1', stdout=StringIO())
        self.assertEqual(self.client.get(self.login_url).status_code, 200)

    def test_reserva_impede_autenticacoes_simultaneas(self):
        BloqueioLogin.objects.create(origem=gerar_digest_origem('login', '127.0.0.1'), reserva_token='outra', reserva_ate=timezone.now()+timedelta(seconds=30))
        with patch('django.contrib.auth.forms.authenticate') as authenticate:
            self.assertEqual(self.client.post(self.login_url, {'username': self.user.username, 'password': 'errada'}).status_code, 404)
            authenticate.assert_not_called()
        self.assertEqual(BloqueioLogin.objects.get().falhas, 0)
        self.assertEqual(BloqueioLogin.objects.get().reserva_token, 'outra')

    def test_falha_banco_nao_libera_autenticacao(self):
        from django.db import OperationalError
        with patch('nucleo.login_security.BloqueioLogin.objects.filter', side_effect=OperationalError):
            self.assertEqual(self.client.post(self.login_url, {}).status_code, 503)

    def test_enquadramento_persiste_e_rejeita_valores_invalidos(self):
        self.client.force_login(self.user)
        self.client.post(reverse('painel:novo'), {**self.dados, 'capa_x': '0', 'capa_y': '83'})
        artigo = Artigo.objects.get()
        self.assertEqual((artigo.capa_x, artigo.capa_y), (0, 83))
        form = ArtigoEditorForm(instance=artigo)
        self.assertEqual(form['capa_y'].value(), 83)
        for valor in ['-1', '101', '50; color:red', 'abc']:
            form = ArtigoEditorForm({**self.dados, 'capa_x': valor})
            self.assertFalse(form.is_valid())
        self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados)
        artigo.refresh_from_db()
        self.assertEqual((artigo.capa_x, artigo.capa_y), (0, 83))

    def test_painel_nao_oferece_link_para_artigo_expirado_e_permite_republicar(self):
        self.client.force_login(self.user)
        artigo = Artigo.objects.create(titulo='Prazo terminado', status='publicado', apagar_em=timezone.now()-timedelta(days=1))
        response = self.client.get(reverse('painel:index'))
        self.assertContains(response, 'Expirado')
        self.assertNotContains(response, 'Ver no site')
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 404)
        self.client.post(reverse('painel:editar', args=[artigo.pk]), self.dados)
        artigo.refresh_from_db()
        self.assertIsNone(artigo.apagar_em)
        self.assertContains(self.client.get(reverse('painel:index')), 'Ver no site')
        self.assertEqual(self.client.get(artigo.get_absolute_url()).status_code, 200)

    def test_situacao_publica_respeita_agendamento_e_categoria(self):
        categoria = CategoriaArtigo.objects.create(nome='Oculta', ativo=False)
        artigo = Artigo.objects.create(titulo='Teste de situação', status='publicado', categoria=categoria)
        self.assertFalse(artigo.visivel_no_site)
        self.assertEqual(artigo.situacao_publica, 'Categoria inativa')
        artigo.categoria = None
        artigo.data_publicacao = timezone.now()+timedelta(days=1)
        self.assertEqual(artigo.situacao_publica, 'Agendado')
        self.assertFalse(artigo.visivel_no_site)
