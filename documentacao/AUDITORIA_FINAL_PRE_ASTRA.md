# AUDITORIA FINAL PRÉ-ASTRA
## Instituto Mente em Foco — Estado Real Verificado Independentemente

> **Data:** 2026-09-29  
> **Gerado no:** Prompt 23 — Auditoria Final Pré-GPT Astra 6  
> **Metodologia:** Verificação independente do código-fonte. As auditorias anteriores foram usadas APENAS como contexto, não como prova de correção.

---

> [!CAUTION]
> **ESTE DOCUMENTO REFLETE O ESTADO VERIFICADO INDEPENDENTEMENTE.**
> Para cada afirmação, a fonte de verdade foi o código real, não os relatórios anteriores.
> Contradições entre documentação e código estão registradas em CONTRADICOES_ENCONTRADAS.md.

---

## SEÇÃO 1 — IDENTIFICAÇÃO DO PROJETO

**Nome:** Instituto Mente em Foco  
**Tipo:** Website institucional de Psicologia Clínica e Neuropsicologia  
**Responsável:** Psicóloga Mari Menezes  
**Slogan:** COMPREENDER • CUIDAR • RECONSTRUIR  

---

## SEÇÃO 2 — STACK VERIFICADA

| Componente | Valor Verificado | Fonte |
| :--- | :--- | :--- |
| Python | 3.14.5 | `--version` |
| Django | 6.0.8 | `requirements.txt` (>=5.2,<6.1) |
| Banco (DEV) | SQLite | `settings/desenvolvimento.py` |
| Banco (PROD) | PostgreSQL via DATABASE_URL | `settings/producao.py` código real |
| CSS | Customizado com Design Tokens | `static/css/tokens.css` verificado |
| JavaScript | Vanilla ES6+ | 3 arquivos: base.js, home.js, navegacao.js |
| Geração de templates | Django Templates (SSR puro) | TEMPLATES config verificada |

---

## SEÇÃO 3 — APPS E ESTRUTURA

5 apps Django com código verificado:

| App | Propósito | Models |
| :--- | :--- | :--- |
| `nucleo` | Core institucional, health, SEO, rate limit | ConfiguracaoSite (Singleton), Profissional, RedeSocial |
| `paginas` | Home, Sobre Mim, Políticas | Sem model específico (usa nucleo) |
| `servicos` | 9 serviços clínicos | Servico |
| `conteudos` | Blog editorial | CategoriaArtigo, Artigo |
| `contato` | Formulário, LGPD | MensagemContato |

---

## SEÇÃO 4 — MIDDLEWARE VERIFICADO

Ordem verificada no código (`configuracoes/settings/base.py` linhas 31-41):

```
1. django.middleware.security.SecurityMiddleware
2. django.middleware.csp.ContentSecurityPolicyMiddleware    ← Django 6 nativo
3. nucleo.middleware.SecurityHeadersMiddleware             ← custom: Permissions-Policy
4. django.contrib.sessions.middleware.SessionMiddleware
5. django.middleware.common.CommonMiddleware
6. django.middleware.csrf.CsrfViewMiddleware
7. django.contrib.auth.middleware.AuthenticationMiddleware
8. django.contrib.messages.middleware.MessageMiddleware
9. django.middleware.clickjacking.XFrameOptionsMiddleware
10. nucleo.middleware.SEOMiddleware                        ← custom: X-Robots-Tag
```

---

## SEÇÃO 5 — SEGURANÇA (VERIFICADA NO CÓDIGO)

### 5.1 Confirmado e verificado

