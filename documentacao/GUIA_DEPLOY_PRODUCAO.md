# Guia Prático de Deploy em Produção (Provider-Agnostic)
**Projeto:** Instituto Mente em Foco  
**Data:** 28/09/2026  
**Stack:** Django 6.0.8 | Python 3.14.5 | PostgreSQL | WSGI | Nginx/PaaS Proxy  
**Objetivo:** Roteiro passo a passo, seguro e determinístico para o primeiro deploy e futuras releases da aplicação.

---

## 1. Princípios Operacionais Inegociáveis

1. **Nunca use `runserver` em Produção:** Sempre utilize um servidor WSGI profissional (ex: Gunicorn).
2. **Nunca realize migrations diretamente em produção sem testar antes:** Todas as migrations devem estar commitadas, testadas e validadas com `makemigrations --check`.
3. **Nunca crie superusuários com credenciais fixas no código:** Utilize `python manage.py createsuperuser` interativo em sessão segura.
4. **Nunca ative indexação (`SEO_ALLOW_INDEXING=True`) antes da validação final:** O site só deve ser indexado após domínio canônico, HTTPS e fotos estarem aprovados.

---

## 2. Preparação do Ambiente de Execução

### Passo 2.1 — Seleção do Commit Aprovado
Garanta que a branch de release (ex: `main`) esteja limpa e com todos os 232 testes unitários aprovados:
```bash
git checkout main
git pull origin main
git status
```

### Passo 2.2 — Configuração das Variáveis de Ambiente
No painel da plataforma de deploy (ou arquivo `.env` seguro no servidor com permissões `600`), configure as seguintes variáveis essenciais (consulte `MATRIZ_VARIAVEIS_AMBIENTE.md`):

```bash
# Ambiente e Segurança
DJANGO_SETTINGS_MODULE=configuracoes.settings.producao
DJANGO_SECRET_KEY=sua_chave_criptografica_unica_com_mais_de_50_caracteres
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=menteemfoco.com.br,www.menteemfoco.com.br
DJANGO_CSRF_TRUSTED_ORIGINS=https://menteemfoco.com.br,https://www.menteemfoco.com.br

# Banco de Dados PostgreSQL
DATABASE_URL=postgres://usuario_app:senha_forte@host_postgre:5432/mente_foco_prod

# Rota Administrativa Opcional
DJANGO_ADMIN_URL=gestao-clinica/

# Segurança HTTPS e Proxy Reverso
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_PROXY_SSL_HEADER=True
TRUST_PROXY_CLIENT_IP=True

# SEO e Domínio Canônico
SITE_URL=https://menteemfoco.com.br
SEO_ALLOW_INDEXING=False

# Dados Institucionais (conforme definição oficial da cliente)
WHATSAPP_NUMERO=5561999999999
EMAIL_CONTATO=contato@menteemfoco.com.br
CRP_PROFISSIONAL=CRP 01/12345
```

---

## 3. Procedimento de Build e Deploy

### Passo 3.1 — Instalação das Dependências do Projeto
No ambiente virtual de produção (Linux), instale os pacotes e o driver PostgreSQL (`psycopg` v3):
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install "psycopg[binary]>=3.2,<4.0"
pip check
```

### Passo 3.2 — Teste de Conectividade e Validação de Migrações
Antes de aplicar qualquer alteração no banco de dados:
```bash
# 1. Verifica consistência estrutural do Django
python manage.py check

# 2. Confirma que não há migrações pendentes de geração
python manage.py makemigrations --check

# 3. Inspeciona o histórico e o plano de migrações
python manage.py showmigrations
python manage.py migrate --plan
```

### Passo 3.3 — Backup Preventivo do Banco de Dados (Releases Futuras)
Se o banco já possuir dados reais (artigos do blog, configurações ou mensagens de contato), realize um snapshot ou dump antes de migrar:
```bash
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -Fc -f "/backups/mente_foco_pre_deploy_$(date +%Y%m%d_%H%M%S).dump"
```

### Passo 3.4 — Aplicação das Migrações
Execute a sincronização do schema no banco PostgreSQL:
```bash
python manage.py migrate --noinput
```

### Passo 3.5 — Coleta de Arquivos Estáticos (Collectstatic)
Colete todos os ativos visuais (CSS, JavaScript, fontes, ícones) para a pasta `staticfiles/`:
```bash
python manage.py collectstatic --noinput --clear
```

---

## 4. Inicialização do Servidor de Aplicação

Execute o servidor WSGI (Gunicorn) apontando para o módulo do projeto:
```bash
gunicorn configuracoes.wsgi:application \
    --workers 3 \
    --threads 2 \
    --bind 0.0.0.0:8000 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

---

## 5. Roteiro de Validação e Smoke Test Pós-Deploy

Após o serviço iniciar, execute a verificação imediata:

1. **Sonda de Liveness (Saúde da Aplicação):**
   ```bash
   curl -I https://menteemfoco.com.br/health/
   # Esperado: HTTP/1.1 200 OK | Corpo: OK | Header: X-Robots-Tag: noindex, nofollow
   ```

2. **Sonda de Readiness (Conectividade com PostgreSQL):**
   ```bash
   curl -I https://menteemfoco.com.br/health/ready/
   # Esperado: HTTP/1.1 200 OK | Corpo: OK | Header: X-Robots-Tag: noindex, nofollow
   ```

3. **Validação de Headers de Segurança:**
   ```bash
   curl -I https://menteemfoco.com.br/
   # Confirmar presença de:
   # X-Content-Type-Options: nosniff
   # X-Frame-Options: DENY
   # Referrer-Policy: strict-origin-when-cross-origin
   # Content-Security-Policy (CSP)
   ```

4. **Navegação nas Páginas Principais:**
   - Acesse via navegador: `/`, `/sobre-mim/`, `/servicos/psicologia/`, `/servicos/neuropsicologia/`, `/conteudos/`, `/contato/`, `/politica-de-privacidade/`.
   - Abra a aba Rede (Network) e Console do DevTools: confirme **zero erro 404 de static**, **zero violação de CSP** e **zero erro 500**.

5. **Acesso Administrativo Seguro:**
   - Acesse a rota administrativa configurada em `DJANGO_ADMIN_URL`.
   - Crie o superusuário oficial da clínica:
     ```bash
     python manage.py createsuperuser
     ```
   - Realize login e verifique a interface do painel.

6. **Teste de Submissão do Formulário de Contato:**
   - Realize uma submissão autorizada de teste pelo formulário `/contato/`.
   - Acesse o Admin e confirme que o registro foi gravado na tabela `MensagemContato`.
   - Exclua o registro de teste pelo painel após validação.

---

## 6. Procedimento de Go-Live (Abertura Pública e Indexação)

Somente após **TODAS** as pendências do cliente estarem resolvidas (fotos definitivas, CRP, aprovação jurídica e domínio oficial):

1. Altere a variável de ambiente:
   ```bash
   SEO_ALLOW_INDEXING=True
   ```
2. Reinicie a aplicação:
   ```bash
   # O robots.txt passará a permitir o rastreamento público (Allow: /)
   # e o sitemap.xml será disponibilizado aos buscadores.
   ```
3. Submeta o `https://menteemfoco.com.br/sitemap.xml` no Google Search Console e Bing Webmaster Tools.
4. Inicie o plano de monitoramento das primeiras 24 horas (consulte `CHECKLIST_GO_LIVE.md`).
