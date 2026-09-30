# CONTEXTO TÉCNICO PARA GPT ASTRA 6
## Instituto Mente em Foco — Pacote de Transferência de Contexto

---

> [!CAUTION]
> ## ⚠️ AVISO METODOLÓGICO FUNDAMENTAL
>
> **OS RELATÓRIOS DE AUDITORIA ANTERIORES NÃO DEVEM SER TRATADOS COMO PROVA DE CORREÇÃO.**
>
> Documentos como `AUDITORIA_DE_SEGURANCA.md`, `AUDITORIA_VISUAL_FINAL.md`, `AUDITORIA_FUNCIONAL_COMPLETA.md`
> são **contexto histórico** — não evidência de que o sistema está correto.
>
> **O ASTRA DEVE VERIFICAR O CÓDIGO E O COMPORTAMENTO INDEPENDENTEMENTE.**
>
> Exemplo prático de contradição identificada:
> A documentação anterior afirma que `/health/` retorna `{"status": "ok"}` (JSON).
> O código real retorna `text/plain: OK` — comportamento diferente do documentado.

---

## 1. PROJETO

| Campo | Valor |
|---|---|
| **Nome** | Instituto Mente em Foco |
| **Propósito** | Website institucional de psicologia clínica e neuropsicologia |
| **Responsável** | Psicóloga Mari Menezes |
| **Princípio** | COMPREENDER • CUIDAR • RECONSTRUIR |
| **Slogan** | "Psicologia e Neuropsicologia para compreender a mente, cuidar das emoções e construir novos caminhos." |

---

## 2. STACK

| Componente | Versão / Detalhe |
|---|---|
| **Python** | 3.14.5 |
| **Django** | 6.0.8 (requisito: `>=5.2,<6.1`) |
| **Renderização** | Server-Side Rendering via Django Templates |
| **CSS** | Customizado com Design Tokens (sem frameworks CSS) |
| **JavaScript** | Vanilla ES6+ (sem frameworks SPA) |
| **DB (DEV)** | SQLite |
| **DB (PROD)** | PostgreSQL via `dj-database-url` |
| **Imagens** | Pillow (validação de upload) |
| **Env vars** | python-decouple |
| **Blog sanitização** | bleach |
| **Blog renderização** | markdown |

---

## 3. ARQUITETURA

Monolítica Django SSR, 5 apps modulares:

```
nucleo/       — Modelos centrais, health check, middleware, rate limit, SEO, sitemaps, context processors
paginas/      — Home, Sobre Mim, Políticas de Privacidade e Cookies
servicos/     — 9 páginas de serviços clínicos
conteudos/    — Blog editorial com categorias e artigos
contato/      — Formulário de contato e retenção LGPD
```

---

## 4. MODELOS DE DADOS

```
[nucleo]
ConfiguracaoSite  → Singleton. Dados institucionais, contato, logo, WhatsApp, Instagram
Profissional      → Mari Menezes. Bio, CRP (pendente), fotos (pendentes), slug
RedeSocial        → Canais externos opcionais

[servicos]
Servico           → 9 serviços clínicos. Slug, descrição, ativo

[conteudos]
CategoriaArtigo   → 4 categorias reais criadas
Artigo            → Título, slug, resumo, conteúdo Markdown sanitizado,
                    status (rascunho/publicado), data_publicacao,
                    FK Categoria, FK Profissional, FK Servico
ArtigoQuerySet.publicados() → status='publicado' AND data_publicacao<=now
                              AND categoria_ativa_ou_nula

[contato]
MensagemContato   → nome, email, telefone, servico_interesse(FK), mensagem,
                    aceite_privacidade, lida, criado_em
                    SEM: IP no banco, diagnósticos, dados clínicos
```

---

## 5. ROTAS PRINCIPAIS