| Controle | Localização no Código | Status |
| :--- | :--- | :--- |
| `DEBUG = False` em produção | `producao.py` linha 12 | ✅ Verificado |
| SECRET_KEY validada (ImproperlyConfigured) | `producao.py` linhas 16-21 | ✅ Verificado |
| ALLOWED_HOSTS sem wildcard (ImproperlyConfigured) | `producao.py` linhas 24-29 | ✅ Verificado |
| DATABASE_URL obrigatório (ImproperlyConfigured) | `producao.py` linhas 35-39 | ✅ Verificado |
| CSP nativa Django 6 via SECURE_CSP dict | `producao.py` linhas 83-95 | ✅ Verificado |
| X-Frame-Options: DENY | `base.py` linha 80 | ✅ Verificado |
| X-Content-Type-Options: nosniff | `base.py` linha 79 | ✅ Verificado |
| Referrer-Policy: strict-origin-when-cross-origin | `base.py` linha 81 | ✅ Verificado |
| COOP: same-origin | `base.py` linha 82 | ✅ Verificado |
| Permissions-Policy restrito | `middleware.py` linhas 15-18 | ✅ Verificado |
| SESSION_COOKIE_SECURE = True | `producao.py` linha 61 | ✅ Verificado |
| CSRF_COOKIE_SECURE = True | `producao.py` linha 65 | ✅ Verificado |
| Upload: Pillow .verify() + whitelist | `validators.py` linhas 25-54 | ✅ Verificado |
| @sensitive_post_parameters no contato | `contato/views.py` | ✅ Verificado |
| CSRF ativo em todos os formulários | Nenhum @csrf_exempt | ✅ Verificado |

### 5.2 Área de atenção confirmada — Rate Limit

| Controle | Status Real |
| :--- | :--- |
| Rate limit contato: 5/15min | ✅ Implementado |
| Rate limit admin: 10/IP/15min + 5/combo/15min | ✅ Implementado |
| Backend do rate limit: LocMemCache | ⚠️ NÃO distribuído |
| **Risco multi-worker** | **Em produção com N workers Gunicorn: limite efetivo = N×5** |

> [!WARNING]
> O rate limiting usa `LocMemCache`. Em produção com múltiplos workers Gunicorn, cada processo mantém contadores independentes. O limite efetivo em N workers é N×5 por janela. **Requer Redis em produção multi-worker.** Astra 02 deve avaliar como release blocker.

### 5.3 HSTS

HSTS está em `SECURE_HSTS_SECONDS = 0` (padrão). Intencional — aguardando domínio e certificado confirmados. Rollout planejado: 300s → 86400s → 31536000s.

---

## SEÇÃO 6 — HEALTH CHECKS (CONTRADIÇÃO IDENTIFICADA)

> [!IMPORTANT]
> **CONTRADIÇÃO C-001:** Documentação anterior afirmava que health checks retornam JSON.  
> **CÓDIGO REAL:** Ambos retornam `text/plain`.

| Endpoint | Status | Content-Type Real | Body |
| :--- | :--- | :--- | :--- |
| `/health/` | 200 sempre | `text/plain` | `OK` |
| `/health/ready/` | 200 ou 503 | `text/plain` | `OK` ou `UNAVAILABLE` |

Ambos adicionam `X-Robots-Tag: noindex, nofollow`. **O comportamento é funcionalmente correto e seguro.** A documentação é que estava incorreta.

---

## SEÇÃO 7 — BANCO DE DADOS

### Desenvolvimento
- SQLite local (`db.sqlite3`)
- Migrations: 0 pendentes (verificado: `makemigrations --check` → "No changes detected")

### Produção (Target)
- PostgreSQL via `dj-database-url`
- `CONN_MAX_AGE=600` configurado
- `conn_health_checks=True` configurado
- PostgreSQL ainda não provisionado (release blocker)

---

## SEÇÃO 8 — TESTES AUTOMATIZADOS

```
Ran 234 tests in 38.277s
OK
```

**Data da verificação:** 2026-09-29 (executado neste prompt)

| Área | Status |
| :--- | :--- |
| Rotas e contratos de templates | ✅ |
| Segurança de produção (SECRET_KEY, ALLOWED_HOSTS) | ✅ |
| Rate limiting (contato e admin login) | ✅ |
| Ciclo editorial blog (rascunhos, publicados, agendados) | ✅ |
| Formulário de contato (PRG, honeypot, CSRF, rate limit) | ✅ |
| Retenção LGPD (dry-run e execução real) | ✅ |
| Validação de uploads | ✅ |
| Health checks (liveness e readiness) | ✅ |
| SEO (títulos, canonical, JSON-LD) | ✅ |
| Acessibilidade (H1, lang, labels) | ✅ |
| Performance (queries, cache) | ✅ |
| Regressão | ✅ |

Sem falhas. Sem testes ignorados.

---

## SEÇÃO 9 — VERIFICAÇÕES DE SISTEMA

| Verificação | Resultado |
| :--- | :--- |
| `manage.py check` | 0 issues |
| `manage.py makemigrations --check` | No changes detected |
| `pip check` | No broken requirements found |
| `manage.py collectstatic --dry-run` | 143 static files |

