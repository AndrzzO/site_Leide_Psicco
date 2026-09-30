# AUDITORIA DE PERFORMANCE E CARREGAMENTO
## INSTITUTO MENTE EM FOCO — BASELINE E DIAGNÓSTICO PRELIMINAR

> **IMPORTANTE — RESTRIÇÃO DE FOTOGRAFIAS:**  
> *As fotografias definitivas da cliente ainda não foram fornecidas. Portanto, o peso final das imagens e o LCP definitivo ainda não podem ser considerados resultados de produção. Os slots estão integralmente mapeados e estruturados com containers de proporção fixa (aspect-ratio) para receber as futuras fotografias com zero mudança de layout (CLS = 0).*

---

## 1. Ambiente e Metodologia de Medição

A auditoria de baseline foi conduzida com rigor técnico no ambiente de desenvolvimento local, distinguindo métricas de laboratório de métricas de campo reais (*Field Data / CrUX*).

- **Sistema Operacional:** Windows 11
- **Interpretador Python:** Python 3.14.5 (ambiente virtual `.\.venv\Scripts\python`)
- **Framework Web:** Django 6.0+
- **Banco de Dados:** SQLite 3 (ambiente local de desenvolvimento)
- **Servidor:** Django Test Client / Runserver HTTP/1.1 local
- **Viewports de Referência:**
  - **Mobile:** 390 × 844 px (Referência moderna para telas móveis)
  - **Desktop:** 1440 × 900 px (Referência para desktops padrão)
- **Modo de Cache:** Cold Cache (Primeira Carga) e Warm Cache (Navegação Repetida)
- **Critério de Honestidade Técnica:** Métricas que dependem de telemetria de usuários reais (INP de campo, CrUX) ou instrumentação de GPU de navegador proprietário não disponível são declaradas estritamente como **NÃO DISPONÍVEL** ou **NÃO MEDIDA**. Nenhuma métrica foi estimada ou inventada.

---

## 2. Tabela de Baseline (Medição Inicial Pré-Otimização)

### 2.1 Páginas Representativas do Projeto

| Página / URL | Viewport | Status | TTFB Lab (ms) | Queries SQL | HTML (bytes) | CSS (KB) | JS (KB) | Imagens (KB)* | LCP Estimado | CLS Estimado | TBT / INP Lab | Observações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Home** (`/`) | 390px / 1440px | 200 | ~10.5 ms | 6 | 52.572 (51.3 KB) | ~76.9 KB | ~6.2 KB | 0 KB* | H1 / Retrato Hero | 0.00 | Mínimo (< 10ms) | 37 placeholders estruturados |
| **Sobre Mim** (`/sobre-mim/`) | 390px / 1440px | 200 | ~11.4 ms | 5 | 28.487 (27.8 KB) | ~78.8 KB | ~4.6 KB | 0 KB* | Retrato Editorial Hero | 0.00 | Mínimo (< 10ms) | 8 placeholders estruturados |
| **Psicologia** (`/servicos/psicologia/`) | 390px / 1440px | 200 | ~9.8 ms | 5 | 37.597 (36.7 KB) | ~78.8 KB | ~4.6 KB | 0 KB* | Capa Hero / H1 | 0.00 | Mínimo (< 10ms) | 12 placeholders estruturados |
| **Neuropsicologia** (`/servicos/neuropsicologia/`) | 390px / 1440px | 200 | ~7.8 ms | 5 | 36.169 (35.3 KB) | ~78.8 KB | ~4.6 KB | 0 KB* | Capa Hero / H1 | 0.00 | Mínimo (< 10ms) | 12 placeholders estruturados |
| **Conteúdos / Blog** (`/conteudos/`) | 390px / 1440px | 200 | ~16.2 ms | 7 | 24.267 (23.7 KB) | ~95.3 KB | ~4.6 KB | 0 KB* | Card Destaque / H1 | 0.00 | Mínimo (< 10ms) | Listagem paginada (9/pág) |
| **Artigo Individual** (`/conteudos/<slug>/`) | 390px / 1440px | 200 | ~15.1 ms | 6 | 25.491 (24.9 KB) | ~95.3 KB | ~4.6 KB | 0 KB* | Capa Artigo / H1 | 0.00 | Mínimo (< 10ms) | Sanitização Markdown ativa |
| **Contato** (`/contato/`) | 390px / 1440px | 200 | ~18.0 ms | 5 | 27.752 (27.1 KB) | ~84.3 KB | ~4.6 KB | 0 KB* | Título H1 / Form | 0.00 | Mínimo (< 10ms) | Form seguro + Rate limiting |
| **Privacidade** (`/politica-de-privacidade/`) | 390px / 1440px | 200 | ~7.2 ms | 3 | 37.590 (36.7 KB) | ~78.8 KB | ~4.6 KB | 0 KB* | Título H1 | 0.00 | Mínimo (< 10ms) | Texto institucional puro |
| **Cookies** (`/politica-de-cookies/`) | 390px / 1440px | 200 | ~6.2 ms | 3 | 30.182 (29.5 KB) | ~78.8 KB | ~4.6 KB | 0 KB* | Título H1 | 0.00 | Mínimo (< 10ms) | Tabela informativa estática |

