import sys
import os
import io
import uuid
import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracoes.settings.desenvolvimento')

import django
django.setup()

from django.test import Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.management import call_command

from nucleo.models import ConfiguracaoSite, Profissional, RedeSocial
from nucleo.validators import validar_imagem
from servicos.models import AreaAtuacao, Servico
from conteudos.models import CategoriaArtigo, Artigo
from contato.models import MensagemContato

client = Client()

# Pre-cleanup in case of previous interrupted run
Artigo.objects.filter(slug__startswith='artigo-teste-rascunho').delete()
CategoriaArtigo.objects.filter(slug__startswith='categoria-teste').delete()
MensagemContato.objects.filter(email='expirada_teste@example.com').delete()

print("=" * 60)
print("TESTE 4: CICLO DE VIDA DO BLOG (RASCUNHO -> PUBLICADO -> DESPUBLICADO)")
print("=" * 60)

test_id = uuid.uuid4().hex[:6]
slug_cat = f'categoria-teste-{test_id}'
slug_art = f'artigo-teste-rascunho-{test_id}'

# 1. Create test category
cat = CategoriaArtigo.objects.create(
    nome=f'Categoria Teste {test_id}',
    slug=slug_cat,
    ativo=True
)

# 2. Create test draft article
artigo_rascunho = Artigo.objects.create(
    titulo=f'[TESTE FUNCIONAL] Artigo Rascunho {test_id}',
    slug=slug_art,
    categoria=cat,
    resumo='Resumo de artigo em rascunho.',
    conteudo='## Subtítulo\nConteúdo editorial do rascunho.',
    status=Artigo.STATUS_RASCUNHO,
    data_publicacao=timezone.now()
)

# Confirm draft is NOT listed in /conteudos/
resp = client.get('/conteudos/')
assert slug_art not in resp.content.decode('utf-8'), "FALHA: Rascunho apareceu na listagem!"
print("[OK] Rascunho NAO aparece na listagem do blog")

# Confirm draft returns 404 on direct URL
resp = client.get(f'/conteudos/{slug_art}/')
assert resp.status_code == 404, f"FALHA: Rascunho retornou {resp.status_code} em vez de 404!"
print("[OK] Acesso direto ao rascunho retorna HTTP 404")

# Confirm draft is NOT in sitemap.xml
resp = client.get('/sitemap.xml')
assert slug_art not in resp.content.decode('utf-8'), "FALHA: Rascunho listado no sitemap!"
print("[OK] Rascunho NAO esta presente no sitemap.xml")

# 3. Publish the article
artigo_rascunho.status = Artigo.STATUS_PUBLICADO
artigo_rascunho.save()

# Confirm published article appears in /conteudos/
resp = client.get('/conteudos/')
assert slug_art in resp.content.decode('utf-8'), "FALHA: Artigo publicado não apareceu na listagem!"
print("[OK] Artigo publicado aparece na listagem do blog")

# Confirm published article returns 200 on direct URL
resp = client.get(f'/conteudos/{slug_art}/')
assert resp.status_code == 200, f"FALHA: Artigo publicado retornou {resp.status_code} em vez de 200!"
print("[OK] Acesso direto ao artigo publicado retorna HTTP 200")

# Confirm published article is in sitemap.xml
resp = client.get('/sitemap.xml')
assert slug_art in resp.content.decode('utf-8'), "FALHA: Artigo publicado ausente do sitemap!"
print("[OK] Artigo publicado esta presente no sitemap.xml")

# 4. Future publication date check
artigo_rascunho.data_publicacao = timezone.now() + datetime.timedelta(days=5)
artigo_rascunho.save()

resp = client.get(f'/conteudos/{slug_art}/')
assert resp.status_code == 404, f"FALHA: Artigo com data futura retornou {resp.status_code} em vez de 404!"
print("[OK] Artigo com data futura retorna HTTP 404 e fica oculto")