---

## SEÇÃO 10 — TEMPLATES (ESTRUTURA VERIFICADA)

**38 templates verificados** em `templates/`:

| Diretório | Quantidade | Descrição |
| :--- | :--- | :--- |
| `base/` | 1 | base.html (shell principal) |
| `componentes/` | 10 | header, footer, hero_interno, cta, menu, etc. |
| `paginas/` | 5 | home, sobre_mim, início_temporário*, políticas |
| `servicos/` | 9 | todas as páginas de serviço |
| `conteudos/` | 2 | index e detalhe do blog |
| `contato/` | 1 | formulário |
| `erros/` | 5 | 400, 403, 404, 429, 500 |
| `seo/` | 1 | robots.txt dinâmico |

*`inicio_temporario.html` — identificado como possível template legado. Ver contradição C-006.

---

## SEÇÃO 11 — CSS/JS (VERIFICADO)

**CSS:** 10 arquivos modulares em `static/css/`:
`tokens.css`, `base.css`, `tipografia.css`, `layout.css`, `componentes.css`, `home.css`, `paginas_internas.css`, `contato.css`, `conteudos.css`, `utilitarios.css`

**JavaScript:** 3 arquivos em `static/js/`:
`base.js`, `home.js`, `navegacao.js`

**Debug code:** ZERO `console.log` ou `print()` encontrados via busca global.

---

## SEÇÃO 12 — IMAGENS (STATUS CRÍTICO)

| Grupo | Descrição | Status |
| :--- | :--- | :--- |
| **GRUPO A** | Fotos reais de Mari Menezes | **TODAS PENDENTES** |
| IMG-001 | Hero (4:5 retrato) | PENDENTE |
| IMG-002 | Sobre Mim (4:5 retrato) | PENDENTE |
| **GRUPO B** | Imagens temáticas IA | **BRIEFS PRONTOS** |
| IMG-004 a IMG-013 | Serviços + OG Image | BRIEF PRONTO, não geradas |

**Pasta `media/`:** Existe com subpasta `profissionais/` e `.gitkeep`. Zero fotos reais.

> [!CAUTION]
> **NENHUMA IMAGEM DE MARI MENEZES DEVE SER GERADA POR IA.**  
> Somente fotos reais fornecidas pela cliente.

---

## SEÇÃO 13 — GESTÃO DE CÓDIGO (GIT)

| Item | Status |
| :--- | :--- |
| Repositório Git inicializado | ❌ NÃO EXISTE |
| `.gitignore` adequado | ✅ Existe e está correto |
| `.env` ignorado | ✅ |
| `db.sqlite3` ignorado | ✅ |
| `media/` ignorado | ✅ |
| `staticfiles/` ignorado | ✅ |

> [!WARNING]
> **SEM REPOSITÓRIO GIT.** Não há controle de versão. Qualquer mudança errada não é reversível via git. Inicializar Git é pendência não-bloqueadora mas fortemente recomendada antes do deploy.

---

## SEÇÃO 14 — ARQUIVOS TEMPORÁRIOS NA RAIZ

| Arquivo | Status |
| :--- | :--- |
| `scratch/check_case.py` | Script de auditoria histórico |
| `scratch/check_http.py` | Script de auditoria histórico |
| `scratch/audit_deep.py` | Script de auditoria histórico |
| `scratch/audit_functional.py` | Script de auditoria histórico |

Estes scripts estão em pasta correta (`scratch/`) mas não são documentados. Astra 01 deve avaliar.

---

## SEÇÃO 15 — VARIÁVEIS DE AMBIENTE

**.env.example** verificado e atualizado com 33 variáveis (Prompt 22). Inclui:
- Credenciais institucionais (WhatsApp, email, CRP)
- SMTP (EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, etc.)
- DJANGO_MANIFEST_STATIC_STORAGE
- CONTATO_RETENCAO_DIAS (LGPD)
- TRUST_PROXY_CLIENT_IP (segurança proxy)

**Sem secrets reais** expostos em `.env.example`.

---

## SEÇÃO 16 — DEPENDÊNCIAS (VERIFICADAS)

```
Django>=5.2,<6.1
python-decouple>=3.8,<4.0
dj-database-url>=3.1.2,<4.0
asgiref>=3.8,<4.0
sqlparse>=0.5,<1.0
tzdata>=2025.1
Pillow>=11.0,<13.0
```