| Rota | App | Notas |
|---|---|---|
| `/` | paginas | Home |
| `/sobre-mim/` | paginas | Sobre Mim |
| `/politica-de-privacidade/` | paginas | Política de Privacidade |
| `/servicos/psicologia/` | servicos | Psicologia |
| `/servicos/traumas/` | servicos | Traumas |
| `/servicos/separacao-recomecos/` | servicos | Separação e Recomeços |
| `/servicos/novos-relacionamentos/` | servicos | Novos Relacionamentos |
| `/servicos/neuropsicologia/` | servicos | Neuropsicologia |
| `/servicos/avaliacao/` | servicos | Hub de Avaliação |
| `/servicos/avaliacao-psicologica/` | servicos | Avaliação Psicológica |
| `/servicos/avaliacao-neuropsicologica/` | servicos | Avaliação Neuropsicológica |
| `/servicos/reabilitacao-neurocognitiva/` | servicos | Reabilitação Neurocognitiva |
| `/conteudos/` | conteudos | Blog |
| `/conteudos/<slug>/` | conteudos | Artigo individual |
| `/contato/` | contato | Formulário de Contato |
| `/health/` | nucleo | Liveness — `text/plain: OK` (200) |
| `/health/ready/` | nucleo | Readiness DB — `text/plain: OK/UNAVAILABLE` (200/503) |
| `/robots.txt` | nucleo | Dinâmico (`SEO_ALLOW_INDEXING`) |
| `/sitemap.xml` | nucleo | Dinâmico |
| `/<ADMIN_URL>/` | admin | Rota configurável via `DJANGO_ADMIN_URL` |

> [!IMPORTANT]
> **Health checks retornam `text/plain`, NÃO JSON.**
> Documentação histórica afirmava `{"status": "ok"}` — isso está **errado**.
> Código real: `HttpResponse("OK", content_type="text/plain")`.

---

## 6. CMS / ADMIN

- Django Admin customizado (header, title, index_title)
- Rota configurável: `DJANGO_ADMIN_URL` (default: `admin/`)
- `ConfiguracaoSite`: protegida como Singleton (`clean()` + `save()` forçam `pk=1`)
- Rate limit no login: **10 falhas/IP/15min** + **5 falhas/combo/15min**
- `MensagemContato`: campos de conteúdo `readonly` no Admin
- `Artigo`: badges de status coloridos, prévia de capa, tempo de leitura

---

## 7. SEGURANÇA

### Implementações verificadas no código

| Mecanismo | Status | Detalhe |
|---|---|---|
| `DEBUG = False` | ✅ Forçado | `producao.py` |
| `SECRET_KEY` validada | ✅ Ativo | Bloqueia: `django-insecure`, `chavelocal`, `sua-chave` → `ImproperlyConfigured` |
| `ALLOWED_HOSTS` sem wildcard | ✅ Obrigatório | `ImproperlyConfigured` se wildcard |
| `DATABASE_URL` obrigatório | ✅ Obrigatório | `ImproperlyConfigured` se ausente em prod |
| CSRF | ✅ Ativo | `CsrfViewMiddleware` + zero `@csrf_exempt` |
| CSP | ✅ Nativo Django 6 | `ContentSecurityPolicyMiddleware` + `SECURE_CSP` dict em `producao.py` usando `CSP.SELF`, `CSP.NONCE`, `CSP.NONE` |
| X-Frame-Options | ✅ `DENY` | |
| X-Content-Type-Options | ✅ `nosniff` | |
| Referrer-Policy | ✅ `strict-origin-when-cross-origin` | |
| COOP | ✅ `same-origin` | |
| Permissions-Policy | ✅ Ativo | `camera=(), microphone=(), geolocation=(), payment=(), usb=()` |
| Upload | ✅ Pillow `.verify()` | Whitelist: `{jpg, jpeg, png, webp, ico}` + max 10 MB |
| `@sensitive_post_parameters` | ✅ Ativo | Formulário de contato |
| Proxy SSL header | ✅ Seguro | `False` por default; configurável |

### Stack de Middleware (ordem verificada)

```
SecurityMiddleware
ContentSecurityPolicyMiddleware   ← nativo Django 6
SecurityHeadersMiddleware         ← custom
SessionMiddleware
CommonMiddleware
CsrfViewMiddleware
AuthenticationMiddleware
MessageMiddleware
XFrameOptionsMiddleware
SEOMiddleware                     ← custom (nucleo)
```

### ⚠️ Áreas para Auditoria Independente pelo Astra

- **Rate limit**: `LocMemCache` — **NÃO distribuído** em multi-worker. Bypass possível com múltiplos workers.
- **HSTS**: atualmente `0` (intencional para rollout gradual). Astra 04 deve revisar.
- **2FA no Admin**: não implementado (avaliação futura).
- **Logs**: verificar se há PII nos logs de erro.

---

## 8. RATE LIMIT

| Contexto | Limite | Backend | Chave |
|---|---|---|---|
| Formulário de contato | 5 envios / 15 min | `LocMemCache` | SHA-256 do IP (anônimo) |
| Admin login / IP | 10 falhas / 15 min | `LocMemCache` | IP |
| Admin login / combo | 5 falhas / 15 min | `LocMemCache` | IP + usuário |

