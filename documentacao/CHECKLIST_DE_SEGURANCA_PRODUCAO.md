# CHECKLIST DE SEGURANÇA E HARDENING PARA PRODUÇÃO
## Instituto Mente em Foco
### Guia Obrigatório de Homologação Pré-Deploy

Este checklist deve ser integralmente validado pela equipe técnica e de infraestrutura antes da publicação definitiva do site no ambiente de produção.

---

## 1. Verificações Críticas de Ambiente e Configuração

- [ ] **DEBUG Desativado:** Confirmar que `DJANGO_DEBUG=False` está ativo nas variáveis do servidor de produção. A aplicação deve recusar inicializar com `DEBUG=True` em produção.
- [ ] **SECRET_KEY Exclusiva:** Chave criptográfica única, longa (> 50 caracteres) e gerada aleatoriamente, sem qualquer valor conhecido ou prefixo `django-insecure`.
- [ ] **ALLOWED_HOSTS Real:** Configurada explicitamente com o domínio oficial (ex: `institutomenteemfoco.com.br,www.institutomenteemfoco.com.br`), sem wildcard `*`.
- [ ] **CSRF_TRUSTED_ORIGINS Real:** Configurada com o esquema HTTPS completo (ex: `https://institutomenteemfoco.com.br,https://www.institutomenteemfoco.com.br`).
- [ ] **DATABASE_URL Segura:** Conexão com PostgreSQL gerenciado em nuvem, utilizando canal criptografado SSL/TLS.
- [ ] **Django Admin Customizado:** Rota administrativa definida via `DJANGO_ADMIN_URL` diferente de caminhos padrão e ausente de `robots.txt` e `sitemap.xml`.

---

## 2. HTTPS, Proxy e Certificados