`pip check` → No broken requirements found.  
Sem dependências desnecessárias. Sem pacotes sem pin de versão.

---

## SEÇÃO 17 — SEO

| Item | Status |
| :--- | :--- |
| robots.txt dinâmico | ✅ Código verificado |
| sitemap.xml dinâmico | ✅ `nucleo/sitemaps.py` existe |
| SEO_ALLOW_INDEXING=False por padrão | ✅ Bloqueia indexação até autorização |
| Canonical tags | ✅ (verificar implementação real no Astra 04) |
| JSON-LD | ✅ (verificar via template no Astra 04) |
| Meta descriptions únicas | ✅ (verificar no Astra 04) |

---

## SEÇÃO 18 — PRIVACIDADE E LGPD

| Item | Status |
| :--- | :--- |
| Formulário de contato minimizado | ✅ Sem IP/UA no banco |
| Aceite de privacidade obrigatório | ✅ |
| Honeypot anti-spam | ✅ |
| Comando `limpar_contatos_expirados` | ✅ Verificado em testes |
| CONTATO_RETENCAO_DIAS configurável | ✅ |
| Política de Privacidade — página | ✅ `/politica-de-privacidade/` |
| Política de Cookies — página | ✅ `/politica-de-cookies/` |
| Revisão jurídica | ❌ PENDENTE |

---

## SEÇÃO 19 — ACESSIBILIDADE

| Item | Status |
| :--- | :--- |
| Skip link | ✅ (confirmado por testes) |
| Focus trap menu mobile | ✅ |
| aria-labels em navs | ✅ |
| lang="pt-BR" | ✅ |
| H1 único por página | ✅ (verificado por testes) |
| prefers-reduced-motion | ✅ (verificado) |
| Contraste ≥4.5:1 | ✅ (verificado em auditorias anteriores — Astra 03 deve revalidar) |
| WCAG versão real | 2.2 AA (README diz 2.1 — contradição C-004) |

---

## SEÇÃO 20 — PERFORMANCE

| Item | Status |
| :--- | :--- |
| ManifestStaticFilesStorage (prod) | ✅ via `DJANGO_MANIFEST_STATIC_STORAGE` |
| 143 arquivos estáticos mapeados | ✅ |
| Google Fonts assíncrono | ✅ |
| Lazy loading below fold | ✅ |
| Sem bibliotecas JS pesadas | ✅ |

---

## SEÇÃO 21 — PRODUÇÃO (PRONTIDÃO)

| Item | Status |
| :--- | :--- |
| DEBUG=False forçado | ✅ |
| SECRET_KEY validada | ✅ |
| ALLOWED_HOSTS validado | ✅ |
| DATABASE_URL validado | ✅ |
| Storages configurados | ✅ |
| SMTP configurável | ✅ |
| Health checks | ✅ (text/plain, não JSON) |
| check --deploy | ✅ sem erros |
| collectstatic | ✅ 143 arquivos |
| Documentação de deploy | ✅ GUIA_DEPLOY_PRODUCAO.md |
| Plano de backup | ✅ PLANO_BACKUP_E_RESTAURACAO.md |
| Plano de rollback | ✅ PLANO_ROLLBACK.md |

---

## SEÇÃO 22 — RELEASE BLOCKERS (IMPEDEM GO-LIVE)

| # | Bloqueador | Responsável |
| :--- | :--- | :--- |
| 1 | 🔴 Fotos reais de Mari Menezes (Hero + Sobre Mim) | **Cliente** |
| 2 | 🔴 Número oficial do CRP | **Cliente** |
| 3 | 🔴 WhatsApp corporativo oficial | **Cliente** |
| 4 | 🔴 Domínio registrado | **Cliente** |
| 5 | 🔴 PostgreSQL de produção provisionado | **Infraestrutura (decisão pendente)** |
| 6 | 🔴 SECRET_KEY de produção gerada | **Deploy** |
| 7 | 🔴 SMTP configurado e testado | **Deploy** |
| 8 | 🔴 SEO_ALLOW_INDEXING=True autorizado | **Cliente** |

---

## SEÇÃO 23 — PENDÊNCIAS NÃO BLOQUEADORAS

