# Auditoria de Prontidão para Produção (Production Readiness Audit)
**Projeto:** Instituto Mente em Foco  
**Data da Auditoria:** 28/09/2026  
**Stack Técnica:** Python 3.14.5 | Django 6.0.8 | SQLite (Dev) / PostgreSQL (Target Prod) | Vanilla CSS & JS | Decouple  
**Status Geral:** Preparação Técnica Concluída — Pendente de Definições de Infraestrutura e Ativos do Cliente para Go-Live Público.

---

## 1. Sumário Executivo

Esta auditoria avalia a prontidão do projeto para transição do ambiente de **Desenvolvimento** para **Staging/Homologação** e **Produção**.
O princípio orientador é a **completa separação de ambientes e a parametrização agnóstica a provedor**: nenhum detalhe de infraestrutura (provedor cloud, CDN, banco gerenciado, SMTP, DNS) foi presumido ou amarrado de forma rígida ao código.

### Classificação de Prontidão:
- **Pronto para Deploy Técnico em Staging/Infraestrutura:** **SIM** (com as variáveis de ambiente corretas).
- **Pronto para Go-Live Público (Lançamento Oficial):** **NÃO (BLOQUEADO)** devido a pendências do cliente (fotografias definitivas, número de CRP oficial, dados de contato e domínio definitivo).

---

## 2. Matriz de Achados da Auditoria