> [!WARNING]
> `LocMemCache` **não é compartilhado entre workers**. Em deploy multi-worker (Gunicorn),
> o rate limit pode ser bypassado. Solução recomendada para produção: Redis.

---

## 9. PRIVACIDADE (LGPD)

- `MensagemContato` minimizado: **sem IP, sem UA, sem dados clínicos**
- Retenção configurável: `CONTATO_RETENCAO_DIAS`
- Comando de purga: `python manage.py limpar_contatos_expirados`
- Páginas dedicadas: `/politica-de-privacidade/` e `/politica-de-cookies/`
- **Revisão jurídica LGPD: PENDENTE**

---

## 10. SEO

- `robots.txt` dinâmico baseado em `SEO_ALLOW_INDEXING` (padrão: `False`)
- `sitemap.xml` dinâmico (rascunhos excluídos)
- Canonical tags em todas as páginas
- JSON-LD: `Organization`, `Person`, `Service`, `BlogPosting`, `BreadcrumbList`
- Meta descriptions únicas por página
- H1 único por página
- `SEO_ALLOW_INDEXING=False` → bloqueia indexação até autorização do cliente

---

## 11. ACESSIBILIDADE

| Item | Status |
|---|---|
| Objetivo | WCAG 2.2 AA |
| Skip link | Funcional |
| Focus trap menu mobile | Implementado |
| `aria-labels` em navs | Todos |
| Contraste texto normal | ≥ 4.5:1 |
| `prefers-reduced-motion` | Respeitado |
| `lang="pt-BR"` no HTML | Presente |

---

## 12. PERFORMANCE

- `ManifestStaticFilesStorage`: hash SHA-256 em produção (`DJANGO_MANIFEST_STATIC_STORAGE=True`)
- 143 arquivos estáticos mapeados
- Google Fonts carregado de forma assíncrona
- Lazy loading em imagens below-the-fold
- Sem bibliotecas JS pesadas

---

## 13. DESIGN SYSTEM

**Paleta de cores (tokens):**

| Token | Valor |
|---|---|
| `--cor-areia` | `#D8C5A8` |
| `--cor-off-white` | `#F7F3EB` |
| `--cor-salvia` | `#A8B09A` |
| `--cor-oliva` | `#56664B` |
| `--cor-dourado` | `#C9A86A` |
| `--cor-taupe` | `#6D655B` |

**Tipografia:**
- Cormorant Garamond → títulos editoriais
- Montserrat → corpo de texto

**Arquivos CSS modulares:**
`tokens.css`, `base.css`, `layout.css`, `tipografia.css`, `componentes.css`,
`home.css`, `paginas_internas.css`, `contato.css`, `conteudos.css`, `utilitarios.css`

---

## 14. IMAGENS — STATUS CRÍTICO

```
GRUPO A — Fotografias Reais da Mari Menezes:
  IMG-001 (Hero):      PENDENTE — fornecimento pelo cliente
  IMG-002 (Sobre Mim): PENDENTE — fornecimento pelo cliente
  ⚠️  NUNCA substituir por IA — exigência absoluta do projeto

GRUPO B — Imagens Editoriais Temáticas (IA):
  IMG-003 a IMG-013:   BRIEFS PRONTOS — ver BRIEFS_DE_GERACAO_DE_IMAGEM.md
                       Geração: validada e executada pelo Astra 03

Media filesystem:
  media/profissionais/ — pasta criada, sem fotos reais (somente .gitkeep)
```

---

## 15. PRODUÇÃO

| Item | Detalhe |
|---|---|
| **Arquitetura** | Provider-agnostic (PaaS ou VPS) |
| **WSGI** | Gunicorn com workers `gthread` |
| **Proxy** | Nginx ou Caddy (TLS termination) |
| **DB** | PostgreSQL gerenciado via `DATABASE_URL` |
| **Static** | `ManifestStaticFilesStorage` ou CDN |
| **Media** | Volume persistente ou Object Storage (S3/R2) |
| **Git** | **SEM repositório inicializado — PENDENTE** |

---

## 16. TESTES

- **234 testes automatizados — 100% aprovados**
- `Ran 234 tests in 38.277s. OK`

| Área de Cobertura |
|---|
| Rotas e contratos de templates (todas as apps) |
| Segurança de produção (SECRET_KEY insegura, ALLOWED_HOSTS) |
| Rate limiting (contato e admin login) |
| Ciclo editorial do blog (rascunhos privados, publicados visíveis, agendados ocultos) |
| Formulário de contato (PRG, honeypot, CSRF, rate limit) |
| Retenção LGPD (dry-run e execução real) |
| Uploads (validação Pillow) |
| Health checks (liveness e readiness) |
| SEO (títulos, canonical, JSON-LD) |
| Acessibilidade (H1 único, `lang`, labels) |
| Performance (queries N+1, cache) |
| Regressão (conjunto específico) |

