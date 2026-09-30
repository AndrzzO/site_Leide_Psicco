import sys
import os
import re

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracoes.settings.desenvolvimento')

import django
django.setup()

from django.test import Client
from django.conf import settings

client = Client()

print("=" * 60)
print("1. VERIFICANDO ROTAS DE LOGIN/SIGNUP PÚBLICO INESPERADAS")
print("=" * 60)

for url in ['/login/', '/signup/', '/register/', '/account/', '/profile/']:
    resp = client.get(url)
    print(f"GET {url:<20} -> {resp.status_code} (esperado 404 para rota pública inexistente)")

print("\n" + "=" * 60)
print("2. TESTANDO ADMIN LOGIN E PROTEÇÃO DE ACESSO")
print("=" * 60)

admin_url = '/' + settings.DJANGO_ADMIN_URL.strip('/') + '/'
resp = client.get(admin_url)
print(f"GET {admin_url:<20} -> {resp.status_code} (302 para login esperado para anônimo)")
if resp.status_code == 302:
    print(f"  Redirect location: {resp.headers.get('Location')}")

login_url = admin_url + 'login/'
resp = client.get(login_url)
print(f"GET {login_url:<20} -> {resp.status_code} (200 esperado)")

print("\n" + "=" * 60)
print("3. TESTANDO CONTATO FORM GET & VALID/INVALID POST")
print("=" * 60)

resp = client.get('/contato/')
print(f"GET /contato/ -> {resp.status_code}")

# Valid POST
post_data = {
    'nome': 'Usuário Teste Auditoria',
    'email': 'teste_audit@example.com',
    'telefone': '61999999999',
    'mensagem': 'Mensagem de teste automatizado para auditoria funcional.',
    'servico_interesse': '',
    'aceite_privacidade': 'on',
    'campo_verificacao': '', # honeypot empty
}
resp_post = client.post('/contato/', post_data, follow=False)
print(f"POST válido /contato/ -> {resp_post.status_code} (Redirect esperado: 302)")
if resp_post.status_code == 302:
    print(f"  Redirect para: {resp_post.headers.get('Location')}")
    resp_redirect = client.get(resp_post.headers.get('Location'))
    print(f"  GET após redirect -> {resp_redirect.status_code}")

# Invalid POST (missing email and phone)
bad_data = {
    'nome': 'Usuário Sem Contato',
    'email': '',
    'telefone': '',
    'mensagem': 'Mensagem sem contato.',
    'aceite_privacidade': 'on',
    'campo_verificacao': '',
}
resp_bad = client.post('/contato/', bad_data, follow=False)
print(f"POST inválido /contato/ -> {resp_bad.status_code} (200 esperado com erros)")
if hasattr(resp_bad, 'context') and resp_bad.context and 'form' in resp_bad.context:
    print(f"  Erros do formulário: {resp_bad.context['form'].errors.as_json()}")

# Clean up synthetic contact created during test
from contato.models import MensagemContato
deleted, _ = MensagemContato.objects.filter(email='teste_audit@example.com').delete()
print(f"Limpeza de contatos sintéticos: {deleted} registros removidos.")