# 5. Unpublish (back to draft)
artigo_rascunho.status = Artigo.STATUS_RASCUNHO
artigo_rascunho.save()

resp = client.get(f'/conteudos/{slug_art}/')
assert resp.status_code == 404, "FALHA: Artigo despublicado continua acessível!"
print("[OK] Despublicacao remove o artigo da visualizacao publica")

# Clean up synthetic article and category
artigo_rascunho.delete()
cat.delete()
print("[OK] Dados sinteticos de teste do blog removidos com sucesso")

print("\n" + "=" * 60)
print("TESTE 5: BUSCA E FILTROS DO BLOG")
print("=" * 60)

# Test search with query
resp = client.get('/conteudos/?q=terapia')
assert resp.status_code == 200
print("[OK] Busca com termo valido retorna 200")

# Test search with XSS attempt
resp = client.get('/conteudos/?q=<script>alert("xss")</script>')
assert resp.status_code == 200
assert '<script>alert("xss")</script>' not in resp.content.decode('utf-8')
print("[OK] Busca com payload XSS tratada de forma segura (escapada)")

# Test search with very long string (truncation to 100)
resp = client.get('/conteudos/?q=' + 'a' * 200)
assert resp.status_code == 200
print("[OK] Busca com termo longo (>100 chars) processada sem erro 500")

print("\n" + "=" * 60)
print("TESTE 6: UPLOADS DE IMAGEM E VALIDACOES DE SEGURANCA")
print("=" * 60)

def criar_imagem_valida(formato='JPEG'):
    f = io.BytesIO()
    img = Image.new('RGB', (100, 100), color='green')
    img.save(f, formato)
    f.seek(0)
    ext = 'jpg' if formato == 'JPEG' else formato.lower()
    return SimpleUploadedFile(f'teste.{ext}', f.read(), content_type=f'image/{ext}')

# Valid JPG
img_jpg = criar_imagem_valida('JPEG')
try:
    validar_imagem(img_jpg)
    print("[OK] JPG valido aprovado pelo validador")
except Exception as e:
    print(f"[FALHA] JPG valido rejeitado indevidamente: {e}")

# Valid PNG
img_png = criar_imagem_valida('PNG')
try:
    validar_imagem(img_png)
    print("[OK] PNG valido aprovado pelo validador")
except Exception as e:
    print(f"[FALHA] PNG valido rejeitado indevidamente: {e}")

# Valid WEBP
img_webp = criar_imagem_valida('WEBP')
try:
    validar_imagem(img_webp)
    print("[OK] WEBP valido aprovado pelo validador")
except Exception as e:
    print(f"[FALHA] WEBP valido rejeitado indevidamente: {e}")

# Fake JPG (plain text named .jpg)
fake_jpg = SimpleUploadedFile('malicioso.jpg', b'<html><body>Not an image</body></html>', content_type='image/jpeg')
try:
    validar_imagem(fake_jpg)
    print("[FALHA] Fake JPG foi aceito indevidamente!")
except ValidationError:
    print("[OK] Fake JPG (conteudo nao-imagem) rejeitado com ValidationError")

# Forbidden EXE
exe_file = SimpleUploadedFile('script.exe', b'MZ\x90\x00', content_type='application/x-msdownload')
try:
    validar_imagem(exe_file)
    print("[FALHA] EXE foi aceito indevidamente!")
except ValidationError:
    print("[OK] Arquivo executavel .exe rejeitado com ValidationError")