| ID | Área | Estado Atual | Requisito de Produção | Risco | Severidade | Ação Necessária | Depende de Infra? | Bloqueia Go-Live? | Status |
|:---|:---|:---|:---|:---|:---|:---|:---:|:---:|:---:|
| **ACH-01** | **Settings** | `DEBUG=True` no desenvolvimento local. | `DEBUG=False` estrito em produção (`configuracoes.settings.producao`). | Vazamento de tracebacks e código-fonte em caso de erro 500. | **CRÍTICO** | Utilizar `DJANGO_SETTINGS_MODULE=configuracoes.settings.producao`. | Não | **SIM** | **RESOLVIDO NO CÓDIGO** |
| **ACH-02** | **Segurança** | `DJANGO_SECRET_KEY` de dev com prefixo `django-insecure`. | Chave criptográfica única, aleatória, com mais de 50 caracteres injetada via secret. | Quebra da integridade de sessões, CSRF e assinaturas criptográficas. | **CRÍTICO** | Injetar segredo via variáveis de ambiente da plataforma de deploy. O settings de prod já valida e rejeita chaves fracas. | Sim | **SIM** | **RESOLVIDO NO CÓDIGO** |
| **ACH-03** | **Domínio** | `DJANGO_ALLOWED_HOSTS` local (`localhost,127.0.0.1`). | Apenas domínios autorizados do Instituto (ex: `menteemfoco.com.br,www.menteemfoco.com.br`). | Ataques de Host Header Poisoning e redirecionamento malicioso. | **CRÍTICO** | Configurar domínios reais aprovados na variável `DJANGO_ALLOWED_HOSTS`. Wildcard `*` é bloqueado. | Sim | **SIM** | **PENDENTE DE INFRA** |
| **ACH-04** | **Banco** | SQLite local (`db.sqlite3`). | PostgreSQL gerenciado via `DATABASE_URL`. | Concorrência limitada, perda de dados em disco efêmero cloud. | **ALTO** | Provisionar PostgreSQL 15+ e configurar `DATABASE_URL=postgres://...`. | Sim | **SIM** | **PENDENTE DE INFRA** |
| **ACH-05** | **Driver DB** | `dj-database-url` instalado; `psycopg` não instalado localmente. | Driver PostgreSQL (`psycopg` v3) instalado no ambiente do servidor Linux. | Falha de inicialização da conexão com o banco relacional de produção. | **ALTO** | Incluir `psycopg[binary]>=3.2,<4.0` no buildpack/requirements de produção. | Sim | **SIM** | **PENDENTE DE DEPLOY** |
| **ACH-06** | **Media** | Armazenamento local em pasta `media/`. | Volume persistente montado ou Object Storage (S3/R2/GCS). | Perda imediata de fotos de artigos e profissionais ao reiniciar contêiner efêmero. | **CRÍTICO** | Definir infraestrutura de persistência (Volume ou Bucket) antes do lançamento. | Sim | **SIM** | **PENDENTE DE INFRA** |
| **ACH-07** | **Fotos** | Foto principal da Mari inserida no Hero; cards secundários utilizam placeholders SVG elegantes. | Fotografias institucionais reais completas da psicóloga e atendimentos. | Quebra de confiança editorial se forem publicados placeholders de desenvolvimento. | **ALTO** | Obter fotos definitivas da cliente e cadastrar via Django Admin. | Não | **SIM (VISUAL)** | **PENDENTE DO CLIENTE** |
| **ACH-08** | **Cadastros** | WhatsApp, e-mail e CRP como `PENDENTE_DEFINICAO`. | Informações oficiais reais revisadas. | Responsabilidade civil/ética perante o Conselho de Psicologia (CRP). | **CRÍTICO** | Preencher dados institucionais oficiais fornecidos pela psicóloga no `.env` ou painel. | Não | **SIM** | **PENDENTE DO CLIENTE** |
| **ACH-09** | **HTTPS** | `DJANGO_SECURE_SSL_REDIRECT=False` em desenvolvimento local. | `DJANGO_SECURE_SSL_REDIRECT=True` e terminação TLS válida no proxy/borda. | Tráfego de mensagens e credenciais em texto claro via HTTP inseguro. | **CRÍTICO** | Ativar certificado TLS/HTTPS na borda/provedor e ligar `DJANGO_SECURE_SSL_REDIRECT=True`. | Sim | **SIM** | **RESOLVIDO NO CÓDIGO** |
| **ACH-10** | **HSTS** | `SECURE_HSTS_SECONDS=0` (seguro para testes pré-deploy). | Rollout progressivo: 300s -> 86400s -> 31536000s após validação HTTPS. | Bloqueio inadvertido de acesso caso o domínio ou TLS falhe prematuramente. | **MÉDIO** | Manter 0 no dia 1; elevar para 300 no dia 2 e progredir conforme estabilidade. | Sim | Não | **RESOLVIDO NO CÓDIGO** |
| **ACH-11** | **Static** | `STATIC_ROOT = BASE_DIR / 'staticfiles'`, `collectstatic` validado com 143 arquivos. | Servir estáticos via Nginx, WhiteNoise ou CDN de borda. | Falha de carregamento de CSS, imagens institucionais e JavaScript. | **ALTO** | Definir se o servidor web (Nginx) ou storage servirá estáticos e rodar `collectstatic`. | Sim | **SIM** | **RESOLVIDO NO CÓDIGO** |
| **ACH-12** | **App Server** | Execução local via `manage.py runserver`. | Servidor WSGI de produção (Gunicorn / uWSGI) gerenciado por systemd ou container. | Queda de servidor, travamentos mono-thread, lentidão e instabilidade. | **CRÍTICO** | Proibir `runserver` em produção; configurar executor WSGI com workers proporcionais aos recursos. | Sim | **SIM** | **PENDENTE DE INFRA** |
| **ACH-13** | **Rate Limit** | Backend de cache padrão em memória (`LocMemCache`). | Cache compartilhado (Redis) OU proteção de rate limit na borda/WAF (Cloudflare/Nginx). | Rate limiting inconsistente entre múltiplos processos workers independentes. | **MÉDIO** | Se a infraestrutura tiver múltiplos workers, definir Redis ou rate limit no proxy reverso. | Sim | Não | **PENDENTE DE INFRA** |
| **ACH-14** | **E-mail** | Backend de e-mail local direcionado ao terminal (`console.EmailBackend`). | Servidor SMTP transacional autenticado (porta 587 TLS) ou API de envio. | Notificações de novos contatos não são enviadas para a caixa postal da psicóloga. | **MÉDIO** | Mensagens já são gravadas com segurança no banco; para e-mail, configurar credenciais SMTP. | Sim | Não | **PENDENTE DE INFRA** |
| **ACH-15** | **Health** | `/health/` (liveness) e `/health/ready/` (readiness de banco) criados com noindex. | Endpoints leves para health checks de orquestradores e monitoramento de uptime. | Indisponibilidade não detectada ou monitoramento quebrado por rate limit/autenticação. | **BAIXO** | Utilizar `/health/` e `/health/ready/` nos probes de monitoramento da plataforma. | Não | Não | **RESOLVIDO NO CÓDIGO** |
| **ACH-16** | **SEO Gate** | `SEO_ALLOW_INDEXING=False` por padrão no código. | `SEO_ALLOW_INDEXING=True` SOMENTE após homologação com domínio final e HTTPS. | Indexação prematura de páginas incompletas, domínios temporários ou ambiente de staging. | **ALTO** | Manter `False` em staging; comutar para `True` na virada de chave do Go-Live. | Não | **SIM** | **RESOLVIDO NO CÓDIGO** |
| **ACH-17** | **Backups** | Nenhum backup automatizado ativo (apenas cópia manual de SQLite). | Rotina diária automatizada de backup de banco de dados e mídia com retenção controlada. | Perda catastrófica de mensagens de contato, configurações e artigos do blog. | **CRÍTICO** | Implementar rotina de backup (snapshot gerenciado ou `pg_dump`) antes do go-live. | Sim | **SIM** | **PENDENTE DE INFRA** |
| **ACH-18** | **Rollback** | Sem procedimento documentado de reversão. | Procedimento claro de rollback de código, migrations e dados. | Indisponibilidade prolongada em caso de deploy com falha. | **ALTO** | Homologar plano de rollback documentado em `PLANO_ROLLBACK.md`. | Não | Não | **RESOLVIDO NO CÓDIGO** |

---

## 3. Classificação dos Release Blockers (Bloqueadores de Go-Live)

### Bloqueadores Técnicos de Infraestrutura (Impedem Deploy em Produção):
1. **Provisionamento do PostgreSQL de Produção:** Banco relacional com credenciais em variáveis de ambiente.
2. **Armazenamento Persistente para Mídia:** Garantia de que a pasta `media/` ou bucket S3/R2 não é efêmero.
3. **Servidor de Aplicação WSGI:** Configuração de executor homologado (ex: Gunicorn).
4. **Terminação TLS/HTTPS:** Certificado SSL/TLS válido e cabeçalhos de proxy configurados.
5. **Configuração de Segredos:** Injeção de `DJANGO_SECRET_KEY` de alta entropia.

### Bloqueadores de Negócio / Visuais (Impedem Abertura ao Público):
1. **Fotografias Definitivas:** Substituição dos placeholders de atendimentos por fotos reais da profissional.
2. **Dados Oficiais de Atendimento:** Registro de CRP válido, e-mail institucional e telefone WhatsApp.
3. **Domínio Oficial e DNS:** Configuração de domínio canônico e propagação de registros A/CNAME.
4. **Política de Privacidade:** Validação final dos canais de contato e prazos de retenção LGPD.