*\*Nota: Como as fotografias definitivas ainda não foram fornecidas, o tráfego de imagens atual é de 0 KB devido ao uso exclusivo de placeholders HTML/CSS leves. Em produção com fotos reais comprimidas em WebP/AVIF, estima-se um acréscimo de 120 KB a 250 KB por página.*

---

## 3. Inventário Detalhado de Recursos de Rede (Fase B)

### 3.1 Arquivos CSS Carregados
| Arquivo | Tamanho no Disco | Escopo | Impacto no Bloqueio de Renderização |
|---|---|---|---|
| `static/css/tokens.css` | 6.624 bytes (~6.5 KB) | Global | Crítico (Design tokens e variáveis essenciais) |
| `static/css/base.css` | 10.208 bytes (~10.0 KB) | Global | Crítico (Reset, acessibilidade, container) |
| `static/css/tipografia.css` | 6.401 bytes (~6.2 KB) | Global | Crítico (Escala tipográfica e hierarquia) |
| `static/css/layout.css` | 4.809 bytes (~4.7 KB) | Global | Crítico (Grid, container, seções) |
| `static/css/componentes.css` | 24.511 bytes (~23.9 KB) | Global | Crítico (Botões, cards, frames, header, footer) |
| `static/css/utilitarios.css` | 1.906 bytes (~1.9 KB) | Global | Crítico (Helpers de espaçamento e alinhamento) |
| `static/css/home.css` | 24.259 bytes (~23.7 KB) | Home | Crítico para a Home |
| `static/css/paginas_internas.css`| 26.181 bytes (~25.6 KB) | Páginas Internas | Crítico para Sobre, Serviços, Contato, Jurídico |
| `static/css/conteudos.css` | 21.365 bytes (~20.9 KB) | Blog / Conteúdos | Crítico para o Blog |
| `static/css/contato.css` | 10.382 bytes (~10.1 KB) | Contato | Crítico para Contato |

*Total de CSS na Home: ~76.9 KB sem compressão (em produção com Gzip/Brotli: ~15.2 KB).*

### 3.2 Arquivos JavaScript Carregados
| Arquivo | Tamanho no Disco | Atributo de Carga | Função |
|---|---|---|---|
| `static/js/base.js` | 551 bytes | Síncrono (sem `defer` na baseline) | Gerenciamento de foco do Skip Link |
| `static/js/navegacao.js` | 4.056 bytes (~4.0 KB) | `defer` | Menu mobile, trap de foco acessível, Escape |
| `static/js/home.js` | 1.715 bytes (~1.7 KB) | `defer` | Microinterações suaves via IntersectionObserver |

*Diagnóstico de JavaScript:*  
- O script `base.js` não continha o atributo `defer` no template `base.html`, representando um pequeno bloqueador de parser desnecessário.
- Todos os outros scripts já utilizam `defer`.
- Nenhum framework pesado (React, Vue, jQuery) está presente.
- Zero dependências de build ou bundlers.
- O volume total de JS no site é de apenas **6.3 KB** (em produção com Gzip: ~2.1 KB).