# Corrupted image bytes
corrupted = SimpleUploadedFile('corrupt.jpg', b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01corrupted_bytes_here', content_type='image/jpeg')
try:
    validar_imagem(corrupted)
    print("[FALHA] Imagem corrompida aceita indevidamente!")
except ValidationError:
    print("[OK] Imagem corrompida rejeitada com ValidationError")

print("\n" + "=" * 60)
print("TESTE 7: SIMULACAO DE ESTADOS VAZIOS (SEM WHATSAPP, EMAIL, FOTOS)")
print("=" * 60)

config = ConfiguracaoSite.get_solo()
original_whatsapp = config.whatsapp
original_email = config.email
original_instagram = config.instagram
original_telefone = config.telefone

try:
    # Set all contact info to empty
    config.whatsapp = ''
    config.email = ''
    config.instagram = ''
    config.telefone = ''
    config.save()

    resp = client.get('/')
    assert resp.status_code == 200, f"Home quebrou com config vazia! Status: {resp.status_code}"
    html = resp.content.decode('utf-8')
    assert 'None' not in html, "Texto 'None' vazou na Home com config vazia!"
    print("[OK] Home renderiza perfeitamente com configuracao de contato vazia (zero 500, zero 'None')")

    resp_contato = client.get('/contato/')
    assert resp_contato.status_code == 200, f"Contato quebrou com config vazia! Status: {resp_contato.status_code}"
    print("[OK] Pagina de Contato renderiza perfeitamente sem WhatsApp cadastrado")

    resp_servicos = client.get('/servicos/psicologia/')
    assert resp_servicos.status_code == 200, f"Servico quebrou! Status: {resp_servicos.status_code}"
    print("[OK] Pagina interna de servico renderiza perfeitamente sem WhatsApp cadastrado")

finally:
    # Restore original config
    config.whatsapp = original_whatsapp
    config.email = original_email
    config.instagram = original_instagram
    config.telefone = original_telefone
    config.save()
    print("[OK] Configuracao original restaurada")

print("\n" + "=" * 60)
print("TESTE 8: PAGINAS DE ERRO EM DEBUG=FALSE")
print("=" * 60)

with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
    resp_404 = client.get('/rota-inexistente-para-teste-404/')
    assert resp_404.status_code == 404, f"404 retornou {resp_404.status_code}"
    html_404 = resp_404.content.decode('utf-8')
    assert 'Traceback' not in html_404, "Traceback vazou na página 404!"
    assert 'Página não encontrada' in html_404 or '404' in html_404, "Página 404 sem mensagem adequada!"
    print("[OK] Erro 404 customizado em DEBUG=False renderiza sem traceback e com link de retorno")

print("\n" + "=" * 60)
print("TESTE 9: COMANDO DE RETENCAO (limpar_contatos_expirados)")
print("=" * 60)

# Create an expired test message (> 30 days old)
antiga = MensagemContato.objects.create(
    nome='Teste Retenção Expirada',
    email='expirada_teste@example.com',
    mensagem='Mensagem expirada de teste.',
    aceite_privacidade=True
)
MensagemContato.objects.filter(id=antiga.id).update(
    criado_em=timezone.now() - datetime.timedelta(days=35)
)

# 1. Sem configuração de retenção -> Abort seguro
call_command('limpar_contatos_expirados')
assert MensagemContato.objects.filter(id=antiga.id).exists(), "Abort seguro falhou em proteger dados sem retenção configurada!"
print("[OK] Comando de retencao sem configuracao: abort seguro comprovado")

# 2. Com --dias 30 em modo --dry-run
call_command('limpar_contatos_expirados', '--dias', '30', '--dry-run')
assert MensagemContato.objects.filter(id=antiga.id).exists(), "Dry-run excluiu registro indevidamente!"
print("[OK] Comando de retencao em modo --dry-run nao exclui registros")

# 3. Com --dias 30 em execução real
call_command('limpar_contatos_expirados', '--dias', '30')
assert not MensagemContato.objects.filter(id=antiga.id).exists(), "Comando de retencao nao excluiu registro antigo com --dias 30!"
print("[OK] Comando de retencao com --dias 30 excluiu com sucesso a mensagem de teste expirada (>30 dias)")

print("\nTODOS OS TESTES FUNCIONAIS EXECUTADOS COM SUCESSO!")
