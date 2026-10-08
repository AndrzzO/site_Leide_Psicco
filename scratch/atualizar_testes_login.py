from pathlib import Path
p=Path('nucleo/tests_rate_limit.py');s=p.read_text(encoding='utf-8-sig'); start=s.index('class TestRateLimitAdminLogin'); end=s.index('class TestIdentificacaoOrigemEProxy',start); s=s[:start]+'''class TestRateLimitAdminLogin(TestCase):
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


'''+s[end:];p.write_text(s,encoding='utf-8')
