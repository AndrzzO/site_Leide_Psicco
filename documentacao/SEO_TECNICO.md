# MANUAL DE SEO TÉCNICO & DADOS ESTRUTURADOS
**PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 5.X
**DATA DE IMPLEMENTAÇÃO:** 21 DE SETEMBRO DE 2026 | **STATUS:** HOMOLOGADO E TESTADO

---

## 1. VISÃO GERAL E FILOSOFIA DE SEO

A estratégia de SEO Técnico do **Instituto Mente em Foco** foi concebida para atender aos mais elevados padrões de qualidade da web, acessibilidade e conformidade ética com o Conselho Federal de Psicologia (CFP).

### Princípios Inegociáveis:
1. **Ética Médica e Psicológica:** Ausência absoluta de avaliações fictícias (`AggregateRating`), estrelas manipuladas, falsas credenciais médicas ou promessas milagrosas de cura.
2. **Prevenção Ativa de Indexação Precoce:** Ambientes locais, de homologação ou previews de pull request são estritamente protegidos contra indexação por buscadores via `SEO_ALLOW_INDEXING=False` e cabeçalho `X-Robots-Tag: noindex, nofollow, noarchive`.
3. **Segurança de Código (Anti-XSS):** Todo JSON-LD serializado é tratado no servidor com escape seguro contra encerramento indevido de scripts (`</script>` -> `\u003c/script\u003e`).
4. **Reserva da Rota Administrativa:** A URL do painel administrativo (`DJANGO_ADMIN_URL`) nunca é vazada no `robots.txt`.

---

## 2. GOVERNANÇA DE AMBIENTES E INDEXAÇÃO

### 2.1 Variáveis de Ambiente (`.env` / `settings`)

| Variável | Tipo | Padrão | Finalidade |
|---|---|---|---|
| `SEO_ALLOW_INDEXING` | `bool` | `False` | Chave-mestra de indexação pública. DEVE ser `True` **apenas** no servidor de produção final. |
| `SITE_URL` | `str` | `http://localhost:8000` | URL pública canônica (sem barra final). Em produção: `https://institutomenteemfoco.com.br`. |
| `GOOGLE_SITE_VERIFICATION` | `str` | `""` | Código de autenticação para o Google Search Console. |
| `BING_SITE_VERIFICATION` | `str` | `""` | Código de autenticação para o Bing Webmaster Tools. |