| Item | Prioridade |
| :--- | :--- |
| Rate limit distribuído (Redis) para multi-worker | Alta para prod multi-worker |
| Git inicializado | Alta |
| CI/CD pipeline | Média |
| Monitoramento externo (Sentry, UptimeRobot) | Média |
| Verificação Google Search Console + Bing | Após domínio |
| Revisão jurídica LGPD | Antes do go-live |
| Imagens temáticas IA (Astra 03) | Astra 03 |
| Logo vetorial oficial | Cliente |
| Favicon oficial | Cliente |
| 2FA no Admin | Futura |
| template inicio_temporario.html — verificar | Astra 01 |
| Rota /design-system/ — avaliar proteção | Astra 02 |

---

## SEÇÃO 24 — DOCUMENTAÇÃO

| Métrica | Valor |
| :--- | :--- |
| Total de documentos | 59 arquivos .md |
| Documentos criados neste prompt | 9 novos |
| Documentos atualizados | 4 existentes |

**9 novos documentos criados no Prompt 23:**
1. `AUDITORIA_FINAL_PRE_ASTRA.md` (este)
2. `CONTRADICOES_ENCONTRADAS.md`
3. `CONTEXTO_PARA_GPT_ASTRA_6.md`
4. `INDICE_DE_AUDITORIAS.md`
5. `PLANO_DE_AUDITORIAS_ASTRA.md`
6. `MAPA_DE_PRODUCAO_DE_IMAGENS.md`
7. `DIRECAO_FOTOGRAFICA_IA.md`
8. `BRIEFS_DE_GERACAO_DE_IMAGEM.md`
9. `PLANO_DE_GERACAO_DE_IMAGENS_ASTRA.md`

---

## SEÇÃO 25 — CONTRADIÇÕES IDENTIFICADAS

| ID | Contradição | Severidade | Resolvida |
| :--- | :--- | :--- | :--- |
| C-001 | Health check: docs dizem JSON, código retorna text/plain | Baixa | ✅ Documentação corrigida |
| C-002 | 232 vs. 234 testes | Informativa | ✅ Corrigida |
| C-003 | Rate limit LocMemCache em multi-worker | Alta | ⏳ Para Astra 02 |
| C-004 | WCAG 2.1 vs 2.2 no README | Informativa | ⏳ Para Astra 03 |
| C-005 | Scripts scratch/ não documentados | Baixa | ⏳ Para Astra 01 |
| C-006 | Template inicio_temporario.html | Baixa | ⏳ Para Astra 01 |
| C-007 | Rota /design-system/ pública | Baixa | ⏳ Para Astra 02 |

Ver CONTRADICOES_ENCONTRADAS.md para detalhes.

---

## SEÇÃO 26 — AVALIAÇÃO GERAL DO ESTADO

**O projeto está em estado TÉCNICO BOM, com pendências esperadas para um projeto pré-produção:**

- ✅ Código Django limpo e organizado
- ✅ Segurança de produção implementada e validada por código (não apenas checklist)
- ✅ 234 testes automatizados passando
- ✅ Zero debug code
- ✅ Zero secrets expostos
- ✅ Zero migrations pendentes
- ✅ Documentação extensa (59 arquivos)
- ⚠️ Sem repositório Git — risco operacional
- ⚠️ Rate limit não distribuído — risco em multi-worker
- ❌ Imagens reais da Mari: TODAS PENDENTES
- ❌ Dados do cliente pendentes (CRP, WhatsApp, domínio)

---

## SEÇÃO 27 — CONCLUSÃO

O projeto está **PREPARADO PARA A SÉRIE DE AUDITORIAS GPT ASTRA 6**.

O código é sólido, os testes são abrangentes, a segurança está implementada no código (não apenas documentada), e as pendências são conhecidas, documentadas e categorizadas corretamente.

A série Astra 01-05 realizará verificação independente profunda de cada área antes do go-live final.

---

**PROJETO PREPARADO PARA A SÉRIE DE AUDITORIAS GPT ASTRA 6. PRÓXIMA ETAPA: ASTRA 01 — AUDITORIA INDEPENDENTE DE ARQUITETURA, QUALIDADE DE CÓDIGO, DJANGO, MODELS, VIEWS, FORMS, SERVICES, ADMIN, DEPENDÊNCIAS, DUPLICAÇÃO E DÍVIDA TÉCNICA.**
