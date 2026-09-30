# AUDITORIA DE SEO TÉCNICO — INSTITUTO MENTE EM FOCO
**Data da Auditoria:** 21 de Setembro de 2026 | **Ambiente:** Desenvolvimento / Staging Inicial
**Responsável Técnico:** Antigravity AI | **Framework:** Django 5.x | **Escopo:** Prompt 12

---

## 1. OBJETIVO DA AUDITORIA

Realizar um diagnóstico completo, criterioso e aprofundado da infraestrutura de SEO técnico do site institucional do **Instituto Mente em Foco**, identificando lacunas, riscos de indexação inadvertida de ambientes não produtivos, ausência de metadados padronizados, falta de sitemap e robots, e necessidade de dados estruturados JSON-LD semânticos e seguros.

---

## 2. DIAGNÓSTICO DO ESTADO ATUAL

### 2.1 Mapeamento de Rotas e Indexabilidade

| Rota | View / Nome | Finalidade | Status Atual | Indexável em Produção? |
|---|---|---|---|---|
| `/` | `paginas:inicio` | Home Institucional | Ativa | Sim (`index, follow`) |
| `/sobre-mim/` | `paginas:sobre_mim` | Perfil da Profissional Mari Menezes | Ativa | Sim (`index, follow`) |
| `/servicos/psicologia/` | `servicos:psicologia` | Psicoterapia Clínica | Ativa | Sim (`index, follow`) |
| `/servicos/neuropsicologia/` | `servicos:neuropsicologia` | Neuropsicologia | Ativa | Sim (`index, follow`) |
| `/servicos/traumas/` | `servicos:traumas` | Traumas e Experiências Difíceis | Ativa | Sim (`index, follow`) |
| `/servicos/separacao-e-recomecos/` | `servicos:separacao_recomecos` | Separação & Recomeços | Ativa | Sim (`index, follow`) |
| `/servicos/novos-relacionamentos/` | `servicos:novos_relacionamentos` | Novos Relacionamentos | Ativa | Sim (`index, follow`) |
| `/servicos/avaliacao/` | `servicos:avaliacao` | Hub de Avaliação | Ativa | Sim (`index, follow`) |
| `/servicos/avaliacao-psicologica/` | `servicos:avaliacao_psicologica` | Avaliação Psicológica | Ativa | Sim (`index, follow`) |
| `/servicos/avaliacao-neuropsicologica/` | `servicos:avaliacao_neuropsicologica` | Avaliação Neuropsicológica | Ativa | Sim (`index, follow`) |
| `/servicos/reabilitacao-neurocognitiva/` | `servicos:reabilitacao_neurocognitiva` | Reabilitação Neurocognitiva | Ativa | Sim (`index, follow`) |
| `/conteudos/` | `conteudos:index` | Listagem Geral do Blog | Ativa | Sim (`index, follow`) |
| `/conteudos/?q=...` | `conteudos:index` (com busca) | Resultado de Busca Interna | Ativa | **NÃO** (`noindex, follow`) |
| `/conteudos/categoria/<slug>/` | `conteudos:categoria` | Filtro por Categoria | Ativa | Sim (`index, follow`) |
| `/conteudos/<slug>/` | `conteudos:detalhe` | Artigo Individual | Ativa | Sim (`index, follow` se publicado) |
| `/contato/` | `contato:index` | Atendimento & Contato | Ativa | Sim (`index, follow`) |
| `/politica-de-privacidade/` | `paginas:politica_privacidade` | LGPD e Privacidade | Ativa | Sim (`noindex, follow` ou canônica) |
| `/privacidade/` | `paginas:privacidade` | Alias de Privacidade | Ativa | **NÃO** (Canônica para `/politica-de-privacidade/`) |
| `/politica-de-cookies/` | `paginas:politica_cookies` | Política de Cookies | Ativa | Sim (`noindex, follow` ou canônica) |
| `/cookies/` | `paginas:cookies` | Alias de Cookies | Ativa | **NÃO** (Canônica para `/politica-de-cookies/`) |
| `/design-system/` | `paginas:laboratorio_design_system` | Laboratório Visual | Dev only | **NÃO** (`noindex, nofollow`, bloqueado em prod) |
| `/health/` | `nucleo:health_check` | Healthcheck de Infra | Ativa | **NÃO** (`noindex, nofollow`, fora de sitemaps) |
| `/{DJANGO_ADMIN_URL}` | `admin:index` | Painel Administrativo | Ativa | **NÃO** (`noindex, nofollow`, fora de robots/sitemap) |

---

### 2.2 Lacunas Identificadas