### 2.2 Verificações Automáticas de Sistema (`manage.py check`)
Implementadas em [`nucleo/checks.py`](file:///c:/Users/andre/Documents/SiteDjangoLeide/nucleo/checks.py) e registradas sob a tag `security`:

* **`seo.E001` (Erro Crítico):** Dispara se `SEO_ALLOW_INDEXING=True` enquanto `DEBUG=True`. Impede subir produção com depurador ativo ou indexar ambiente de teste.
* **`seo.E002` (Erro Crítico):** Dispara se `SEO_ALLOW_INDEXING=True` e `SITE_URL` estiver vazia, ou contiver `localhost`, `127.0.0.1` ou `example.com`.
* **`seo.W001` (Aviso):** Alerta caso `SEO_ALLOW_INDEXING=True` e `SITE_URL` não inicie com o protocolo seguro `https://`.

### 2.3 Middleware de Cabeçalhos HTTP (`SEOMiddleware`)
Registrado em `nucleo.middleware.SEOMiddleware`:
* Se `SEO_ALLOW_INDEXING == False`: injeta `X-Robots-Tag: noindex, nofollow, noarchive` em 100% das respostas HTTP.
* Se `SEO_ALLOW_INDEXING == True`:
  * Páginas de erro (status >= 400): injeta `X-Robots-Tag: noindex, nofollow`.
  * Resultados de pesquisa interna (`?q=...`): injeta `X-Robots-Tag: noindex, follow`.
  * Rotas `/health/` e `/design-system/`: injeta `X-Robots-Tag: noindex, nofollow`.
  * Páginas de políticas (`/politica-de-privacidade/`, `/politica-de-cookies/`): injeta `X-Robots-Tag: noindex, follow`.

---

## 3. ROBOTS.TXT DINÂMICO (`/robots.txt`)

Gerado pela view `nucleo.views.robots_txt` com tipo MIME `text/plain; charset=utf-8`:

### Quando `SEO_ALLOW_INDEXING=False` (Dev / Homologação):
```txt
User-agent: *
Disallow: /
```

### Quando `SEO_ALLOW_INDEXING=True` (Produção):
```txt
User-agent: *
Allow: /

Sitemap: https://institutomenteemfoco.com.br/sitemap.xml
```

> [!NOTE]
> Por diretriz de segurança cibernética, a URL secreta do Django Admin **não** é declarada em `Disallow:` para evitar ataques de enumeração e reconhecimento de rotas administrativas. O bloqueio ao painel administrativo é realizado no nível do próprio Django e com `noindex, nofollow` padrão da aplicação admin.

---

## 4. SITEMAP.XML DINÂMICO (`/sitemap.xml`)

Construído via `django.contrib.sitemaps` em [`nucleo/sitemaps.py`](file:///c:/Users/andre/Documents/SiteDjangoLeide/nucleo/sitemaps.py):

| Seção de Sitemap | Itens Incluídos | Priority | Changefreq | Regra de Exclusão |
|---|---|---|---|---|
| `paginas` | `/`, `/sobre-mim/`, `/contato/`, `/politica-de-privacidade/`, `/politica-de-cookies/` | 1.0 (Home), 0.8 (Páginas), 0.3 (Legais) | Weekly / Monthly / Yearly | Exclui aliases duplicados (`/privacidade/`, `/cookies/`), erros e utilitários. |
| `servicos` | Todas as páginas ativas de serviços (`psicologia`, `neuropsicologia`, `traumas`, etc.) | 0.9 / 0.8 | Monthly | Exclui serviços inativos (`ativo=False`). |
| `conteudos` | Artigos publicados do Blog | 0.7 | Weekly | Exclui rascunhos (`status='rascunho'`), artigos agendados no futuro e com categorias inativas. |
| `categorias` | Categorias temáticas ativas | 0.6 | Weekly | Exclui categorias sem nenhum artigo publicado. |

---

## 5. ARQUITETURA DE METADADOS CENTRALIZADA (`base.html`)

Localizada em [`templates/base/base.html`](file:///c:/Users/andre/Documents/SiteDjangoLeide/templates/base/base.html):

```html
<!-- Metadados Fundamentais de SEO -->
<title>{% block title %}{{ NOME_INSTITUTO }} — {{ CONCEITO_TRIPLICE }}{% endblock title %}</title>
<meta name="description" content="{% block meta_description %}{{ ASSINATURA_INSTITUCIONAL }}{% endblock meta_description %}">
<meta name="robots" content="{% block meta_robots %}{% if meta_robots %}{{ meta_robots }}{% elif not SEO_ALLOW_INDEXING %}noindex, nofollow, noarchive{% else %}index, follow{% endif %}{% endblock meta_robots %}">

<!-- URL Canônica Absoluta -->
<link rel="canonical" href="{% if canonical_url %}{{ canonical_url }}{% elif canonical_path %}{{ SITE_URL }}{{ canonical_path }}{% else %}{{ SITE_URL }}{{ request.path }}{% endif %}">

<!-- Verificação de Mecanismos de Busca -->
{% if GOOGLE_SITE_VERIFICATION %}<meta name="google-site-verification" content="{{ GOOGLE_SITE_VERIFICATION }}">{% endif %}
{% if BING_SITE_VERIFICATION %}<meta name="msvalidate.01" content="{{ BING_SITE_VERIFICATION }}">{% endif %}

<!-- Open Graph & Twitter Cards -->
<meta property="og:site_name" content="{{ NOME_INSTITUTO }}">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="{% block og_type %}website{% endblock og_type %}">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="...">
<meta property="og:image" content="...">
<meta property="og:image:alt" content="...">
<meta name="twitter:card" content="summary_large_image">
```

---

## 6. DADOS ESTRUTURADOS SCHEMA.ORG (JSON-LD)

Disponibilizados via templatetags seguras em [`nucleo/templatetags/seo_tags.py`](file:///c:/Users/andre/Documents/SiteDjangoLeide/nucleo/templatetags/seo_tags.py):

### 6.1 Grafo Base (`render_global_schema`)
Presente globalmente em todas as páginas do site:
* **`WebSite`:** Identidade do portal, idioma `pt-BR`, e `SearchAction` apontando para `/conteudos/?q={search_term_string}`.
* **`Organization`:** Razão social, marca, logotipo SVG oficial, canais reais de atendimento (telefone, e-mail) e redes sociais confirmadas (ignora marcadores `PENDENTE_DEFINICAO`).
* **`Person`:** Psicóloga Mari Menezes, cargo "Psicóloga Clínica e Neuropsicóloga", vínculo institucional com o Instituto e CRP oficial (quando configurado).

### 6.2 Esquemas Específicos por Página
* **Páginas de Serviços:** `Service` com nome, descrição, provedor (`@id: #organization`) e área atendida (`Brasil`).
* **Páginas de Artigo:** `BlogPosting` com manchete, resumo, datas ISO 8601 (`datePublished`, `dateModified`), imagem de capa absoluta, autoria e editora.
* **Páginas Internas:** `BreadcrumbList` estruturado indicando a hierarquia de navegação com URLs absolutas.

---

## 7. POLÍTICAS DE ROTA E CANONICALIZAÇÃO

1. **Busca Interna (`/conteudos/?q=...`):**
   - Diretiva: `noindex, follow`
   - Canonical: aponta para a URL base `/conteudos/` (limpa de parâmetros de pesquisa).
2. **Páginas Legais (`/politica-de-privacidade/`, `/politica-de-cookies/`):**
   - Diretiva: `noindex, follow`
   - Aliases (`/privacidade/`, `/cookies/`): Canonical explícita apontando para suas versões definitivas.
3. **Páginas de Erro (400, 403, 404, 500):**
   - Diretiva: `noindex, nofollow`.

---

## 8. CHECKLIST PARA ATIVAÇÃO EM PRODUÇÃO

Ao realizar o deploy definitivo para o domínio de produção:

1. [ ] Configurar `SITE_URL=https://institutomenteemfoco.com.br` no `.env`.
2. [ ] Garantir que o certificado SSL esteja ativo e forçando HTTPS.
3. [ ] Definir `DJANGO_DEBUG=False` no `.env`.
4. [ ] Definir `SEO_ALLOW_INDEXING=True` no `.env`.
5. [ ] Obter os códigos de verificação no Search Console e configurar `GOOGLE_SITE_VERIFICATION`.
6. [ ] Executar `python manage.py check --deploy` para atestar zero inconformidades.
7. [ ] Acessar `https://institutomenteemfoco.com.br/robots.txt` e verificar a saída com `Allow: /` e link para o sitemap.
8. [ ] Submeter `https://institutomenteemfoco.com.br/sitemap.xml` no Google Search Console e Bing Webmaster Tools.
9. [ ] Validar a Home e um Artigo na [Ferramenta de Teste de Rich Results do Google](https://search.google.com/test/rich-results).
