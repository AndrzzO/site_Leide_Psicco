from urllib.parse import urlsplit, parse_qs
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from contato.models import MensagemContato

class WhatsAppFormularioTests(TestCase):
    @patch('contato.views.RateLimiter.verificar_contato', return_value=(True, 0))
    @patch('nucleo.context_processors.dados_institucionais', return_value={'WHATSAPP_LINK': 'https://wa.me/5561993147966?text=padrao'})
    def test_mensagem_preenchida_e_codificada(self, contexto, limite):
        response = self.client.post(reverse('contato:index'), {'nome':'Ana Silva', 'email':'ana@example.com', 'telefone':'61999998888', 'mensagem':'Olá! Quero informações & horários.', 'aceite_privacidade':'on', 'destino':'whatsapp'})
        self.assertEqual(response.status_code, 200)
        url = urlsplit(response.context['whatsapp_destino'])
        self.assertEqual(url.netloc, 'wa.me')
        self.assertEqual(url.path, '/5561993147966')
        texto = parse_qs(url.query)['text'][0]
        self.assertEqual(texto, 'Olá Dra. Marileide, me chamo Ana Silva.\n\nQuero saber mais a respeito dos seus atendimentos.\n\nOlá! Quero informações & horários.\n\nTelefone: 61999998888\nE-mail: ana@example.com')
        self.assertFalse(MensagemContato.objects.exists())
        self.assertIn('no-store', response.headers['Cache-Control'])

    @patch('contato.views.RateLimiter.verificar_contato', return_value=(True, 0))
    def test_invalido_nao_redireciona_whatsapp(self, limite):
        r = self.client.post(reverse('contato:index'), {'nome':'Ana Silva', 'destino':'whatsapp'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['form'].errors)
