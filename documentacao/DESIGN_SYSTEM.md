# DESIGN SYSTEM & GUIA DE ESTILO — INSTITUTO MENTE EM FOCO
**DOCUMENTO DE ESPECIFICAÇÃO DE TOKENS, TIPOGRAFIA, COMPONENTES E ACESSIBILIDADE**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA CSS

---

## 1. PRINCÍPIOS DE DESIGN E IDENTIDADE VISUAL

A estética do **Instituto Mente em Foco** é definida pelo conceito tríplice:

$$\text{PSICOLOGIA CONTEMPORÂNEA} + \text{EDITORIAL PREMIUM} + \text{CLÍNICA HUMANA}$$

* **Acolhimento Sereno:** Ambientes visuais claros, confortáveis e aconchegantes que diminuem a ansiedade do visitante.
* **Maturidade e Rigor Ético:** Tipografia serifada nobre aliada à limpeza da sans-serif, sem apelos sensacionalistas de marketing, promessas irreais ou elementos agressivos de conversão.
* **Espaço Negativo Generoso:** Grandes áreas de respiro vertical (`clamp(4rem, 6vw, 6.5rem)`), valorizando o ritmo de leitura editorial e a contemplação.
* **Equilíbrio Fotográfico:** O design integra a fotografia como protagonista da composição, reservando espaços com `aspect-ratio` nativo (prevenção absoluta de CLS - *Cumulative Layout Shift*).

---

## 2. ARQUITETURA CSS MODULAR

Os arquivos de folha de estilo estão organizados em `static/css/` com responsabilidades estritas e ordem de carregamento previsível no template `templates/base/base.html`:

| Ordem | Arquivo | Finalidade e Responsabilidade |
| :---: | :--- | :--- |
| **1** | [`tokens.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/tokens.css) | Centralização de variáveis CSS (`:root`): paleta de 6 cores, semântica, escala clamp, espaçamentos, radius e sombras. |
| **2** | [`base.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/base.css) | Reset moderno, regras globais de `html`/`body`, acessibilidade (`:focus-visible`, `.skip-link`, `.sr-only`), formulários base e reduced-motion. |
| **3** | [`tipografia.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/tipografia.css) | Hierarquia de títulos (`.titulo-hero`, `.titulo-display`, `.titulo-secao`), `.eyebrow`, parágrafos lead, citações e assinaturas. |
| **4** | [`layout.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/layout.css) | Containers (`.container`, `.container-largo`, `.container-texto`), grids (`.grid-2`, `.grid-cards`), seções (`.secao--clara`, `.secao--areia`, `.secao--verde`) e ritmo (`.flow`). |
| **5** | [`componentes.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/componentes.css) | Componentes de interface: botões (`.btn`), cards (`.card-servico`, `.card-foto`, `.card-identificacao`), frames de mídia e `.placeholder-imagem`. |
| **6** | [`utilitarios.css`](file:///c:/Users/andre/Documents/SiteDjangoLeide/static/css/utilitarios.css) | Classes utilitárias mínimas e indispensáveis (alinhamentos, visibilidade responsiva, ponto focal). |

---

## 3. DESIGN TOKENS — PALETA DE CORES

### 3.1 Cores Primitivas Homologadas
* **Bege Areia (`--cor-areia`):** `#D8C5A8` — Tom natural, acolhedor e orgânico; ideal para blocos de apoio e respiros suaves.
* **Off-White (`--cor-off-white`):** `#F7F3EB` — Superfície principal do site; iluminação natural sem a frieza artificial do branco 100%.
* **Verde Sálvia (`--cor-salvia`):** `#A8B09A` — Verde botânico suave para elementos de apoio, ícones e harmonia visual.
* **Verde Oliva Profundo (`--cor-oliva`):** `#56664B` — Cor institucional nobre; aplicada em títulos de destaque, botões primários e rodapé escuro.
* **Dourado Champagne (`--cor-dourado`):** `#C9A86A` — Detalhe nobre refinado; aplicado em linhas delicadas, numeração de passos e detalhes de assinatura.
* **Marrom Taupe (`--cor-taupe`):** `#6D655B` — Neutro terroso equilibrado; cor de texto secundário, rótulos e bordas elegantes.

### 3.2 Tokens Semânticos
```css
/* Superfícies e Fundos */
--cor-fundo-principal: var(--cor-off-white);
--cor-fundo-secundario: #EFE9DE;
--cor-fundo-areia: var(--cor-areia);
--cor-fundo-verde: var(--cor-oliva);
--cor-superficie: #FFFFFF;
--cor-overlay-foto: linear-gradient(180deg, rgba(45, 41, 38, 0.05) 0%, rgba(45, 41, 38, 0.65) 100%);

/* Tipografia e Textos */
--cor-texto-principal: #2D2926;  /* Café escuro orgânico, alto contraste (WCAG AA > 7:1) */
--cor-texto-secundario: #5E5953; /* Taupe médio para parágrafos */
--cor-texto-suave: #7D766D;      /* Metadados, datas e notas */
--cor-texto-claro: var(--cor-off-white); /* Textos sobre fundo verde escuro */
--cor-titulo: var(--cor-oliva);

/* Bordas e Ações */
--cor-borda: rgba(109, 101, 91, 0.2);
--cor-borda-suave: rgba(109, 101, 91, 0.12);
--cor-acao: var(--cor-oliva);
--cor-acao-hover: #44523B;
--cor-whatsapp: #4D6B42;
--cor-whatsapp-hover: #3C5533;
--cor-focus: var(--cor-oliva);
--cor-erro: #9C3D3D;
--cor-erro-fundo: #FBF2F2;
```

---

## 4. TIPOGRAFIA E ESCALA MODULAR

### 4.1 Famílias Tipográficas
* **Títulos, Cabeçalhos e Citações:** `'Cormorant Garamond', Georgia, 'Times New Roman', serif;`
  * Pesos carregados: `400`, `500`, `600`, `700`, `400i`, `600i`.
* **Textos, Navegação, Botões e Rótulos:** `'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
  * Pesos carregados: `400`, `500`, `600`.
* **Estratégia de Performance:** Pré-conexão (`preconnect`) e `font-display: swap` no `base.html` garantem que a renderização não seja bloqueada.

### 4.2 Escala Tipográfica Fluida (com `clamp`)
* `--fonte-xs`: `clamp(0.75rem, 0.72rem + 0.15vw, 0.8125rem)` (~12-13px)
* `--fonte-sm`: `clamp(0.8125rem, 0.78rem + 0.2vw, 0.875rem)` (~13-14px)
* `--fonte-base`: `clamp(0.9375rem, 0.9rem + 0.2vw, 1rem)` (~15-16px)
* `--fonte-md`: `clamp(1.0625rem, 1rem + 0.3vw, 1.1875rem)` (~17-19px)
* `--fonte-lg`: `clamp(1.25rem, 1.15rem + 0.5vw, 1.4375rem)` (~20-23px)
* `--fonte-xl`: `clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)` (~24-30px)
* `--fonte-2xl`: `clamp(1.875rem, 1.6rem + 1.2vw, 2.5rem)` (~30-40px)
* `--fonte-3xl`: `clamp(2.25rem, 1.85rem + 1.8vw, 3.25rem)` (~36-52px)
* `--fonte-hero`: `clamp(2.5rem, 1.95rem + 2.5vw, 4.25rem)` (~40-68px)

---

## 5. ESPAÇAMENTO, CONTAINERS E GRIDS

### 5.1 Escala de Espaçamento
* `--espaco-1`: `0.25rem` (4px)
* `--espaco-2`: `0.5rem` (8px)
* `--espaco-3`: `0.75rem` (12px)
* `--espaco-4`: `1rem` (16px)
* `--espaco-5`: `1.25rem` (20px)
* `--espaco-6`: `1.5rem` (24px)
* `--espaco-8`: `2rem` (32px)
* `--espaco-10`: `2.5rem` (40px)
* `--espaco-12`: `3rem` (48px)
* `--espaco-16`: `4rem` (64px)
* `--espaco-20`: `5rem` (80px)
* `--espaco-24`: `6rem` (96px)

### 5.2 Seções Editoriais e Respiro
* `--secao-y-sm`: `clamp(2.5rem, 4vw, 4rem)`
* `--secao-y-md`: `clamp(4rem, 6vw, 6.5rem)`
* `--secao-y-lg`: `clamp(5rem, 8vw, 8.5rem)`

### 5.3 Containers
* `.container`: Largura máxima de `1280px` com padding inline responsivo `clamp(1rem, 3vw, 2.5rem)`.
* `.container-largo`: Largura máxima de `1440px` para galerias e composições fotográficas amplas.
* `.container-texto`: Largura máxima de `720px` para garantir a meta de 60 a 75 caracteres por linha em leituras longas.

---

## 6. GUIA DE COMPONENTES E EXEMPLOS HTML

### 6.1 Botões e Ações (`.btn`)
```html
<!-- Botão Primário (Verde Oliva Profundo) -->
<a href="#" class="btn btn--primario">Quero conhecer o atendimento</a>