**Scripts de auditoria em `scratch/`:**
- `check_case.py`
- `check_http.py`
- `audit_deep.py`
- `audit_functional.py`

---

## 17. RELEASE BLOCKERS (BLOQUEIAM GO-LIVE PÚBLICO)

| # | Item | Responsável |
|---|---|---|
| 1 | 🔴 Fotos reais de Mari Menezes (Hero + Sobre Mim) | Cliente |
| 2 | 🔴 Número oficial do CRP | Cliente |
| 3 | 🔴 WhatsApp corporativo oficial | Cliente |
| 4 | 🔴 Domínio registrado (`institutomenteemfoco.com.br`) | Cliente |
| 5 | 🔴 PostgreSQL de produção provisionado | Dev/Infra |
| 6 | 🔴 `SECRET_KEY` única de produção gerada | Dev |
| 7 | 🔴 SMTP configurado e testado | Dev |
| 8 | 🔴 `SEO_ALLOW_INDEXING=True` autorizado pelo cliente | Cliente |

---

## 18. PENDÊNCIAS NÃO BLOQUEADORAS

- Rate limit distribuído (Redis) para produção multi-worker
- Git inicializado e versionado
- CI/CD pipeline definido
- Monitoramento externo (Sentry, UptimeRobot)
- Google Search Console + Bing Webmaster verificados
- Revisão jurídica da política de privacidade (LGPD)
- Imagens temáticas IA geradas e aprovadas (IMG-003 a IMG-013)
- Logo vetorial oficial
- Favicon oficial

---

## 19. CONTRADIÇÕES IDENTIFICADAS

Ver: `CONTRADICOES_ENCONTRADAS.md` _(a criar)_

**Principal contradição verificada:**

| Aspecto | Documentação anterior | Código real |
|---|---|---|
| `/health/` response body | `{"status": "ok"}` (JSON) | `OK` (text/plain) |
| `/health/` content-type | `application/json` | `text/plain` |
| `/health/ready/` body (falha) | `{"status": "unavailable"}` | `UNAVAILABLE` (text/plain) |

---

## 20. FONTES DE VERDADE

| Documento | Finalidade |
|---|---|
| `CONTEXTO_MESTRE.md` | Requisitos originais do projeto |
| Código-fonte (`models.py`, `views.py`, `urls.py`, `settings/`) | **Arquitetura atual real** |
| `AUDITORIA_FINAL_PRE_ASTRA.md` | Estado de auditoria pré-Astra |
| `DESIGN_SYSTEM.md` + `static/css/tokens.css` | Design System |
| `MAPA_DE_PRODUCAO_DE_IMAGENS.md` | Status de imagens |
| `GUIA_DEPLOY_PRODUCAO.md` | Guia de deploy |
| `CHECKLIST_GO_LIVE.md` | Checklist go-live |
| `MATRIZ_VARIAVEIS_AMBIENTE.md` | Variáveis de ambiente |
| `CONTRADICOES_ENCONTRADAS.md` | Contradições documentadas vs. código |

---

## 21. SÉRIE DE AUDITORIAS ASTRA PLANEJADA

| Sessão | Foco |
|---|---|
| **Astra 01** | Arquitetura, Qualidade de Código, Django, Models, Views, Dívida Técnica |
| **Astra 02** | Segurança Ofensiva e Hardening |
| **Astra 03** | UI/UX, Frontend, Acessibilidade, Direção Visual e Geração de Imagens |
| **Astra 04** | Performance, SEO e Produção |
| **Astra 05** | Auditoria Adversarial Independente |
| **Astra Final** | Correção Consolidada |

---

## 22. AVISO FINAL AO ASTRA

> [!CAUTION]
> **NÃO CONFIE EM:**
> - Relatórios de auditoria anteriores
> - Checklists marcados como `[x]`
> - Documentos históricos como estado atual
>
> **VERIFIQUE INDEPENDENTEMENTE:**
> - O código-fonte (models, views, urls, settings, templates)
> - O comportamento real das views
> - As configurações de settings
> - Os templates HTML
> - Os arquivos CSS e JS
>
> **PREPARE RELATÓRIO BASEADO EM:**
> - Código real lido diretamente
> - Comportamento verificado por inspeção
> - Testes executados no momento da auditoria