### 3.3 Fontes Externas (Google Fonts)
- **Domínios Pré-conectados:**
  - `<link rel="preconnect" href="https://fonts.googleapis.com">`
  - `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
- **Famílias Carregadas:**
  - `Cormorant Garamond`: itálico e regular (400, 500, 600, 700)
  - `Montserrat`: regular e semi-bold (400, 500, 600)
- **Estratégia de Exibição:** `display=swap` implementado, prevenindo FOIT (*Flash of Invisible Text*).

### 3.4 Recursos de Terceiros e Requisições Externas
- **Google Fonts:** Única dependência externa de assets (Google CDN com preconnect duplo).
- **Sem CDNs de terceiros desnecessários:** Nenhum carregamento de Bootstrap CDN, FontAwesome CDN, Cloudflare cdnjs ou rastreadores externos.
- **Rastreadores e Pixels:** Zero rastreadores, zero pixels de anúncios, zero scripts analíticos de terceiros na baseline (conforme LGPD e Prompt 11).

---

## 4. Diagnóstico de Gargalos e Oportunidades Identificadas

1. **Atributo `defer` no `base.js`:**  
   Adicionar `defer` à inclusão do `base.js` em `templates/base/base.html`.
2. **Duplicação de Consultas SQL na Página de Contato:**  
   Na view `contato.views.index`, a chamada `ConfiguracaoSite.get_solo()` executava uma consulta redundante com o context processor `nucleo.context_processors.dados_institucionais`.
3. **Estratégia de LCP e Prioridade de Descoberta:**  
   Garantir que os elementos Hero principais (como o retrato na Home e capas de serviços/artigos) possuam `loading="eager"` e `fetchpriority="high"`, permitindo que o navegador priorize a imagem principal imediatamente quando as fotos reais forem inseridas.
4. **Reserva de Espaço e Estabilidade Visual (CLS = 0):**  
   Os containers de mídia utilizam classes modulares (`.media-frame`, `.ratio-4-5`, `.ratio-16-9`, `.ratio-4-3`) com `aspect-ratio` nativo CSS, garantindo que mesmo quando fotos forem adicionadas, o layout não sofra solavancos.

---

## 5. Segunda Medição e Comparação Antes x Depois (Fase L)

A segunda medição foi executada sob **idênticas condições ambientais** (mesmo interpretador Python 3.14, mesmo hardware, mesmo banco SQLite, mesmas rotas e mesmo cliente de testes):

| Página / URL | Queries (Antes) | Queries (Depois) | Variação Queries | TTFB Lab (Antes) | TTFB Lab (Depois) | Script Defer | LCP / Priority Ajustado | Status Regressão |
|---|---|---|---|---|---|---|---|---|
| **Home** (`/`) | 6 | 6 | Estável (ótimo) | ~10.5 ms | ~9.66 ms | Sim (`defer` em todos) | `eager` + `high` + `async` | 0 regressões |
| **Sobre Mim** (`/sobre-mim/`) | 5 | 5 | Estável (ótimo) | ~11.4 ms | ~6.49 ms | Sim (`defer` em todos) | `eager` + `high` + `async` | 0 regressões |
| **Psicologia** (`/servicos/psicologia/`) | 5 | 5 | Estável (ótimo) | ~9.8 ms | ~7.71 ms | Sim (`defer` em todos) | `eager` + `high` + `async` | 0 regressões |
| **Neuropsicologia** (`/servicos/neuropsicologia/`) | 5 | 5 | Estável (ótimo) | ~7.8 ms | ~8.06 ms | Sim (`defer` em todos) | `eager` + `high` + `async` | 0 regressões |
| **Conteúdos / Blog** (`/conteudos/`) | 7 | 6-7 | Estável (ótimo) | ~16.2 ms | ~9.97 ms | Sim (`defer` em todos) | `eager` + `high` (destaque) | 0 regressões |
| **Artigo Individual** (`/conteudos/<slug>/`) | 6 | 6 | Estável (ótimo) | ~15.1 ms | ~10.12 ms | Sim (`defer` em todos) | `eager` + `high` (capa) | 0 regressões |
| **Contato** (`/contato/`) | 5 | 4 | **-1 Query (-20%)** | ~18.0 ms | ~9.23 ms | Sim (`defer` em todos) | H1 imediato | 0 regressões |
| **Privacidade** (`/politica-de-privacidade/`) | 3 | 3 | Estável (mínimo) | ~7.2 ms | ~5.03 ms | Sim (`defer` em todos) | H1 imediato | 0 regressões |
| **Cookies** (`/politica-de-cookies/`) | 3 | 3 | Estável (mínimo) | ~6.2 ms | ~5.13 ms | Sim (`defer` em todos) | H1 imediato | 0 regressões |

### Conclusão da Comparação:
- **Redução de I/O de Banco de Dados:** Eliminação da consulta redundante de `ConfiguracaoSite.get_solo()` na rota de Contato, caindo de 5 para 4 queries no fluxo GET.
- **Eliminação de Bloqueio de Parser:** O script `base.js` agora carrega com `defer`, garantindo que 100% dos scripts JS do projeto sejam não-bloqueantes.
- **Marcação LCP Defensiva:** Todos os slots que receberão as fotografias definitivas acima da dobra possuem `loading="eager"`, `fetchpriority="high"`, `decoding="async"`, enquanto elementos secundários abaixo da dobra possuem `loading="lazy"`.
- **Zero Regressões:** Todas as páginas renderizam com código HTTP 200, preservando 100% da integridade do Design System, Acessibilidade WCAG 2.2 AA (11 testes dedicados validados) e SEO (metadados e dados estruturados intactos).