<!-- Botão Secundário (Contorno Oliva) -->
<a href="#" class="btn btn--secundario">Conhecer especialidades</a>

<!-- Botão WhatsApp (Verde Botânico Elegante) -->
<a href="#" class="btn btn--whatsapp">Falar no WhatsApp</a>

<!-- Botão Dourado/Areia (para seções escuras) -->
<a href="#" class="btn btn--dourado">Agende seu atendimento</a>

<!-- Link com Seta Indicadora -->
<a href="#" class="link-seta">
  Saiba mais sobre a consulta
  <span class="link-seta__icone" aria-hidden="true">→</span>
</a>
```

### 6.2 Eyebrow e Títulos Editoriais
```html
<header class="section-header section-header--esquerda">
  <span class="eyebrow">COMPREENDER • CUIDAR • RECONSTRUIR</span>
  <h1 class="titulo-hero">Você não precisa permanecer preso ao que viveu.</h1>
  <p class="texto-lead">A psicoterapia e a avaliação neuropsicológica oferecem caminhos seguros...</p>
</header>
```

### 6.3 Cards de Identificação Emocional (Fileira da Referência)
```html
<div class="fileira-identificacao">
  <div class="card-identificacao">
    <div class="card-identificacao__icone" aria-hidden="true">
      <svg width="24" height="24">...</svg>
    </div>
    <p class="card-identificacao__texto">"Meu relacionamento terminou e não sei como recomeçar."</p>
  </div>
</div>
```

### 6.4 Cards de Serviço e Especialidades Clínicas
```html
<div class="card card-servico">
  <div>
    <div class="card-servico__icone" aria-hidden="true">
      <svg width="24" height="24">...</svg>
    </div>
    <h4 class="titulo-card">Psicoterapia Individual</h4>
    <p class="card-servico__descricao">Espaço seguro de escuta para elaborar dores e crises.</p>
  </div>
  <a href="#" class="link-seta">
    Conhecer atendimento
    <span class="link-seta__icone" aria-hidden="true">→</span>
  </a>
</div>
```

### 6.5 Cards Fotográficos com Overlay (`.card-foto`)
```html
<a href="#" class="card-foto">
  <img src="foto.jpg" alt="Atendimento em Psicologia">
  <div class="card-foto__overlay"></div>
  <div class="card-foto__conteudo">
    <span class="badge badge--escuro card-foto__badge">Atendimento</span>
    <h4 class="card-foto__titulo">Psicologia</h4>
    <span class="link-seta" style="color: var(--cor-areia);">Ver detalhes →</span>
  </div>
</a>
```

### 6.6 Componente Oficial de Placeholder Temporário de Mídia
```html
<div class="media-frame ratio-4-5">
  <div class="placeholder-imagem">
    <span class="placeholder-imagem__codigo">IMG-001</span>
    <span class="placeholder-imagem__descricao">Foto Principal — Mari Menezes</span>
    <span class="placeholder-imagem__ratio">Proporção 4:5 (Vertical)</span>
  </div>
</div>
```

### 6.7 Passos Editoriais (`.step`)
```html
<div class="step">
  <span class="step__numero">01</span>
  <h3 class="step__titulo">Conversar</h3>
  <p class="step__descricao">O primeiro contato para expor o momento atual e alinhar o cuidado.</p>
</div>
```

---

## 7. ACESSIBILIDADE E RESPONSIVIDADE

* **WCAG 2.1 Nível AA:** Todos os pares de texto/fundo homologados possuem contraste superior a 4.5:1 (texto normal) e 3:1 (títulos grandes).
* **Navegação por Teclado:** Foco visível global ativo com `:focus-visible { outline: 2px solid var(--cor-focus); outline-offset: 3px; }`.
* **Skip Link:** Implementado no topo de `base.html` saltando direto para o `#conteudo-principal`.
* **Prevenção de Movimento Vestibular:** Suporte nativo a `@media (prefers-reduced-motion: reduce)` desabilitando animações desnecessárias.
* **Tamanhos Testados e Homologados:**
  * Mobile: `320px`, `360px`, `390px`, `430px`.
  * Tablet: `768px`.
  * Laptop/Desktop: `1024px`, `1280px`, `1440px`.
  * Ultrawide: `1920px+`.
  * Ausência total de overflow horizontal (`box-sizing: border-box`, larguras fluidas).