- [ ] **HTTPS Funcional:** Certificado TLS válido (Let's Encrypt, Cloudflare ou Provedor de Nuvem) sem erros de expiração ou autoridade emissora.
- [ ] **Redirecionamento SSL:** `DJANGO_SECURE_SSL_REDIRECT=True` forçando todo o tráfego HTTP para HTTPS.
- [ ] **Reverse Proxy Validado:** Se a aplicação estiver atrás de Nginx, Caddy, Render, Railway ou AWS ALB com terminação TLS, validar se `DJANGO_SECURE_PROXY_SSL_HEADER=True` é aplicável e se os cabeçalhos do cliente não podem ser forjados.
- [ ] **Cookies Seguros:** Validar em navegador que os cookies `sessionid` e `csrftoken` possuem os atributos `Secure`, `HttpOnly` (para sessão) e `SameSite=Lax`.

---

## 3. Política HSTS (HTTP Strict Transport Security)

- [ ] **Fase 1 (Teste Inicial):** Após confirmação do HTTPS, ativar `DJANGO_SECURE_HSTS_SECONDS=300` (5 minutos) e navegar por todas as páginas.
- [ ] **Fase 2 (Estabilização):** Caso não haja nenhum erro de certificado ou recursos quebrados, aumentar para `DJANGO_SECURE_HSTS_SECONDS=86400` (1 dia).
- [ ] **Fase 3 (Produção Longa):** Após homologação de 7 dias sem intercorrências, definir `DJANGO_SECURE_HSTS_SECONDS=31536000` (1 ano).
- [ ] **HSTS Preload:** Apenas habilitar `DJANGO_SECURE_HSTS_PRELOAD=True` e submeter ao HSTS Preload List após decisão gerencial consciente e confirmação de que todos os subdomínios suportam HTTPS de forma perpétua.

---

## 4. Content Security Policy (CSP) e Cabeçalhos Defensivos

- [ ] **CSP Enforcement Testada:** Confirmar que `Content-Security-Policy` está sendo emitido sem erros indevidos no console do navegador (DevTools > Console).
- [ ] **Permissão de Fontes:** Google Fonts (`fonts.googleapis.com` e `fonts.gstatic.com`) carregando normalmente sob a política.
- [ ] **Estrutura de JSON-LD:** Schemas institucionais e editoriais parseados e aprovados pelo Google Rich Results Test.
- [ ] **Django Admin sob CSP:** Testado login, changelist, edição de artigos e upload de imagens sem bloqueio de scripts ou formulários.
- [ ] **X-Frame-Options:** Confirmar presença do cabeçalho `X-Frame-Options: DENY`.
- [ ] **X-Content-Type-Options:** Confirmar presença do cabeçalho `nosniff`.
- [ ] **Permissions-Policy:** Confirmar restrição de APIs desnecessárias (`camera=(), microphone=(), geolocation=(), payment=(), usb=()`).
- [ ] **Cross-Origin-Opener-Policy (COOP):** Confirmar presença do cabeçalho `same-origin`.

---

## 5. Proteção de Dados, Privacidade e Formulários

- [ ] **Proteção CSRF Ativa:** Formulário de contato exige token CSRF e rejeita requisições forjadas com status 403.
- [ ] **Honeypot Ativo:** Campo armadilha oculto descarta submissões automáticas de spam sem persistir registros espúrios.
- [ ] **Sanitização de Markdown:** Artigos do Blog não executam tags `<script>`, `<iframe>` ou atributos maliciosos como `onerror`.
- [ ] **PII Protegida:** Parâmetros de formulário marcados com `@sensitive_post_parameters` e mensagens de contato fora de `list_display` do Admin.
- [ ] **Logs Limpos:** Zero senhas, zero tokens e zero dados pessoais completos gravados nos logs de produção.
- [ ] **Rotinas de Retenção LGPD:** Caso `CONTATO_RETENCAO_DIAS` esteja configurado, agendar execução diária do comando `limpar_contatos_expirados`.

---

## 6. Arquivos e Uploads

- [ ] **Uploads Seguros:** Apenas arquivos de imagem reais (`JPEG`, `PNG`, `WEBP`, `ICO`) validados via Pillow com tamanho máximo de 10 MB.
- [ ] **Media Files em Produção:** `MEDIA_URL` não servida pelo Django nativo em produção (`DEBUG=False`), utilizando storage de nuvem ou servidor web dedicado.
- [ ] **Arquivos Privados Fora da Webroot:** Diretórios `.git`, `.env`, arquivos de log e backups completamente fora do diretório público de arquivos estáticos.

---

## 7. Verificações Automatizadas

- [ ] **System Check Geral:** `python manage.py check` executado com zero erros.
- [ ] **Deploy Check:** `python manage.py check --deploy` revisado com sucesso.
- [ ] **Suíte de Testes:** `python manage.py test` com 234 testes passando (100% de sucesso).
- [ ] **Auditoria de Migrações:** `python manage.py makemigrations --check` com resultado `No changes detected`.
- [ ] **Auditoria de Pacotes:** `python -m pip check` com resultado `No broken requirements found`.

---

## 8. Proteção contra Abuso e Rate Limiting (Prompt 17)

- [ ] **Admin Login Rate Limit Testado:** Bloqueio de força bruta por IP (10 falhas/15 min) e Combo (5 falhas/15 min) validado.
- [ ] **Contato Rate Limit Testado:** Limite de 5 envios/15 min por origem verificado com retorno HTTP 429.
- [ ] **Client IP Definido pela Infraestrutura:** Validar se a aplicação recebe o IP real via `REMOTE_ADDR` ou se exige proxy.
- [ ] **Proxy Confiável Validado:** Caso utilize proxy reverso, definir `TRUST_PROXY_CLIENT_IP=True` somente após garantir que o proxy sobrescreve o cabeçalho `X-Forwarded-For`.
- [ ] **Backend de Cache de Produção Definido:** Homologar se a produção mono-processo utiliza `LocMemCache` ou se ambiente com múltiplos workers requer Redis/Memcached compartilhado.
- [ ] **Página de Erro 429 Testada:** Resposta HTTP 429 renderizada com template acessível, `Retry-After` e `Cache-Control: no-store`.
- [ ] **Spam Monitoring Definido:** Monitorar volume de descartes por honeypot e frequência de respostas 429 nos logs de produção.
- [ ] **Proteção Distribuída Revisada no Deploy:** Para mitigação volumétrica (DDoS), avaliar ativação de regras de limitação no Cloudflare WAF ou Nginx `limit_req`.

---

## 9. Health Checks e Observabilidade em Produção (Prompt 22)

- [ ] **Liveness Probe (`/health/`):** Retorna status 200 OK leve com `{"status": "ok"}` sem dependência de banco para checagem rápida do orquestrador.
- [ ] **Readiness Probe (`/health/ready/`):** Executa query leve (`SELECT 1`) e retorna HTTP 200 `{"status": "ready", "database": "connected"}` quando operacional, ou HTTP 503 `{"status": "unavailable", "database": "unavailable"}` em caso de indisponibilidade da base.
- [ ] **Proteção contra Indexação de Endpoints Internos:** Ambos os endpoints emitem `X-Robots-Tag: noindex, nofollow`.
- [ ] **Sigilo Operacional em Health Checks:** Em caso de erro 503, a resposta oculta estritamente detalhes de conexão, exceções internas, hosts ou stack traces.

---

## 10. Storages, Assets Estáticos e E-mail Transacional (Prompt 22)

- [ ] **STORAGES Moderno (Django 6.0):** Dicionário `STORAGES` explícito configurando separadamente `staticfiles` e `default` (mídia).
- [ ] **ManifestStaticFilesStorage em Produção:** Hash SHA-256 e cache perpétuo nos assets estáticos configurados via `DJANGO_MANIFEST_STATIC_STORAGE=True` (com salvaguarda para False em pipelines com hash externo).
- [ ] **Configuração SMTP Blindada:** Variáveis de envio transacional (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`) lidas do ambiente sem credenciais hardcoded.