1. **Governança de Ambientes:**
   - Não havia variável `SEO_ALLOW_INDEXING`. Ambientes locais e de teste poderiam, inadvertidamente, enviar tags `index, follow` caso expostos à web (ex: túneis Ngrok, previews de CI/CD).
   - Ausência de cabeçalho HTTP `X-Robots-Tag: noindex, nofollow, noarchive` em ambientes de desenvolvimento e homologação.
   - Ausência de verificação preventiva de inicialização (`check`) alertando caso `SEO_ALLOW_INDEXING=True` fosse ativado concomitantemente com `DEBUG=True`.

2. **Robots.txt e Sitemap.xml:**
   - Inexistência de rota `/robots.txt`. Mecanismos de busca dependiam do comportamento padrão ou recebiam erro 404.
   - Inexistência de `/sitemap.xml`. Ausência de integração com `django.contrib.sitemaps`.
   - Risco de expor a rota administrativa configurável (`DJANGO_ADMIN_URL`) caso o robots tentasse desautorizá-la explicitamente.

3. **Arquitetura de Metadados e Redes Sociais:**
   - O `<title>` e `<meta name="description">` eram renderizados de forma simplificada no `templates/base/base.html`, sem suporte hierárquico consolidado.
   - Total ausência de meta tags Open Graph (`og:title`, `og:description`, `og:image`, `og:type`, `og:url`, `og:site_name`, `og:locale`).
   - Total ausência de meta tags do Twitter Cards (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`).
   - Ausência de meta tags de verificação para Google Search Console e Bing Webmaster Tools.

4. **URL Canônica e Parametrização:**
   - A tag `<link rel="canonical">` utilizava `{{ SITE_URL }}{{ request.path }}`, o que é vulnerável caso parâmetros de busca (`?q=...`) ou rastreamento (`?utm_source=...`) afetem a indexação de páginas duplicadas.
   - Resultados de pesquisa interna (`/conteudos/?q=termo`) não aplicavam a diretiva `noindex, follow`.

5. **Dados Estruturados (JSON-LD):**
   - Não havia nenhuma tag `<script type="application/ld+json">` no código-fonte.
   - Ausência de templatetag com proteção estrita contra Cross-Site Scripting (XSS) em dados JSON serializados (necessidade de escapar `</` como `\u003c/`).

6. **Integridade Ética:**
   - Risco comum em projetos de saúde de incluir dados fictícios de médicos (CRM), avaliações artificiais (`aggregateRating`) ou cidades inventadas. Deve-se assegurar conformidade com a regulamentação do CFP e a realidade institucional.

---

## 3. PLANO DE REMEDIAÇÃO TÉCNICA

| Item | Ação Técnica | Arquivo Envolvido |
|---|---|---|
| **Ambientes** | Criar `SEO_ALLOW_INDEXING`, `GOOGLE_SITE_VERIFICATION`, `BING_SITE_VERIFICATION`, `django.contrib.sitemaps` e normalizar `SITE_URL` | `configuracoes/settings/base.py`, `.env.example` |
| **System Checks** | Implementar `seo.E001`, `seo.E002` e `seo.W001` via `django.core.checks` | `nucleo/checks.py`, `nucleo/apps.py` |
| **Header HTTP** | Implementar `SEOMiddleware` injetando `X-Robots-Tag` | `nucleo/middleware.py` |
| **Robots.txt** | Rota `/robots.txt` dinâmica respeitando `SEO_ALLOW_INDEXING` sem expor URL secreta do admin | `nucleo/views.py`, `templates/seo/robots.txt`, `configuracoes/urls.py` |
| **Sitemap.xml** | Configurar `PaginasSitemap`, `ServicosSitemap`, `ConteudosSitemap`, `CategoriasSitemap` | `nucleo/sitemaps.py`, `configuracoes/urls.py` |
| **Base Template** | Centralizar title hierárquico, descriptions, canonical limpo, Open Graph, Twitter e verificações | `templates/base/base.html` |
| **JSON-LD** | Templatetags `render_json_ld` e `build_absolute_url` com serialização e escape anti-XSS | `nucleo/templatetags/seo_tags.py` |
| **Esquemas Schema** | Adicionar `@graph` com `WebSite`, `Organization`, `Person`, `Service`, `BlogPosting`, `ContactPage`, `BreadcrumbList` | Templates de cada seção e base |
| **Páginas Específicas** | Aplicar `noindex, follow` em busca interna e páginas legais, e `noindex, nofollow` em erros | Views de `conteudos`, `paginas`, `nucleo` |
| **Testes** | Suíte completa com 100% de cobertura nos requisitos de SEO | `nucleo/tests_seo.py` |

---

## 4. CONCLUSÃO DA AUDITORIA

A base do projeto é sólida, modular e limpa. A introdução do módulo de SEO Técnico não requer alterações estruturais de banco de dados (zero migrações de modelo), respeita o design system existente e eleva o nível de maturidade do Instituto Mente em Foco para padrões de excelência técnica e conformidade regulatória.