---

## 8. LABORATÓRIO VISUAL (`/design-system/`)

* **URL de Desenvolvimento:** `http://127.0.0.1:8000/design-system/`
* **Controle de Ambiente:** Acesso restrito a instâncias rodando com `DEBUG = True`. Em ambiente de produção (`DEBUG = False`), o Django retorna imediatamente **HTTP 404**, protegendo os testes visuais internos.

---

## 9. COMPONENTES GLOBAIS DE INTERFACE (PROMPT 04)

### 9.1 Header Institucional (`.cabecalho-site`)
* **Posicionamento:** `position: sticky; top: 0; z-index: 100;` com altura fixa de `84px`.
* **Superfície e Acabamento:** Fundo off-white translúcido (`rgba(247, 246, 242, 0.94)`) com suporte a `backdrop-filter: blur(12px)` e borda inferior sutil (`1px solid var(--cor-borda)`).
* **Estrutura:** Logo à esquerda com tipografia de fallback nobre (*Cormorant Garamond*), menu horizontal desktop ao centro/direita, botão CTA "Agendar atendimento" e acionador mobile hambúrguer acessível.

### 9.2 Navegação Desktop (`.navegacao-principal`)
* **Breakpoint:** Visível e alinhado horizontalmente em viewports $\ge 1080px$. Em telas menores, oculta para preservar o layout e cede lugar ao menu mobile.
* **Estado Ativo:** Indicado visualmente por sublinhado sutil em `--cor-dourado` e programmaticamente com `aria-current="page"`.
* **Tipografia:** `Montserrat`, 500/600, 0.9rem, com tracking suave e contraste validado WCAG AA.

### 9.3 Menu Mobile Drawer (`.menu-mobile`)
* **Mecanismo:** Painel lateral deslizante off-white com largura `min(380px, 86vw)`, sombreamento profundo e backdrop escuro com blur (`.menu-mobile__backdrop`).
* **Acessibilidade:**
  * Controlado via `aria-expanded` e `aria-controls="menu-mobile-painel"`.
  * Fechamento automático via tecla `Escape`, clique no backdrop ou seleção de links de navegação.
  * Restauração de foco ao botão disparador (`#menu-mobile-toggle`).
  * Bloqueio de rolagem do body (`overflow: hidden`) durante a abertura.
  * Fechamento automático caso a viewport seja redimensionada acima de 1080px.

### 9.4 Rodapé Institucional (`.rodape-site`)
* **Superfície:** Fundo `--cor-oliva` com tipografia clara em `--cor-areia` e `--cor-off-white`.
* **Grid de 4 Colunas:**
  1. Identidade institucional, síntese da proposta clínica e registro profissional da Psicóloga Mari Menezes (CRP).
  2. Links rápidos de navegação institucional.
  3. Áreas de atuação e serviços clínicos.
  4. Canais diretos de atendimento (WhatsApp, e-mail, horário) e redes sociais verificadas.
* **Barra de Direitos:** Divisor dourado sutil, ano dinâmico `{% now "Y" %}` e link obrigatório para a Política de Privacidade.

### 9.5 Botão Flutuante do WhatsApp (`.btn-whatsapp-flutuante`)
* **Posicionamento:** Canto inferior direito fixo (`bottom: 24px; right: 24px; z-index: 90;`).
* **Visual:** Ícone vetorial SVG do WhatsApp em fundo `--cor-oliva` / `--cor-salvia` sofisticado (sem tons néon vulgares), sombra suave e tooltip acessível "Fale conosco pelo WhatsApp".
* **Condição de Exibição:** Renderizado estritamente quando `WHATSAPP_LINK` estiver preenchido no CMS (sem exibir botões quebrados para números vazios ou pendentes).

---

## 10. DIRETRIZES DE PERFORMANCE E ESTABILIDADE VISUAL (PROMPT 15)

