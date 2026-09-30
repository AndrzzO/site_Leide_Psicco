"""Regressões do reposicionamento editorial, sem alterar fluxos de contato."""
from django.test import TestCase, override_settings
from django.core.cache import cache
from django.urls import reverse
from contato.models import MensagemContato
from servicos.editorial import AVALIACOES


class ReformulacaoEditorialTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_seis_paginas_distintas_e_slug_desconhecido(self):
        titles, descriptions, introductions = set(), set(), set()
        for item in AVALIACOES:
            response = self.client.get(reverse('servicos:avaliacao_especifica', kwargs={'slug': item['slug']}))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, item['h1'])
            self.assertContains(response, 'Solicitar avaliação psicológica')
            self.assertContains(response, item['faq'][0][0])
            titles.add(response.context['titulo_pagina'])
            descriptions.add(response.context['meta_descricao'])
            introductions.add(item['intro'])
        self.assertEqual(len(titles), 6)
        self.assertEqual(len(descriptions), 6)
        self.assertEqual(len(introductions), 6)
        self.assertEqual(self.client.get('/servicos/avaliacao/inexistente/').status_code, 404)

    def test_contato_preserva_finalidade_sem_aceitar_texto_arbitrario(self):
        for assunto in ['burnout', 'inss', 'credenciamento', 'psicoterapia']:
            response = self.client.get('/contato/', {'assunto': assunto})
            self.assertTrue(response.context['form'].initial['mensagem'])
        response = self.client.get('/contato/', {'assunto': '<script>alert(1)</script>'})
        self.assertEqual(response.context['form'].initial['mensagem'], '')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_interesse_credenciamento_usa_fluxo_existente(self):
        response = self.client.get('/credenciamento/')
        self.assertContains(response, 'action="/contato/?assunto=credenciamento"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'aceite_privacidade')
        response = self.client.post('/contato/?assunto=credenciamento', {
            'nome': 'Profissional de Teste',
            'email': 'profissional@example.com',
            'mensagem': 'Tenho interesse no credenciamento de psicólogos.',
            'aceite_privacidade': 'on',
            'campo_verificacao': '',
        })
        self.assertRedirects(response, reverse('contato:index'))
        self.assertEqual(MensagemContato.objects.count(), 1)
        self.assertIn('credenciamento', MensagemContato.objects.get().mensagem)

    def test_interesse_invalido_mostra_erros_e_preserva_mensagem(self):
        response = self.client.post('/contato/?assunto=credenciamento', {
            'nome': 'Profissional de Teste',
            'mensagem': 'Tenho interesse no credenciamento de psicólogos.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tenho interesse no credenciamento')
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(MensagemContato.objects.count(), 0)

    def test_sitemap_inclui_novas_paginas(self):
        from nucleo.sitemaps import AvaliacoesEspecificasSitemap, PaginasSitemap
        sitemap = AvaliacoesEspecificasSitemap()
        self.assertEqual(len(sitemap.items()), 6)
        for slug in sitemap.items():
            self.assertEqual(self.client.get(sitemap.location(slug)).status_code, 200)
        self.assertIn('/credenciamento/', [PaginasSitemap().location(i) for i in PaginasSitemap().items()])