* **Estabilidade Dimensional (CLS = 0):** Todos os componentes de mídia utilizam classes nativas (`.media-frame`, `.ratio-4-5`, `.ratio-16-9`, `.ratio-4-3`) com `aspect-ratio` CSS explícito, garantindo que o espaço físico esteja previamente reservado antes do carregamento de qualquer imagem.
* **Priorização do LCP:** Slots visuais acima da dobra (como o retrato Hero na Home e capas de serviços/artigos) utilizam `loading="eager"`, `fetchpriority="high"` e `decoding="async"`.
* **Carregamento Diferido (Lazy Loading):** Todos os componentes abaixo da dobra utilizam `loading="lazy"` e `decoding="async"` nativos.
* **Respeito a Movimento Reduzido:** Em `@media (prefers-reduced-motion: reduce)`, todas as transições e animações são neutralizadas (`0.01ms`), garantindo acessibilidade vestibular sem custos de repaint.

---

## 11. DIRETRIZES DE RESPONSIVIDADE UNIVERSAL E COMPATIBILIDADE CROSS-BROWSER (PROMPT 19)

* **Estratégia Mobile-First Rigorosa:** Todos os estilos base são definidos primariamente para viewports compactos (320px+), expandindo-se progressivamente através de `@media (min-width: ...)`.
* **Zero Overflow Horizontal Destrutivo:** Nenhum elemento do DOM viola a restrição `scrollWidth <= clientWidth`. O transbordamento é prevenido em nível de componente com `max-width: 100%`, `overflow-wrap: break-word` e grids adaptativos.
* **Prevenção de Auto-Zoom em WebKit (iOS):** Todos os campos de entrada (`.form-input`, `.form-select`, `.form-textarea`, `.barra-busca__input`) possuem `font-size: 1rem` (16px), impedindo que o Safari mobile execute zoom involuntário durante o foco.
* **Ergonomia e Touch Targets (WCAG 2.5.8):** Todos os botões, links de cabeçalho/rodapé e ícones interativos possuem área de toque mínima cravada em **44x44px** (ou 48x48px no caso dos botões de ação primários).
* **Safe Area Insets e Entalhes de Tela:** Elementos fixos (como `.whatsapp-flutuante`) utilizam `env(safe-area-inset-*, 0px)` com fallback defensivo para acomodar perfeitamente dynamic island, notches e gestos de navegação inferior.
* **Reflow a 200% (WCAG 1.4.10):** A arquitetura visual suporta ampliação de até 200% em tela de 1280px (equivalente ao viewport de 320px) sem colisão de textos, sem truncamento de títulos e sem surgimento de barras de rolagem bidirecionais.

---

## 12. CONSOLIDAÇÃO DE DESIGN TOKENS E POLIMENTO VISUAL FINAL (PROMPT 20)

### 12.1 Normalização e Unificação de Tokens Globais
* **Restauração da Variável Crítica `--fonte-titulo`:** Mapeamento explícito de `--fonte-titulo: var(--fonte-display);` em `tokens.css`, restabelecendo a família serifada nobre *Cormorant Garamond* em todos os títulos H1, H2 e H3 do site, em conformidade com a imagem de referência.
* **Aliases Semânticos Globais:** Criação de aliases de retrocompatibilidade em `tokens.css` (`--cor-branco: var(--cor-superficie);`, `--cor-areia-clara: var(--cor-fundo-secundario);`, `--cor-oliva-profundo: var(--cor-oliva);`, `--cor-texto: var(--cor-texto-principal);`, `--espaco-14: 3.5rem;`, `--radius-full: var(--radius-pill);`, `--raio-sm`, `--raio-md`, `--raio-lg`, `--raio-completo`, `--sombra-sm`, `--sombra-md`, `--sombra-lg`, `--transicao-normal`, `--largura-conteudo`).
* **Expurgo de Cores Hardcoded:** Eliminação de declarações hexadecimais isoladas (`#2C3C30`, `#B8965A`, `#E2DED4`) em `contato.css` e `conteudos.css`, substituídas por `var(--cor-oliva)`, `var(--cor-dourado)` e `var(--cor-borda-suave)`.

### 12.2 Padronização de Componentes e Interações
* **Botão de Retorno (`.botao-retorno`):** Unificado em `base.css` com `display: inline-flex; align-items: center; min-height: 48px; gap: 0.5rem;` e microinteração de recuo suave da seta à esquerda no hover.
* **Gradientes de Cabeçalho:** Sincronização uniforme dos cabeçalhos em `paginas_internas.css`, `home.css` e `conteudos.css` com `linear-gradient(180deg, var(--cor-fundo-secundario) 0%, var(--cor-off-white) 100%)`.
* **Citação Flutuante sobre Mídia:** Ajuste de contraste com opacidade reforçada `rgba(247, 243, 235, 0.95)`, `backdrop-filter: blur(8px)`, borda dourada suave e sombra moderada.
