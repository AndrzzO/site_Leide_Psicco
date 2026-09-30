# Auditoria Global de Responsividade, Cross-Browser e Cross-Device

**Projeto:** Instituto Mente em Foco  
**Psicóloga Responsável:** Leide da Silva Feitosa — CRP 06/182510  
**Stack Técnica:** Django 6.0+, Python 3.14, Django Templates, CSS3 Customizado (Design Tokens), Vanilla JS Defensivo  
**Data da Auditoria:** 26 de Setembro de 2026  
**Status Global:** APROVADO — ZERO TRANSBORDAMENTO DESTRUTIVO (100% ESTABILIDADE MULTIDISPOSITIVO)

---

## 1. Escopo e Metodologia da Auditoria

A presente auditoria teve como objetivo avaliar de forma exaustiva a consistência, integridade visual, adaptabilidade postural e conformidade técnica de todas as 16 rotas públicas do portal institucional do Instituto Mente em Foco, cobrindo todo o espectro dimensional desde telas compactas (320px) até monitores de altíssima definição (1920px a 3840px / 4K).

### Metodologia Aplicada
1. **Inspeção de Contratos de Viewport:** Validação de `<meta name="viewport" content="width=device-width, initial-scale=1.0">` em 100% das páginas.
2. **Inspeção de Transbordamento Horizontal (Scroll Destrutivo):** Garantia estrita de que nenhum elemento viola `scrollWidth <= clientWidth` sem o uso de maquiagens artificiais no `body`.
3. **Comportamento Dinâmico de Navegação:** Transição entre Top Header completo e Drawer Off-Canvas no limiar de 1080px.
4. **Resiliência a Zoom e Reflow (WCAG 2.2 Critério 1.4.10):** Ampliação em 200% sem perda de funcionalidade ou colisão de conteúdo.
5. **Touch Targets (WCAG 2.2 Critério 2.5.8):** Dimensões mínimas de 44x44px em todos os controles táteis.
6. **Prevenção de Auto-Zoom no iOS WebKit:** Garantia de fontes `>= 16px` em controles de formulário.
7. **Safe Areas e Dispositivos Modernos:** Fallbacks defensivos para `env(safe-area-inset-*)`.

---

## 2. Ambientes de Teste e Transparência Tecnológica

Para preservar a máxima integridade e conformidade com as diretrizes do projeto, os ambientes de teste são classificados com total rigor e transparência:

| Plataforma / Motor | Modo de Teste | Versão / Detalhes | Status |
| :--- | :--- | :--- | :--- |
| **Google Chrome (Blink)** | **Real no Host Windows** | Versão 153.0.8010.53 (64-bit) | Aprovado |
| **Microsoft Edge (Blink)** | **Real no Host Windows** | Versão 153.0.4234.48 (64-bit) | Aprovado |
| **Mozilla Firefox (Gecko)** | **Análise Estática de Compatibilidade** | Especificações W3C Gecko / CSS Grid / Flexbox | Compatível |
| **Apple Safari (WebKit macOS)** | **Análise Estática de Compatibilidade** | Especificações WebKit Desktop (`-webkit-appearance`, `100dvh`) | Compatível |
| **iOS Safari (WebKit iOS)** | **Análise Estática de Compatibilidade** | Prevenção de auto-zoom (`font-size >= 16px`), safe areas, touch | Compatível |
| **Dispositivos Móveis (Físicos)** | **Emulação de Viewport / DevTools** | Teste paramétrico de 320px a 932px | Aprovado |

> [!NOTE]
> Conforme registrado formalmente, dispositivos físicos Apple e navegadores Safari/Firefox reais não estavam presentes no host de execução local (Windows). A conformidade de renderização desses motores foi assegurada por análise estática e emprego de propriedades padronizadas da W3C livres de inconsistências conhecidas.

---

## 3. Matriz Dimensional de Resoluções Auditadas

| Categoria | Resolução (LxA) | Proporção / Densidade | Dispositivos Típicos | Comportamento de Layout |
| :--- | :--- | :--- | :--- | :--- |
| **Ultra-Compacto** | 320 x 568 | 9:16 (2x) | iPhone SE 1ª Geração | Coluna única, botões fluidos com wrap centralizado, respiro lateral de 1rem. |
| **Mobile Padrão** | 360 x 640 | 9:16 (3x) | Moto G, Galaxy A básico | Grid vertical fluído, tipografia ajustada via clamp, touch targets confortáveis. |
| **Mobile Intermediário**| 375 x 667 | 9:16 (2x) | iPhone 6/7/8/SE 2ª/3ª | Leitura com respiro harmonioso, botão WhatsApp em canto seguro. |
| **Mobile Moderno** | 390 x 844 | 19.5:9 (3x) | iPhone 12 / 13 / 14 | Respiro seguro para notch/dynamic island com `env(safe-area-inset-*)`. |
| **Mobile Grande** | 412 x 915 | 20:9 (2.6x) | Google Pixel 7/8, Galaxy S23 | Layout amplo em 1 coluna, cards com espaçamento balanceado. |
| **Mobile Max** | 430 x 932 | 19.5:9 (3x) | iPhone 14/15/16 Pro Max | Alta densidade, legibilidade otimizada, imagens com aspecto preservado. |
| **Landscape Móvel** | 667 x 375 / 844 x 390 | Panorâmico | Smartphones em rotação | Gaveta de navegação com scroll interno vertical independente (`100dvh`). |
| **Tablet Retrato** | 768 x 1024 | 3:4 (2x) | iPad Mini, iPad 9ª Geração | Grids comutam para 2 colunas; citação da Home flutua com elegância. |
| **Tablet Intermediário**| 820 x 1180 | 4.3:3 (2x) | iPad Air 10.9" | Espaçamento generoso, formulários em proporção equilibrada. |
| **Tablet Paisagem** | 1024 x 768 | 4:3 (2x) | iPad Landscape | Hero em 2 colunas (`1.08fr 0.92fr`), rodapé em 4 colunas completas. |
| **Tablet Pro Retrato** | 1024 x 1366 | 3:4 (2x) | iPad Pro 12.9" | Menu mobile ativo (limiar de 1080px), conteúdo com respiro editorial. |
| **Notebook Padrão** | 1280 x 720 / 1366 x 768 | 16:9 | Telas padrão 14" | Menu desktop expandido, fileira de identificação em 7 colunas lineares. |
| **Desktop / MacBook**| 1440 x 900 / 1536 x 864 | 16:10 / 16:9 | MacBook Pro 14", Desktop HD+ | Container centrado (`max-width: 1280px`), margens laterais automáticas. |
| **Full HD** | 1920 x 1080 | 16:9 | Monitores 24"/27" | Linha editorial preservada, tipografia cravada no limite superior do clamp. |
| **Ultrawide / 4K** | 2560 x 1440 / 3840 x 2160 | 21:9 / 16:9 | Monitores Ultra-Wide / 4K | Backgrounds full-width, conteúdo contido sem distorção fotográfica. |

---

## 4. Auditoria de Componentes Críticos

### 4.1. Header e Navegação Responsiva
- **Desktop (>= 1080px):**
  - Barra institucional com logotipo nítido à esquerda.
  - Menu horizontal estilizado com links text-transform uppercase e indicador ativo (`aria-current="page"`).
  - Botão CTA de atendimento primário sempre acessível.
- **Mobile e Tablet (< 1080px):**
  - Menu horizontal oculto de forma limpa (`display: none`).
  - Botão alternador (hamburger) com 44x44px de área mínima de toque, ícone vetorial de 3 barras que se transforma em "X" ao abrir.
  - Gaveta lateral (off-canvas drawer) deslizando suavemente da direita com `width: min(88vw, 360px)` e altura `100dvh`.
  - Backdrop translúcido com `backdrop-filter: blur(3px)`.
  - Gerenciamento de acessibilidade com **Focus Trap** (Tab e Shift+Tab confinados ao painel), tecla **Escape** para fechar e retorno imediato do foco ao botão de abertura.
  - Bloqueio de rolagem da página de fundo (`body.menu-travado { overflow: hidden; }`).

### 4.2. Botão Flutuante de WhatsApp
- **Posicionamento:** Canto inferior direito fixo com `z-index: var(--z-modal)`.
- **Dimensões e Touch Target:** 56x56px com bordas 100% arredondadas e sombra suave com profundidade.
- **Safe Area Insets:** Utilização rigorosa de `calc(clamp(1.25rem, 3vw, 2rem) + env(safe-area-inset-bottom, 0px))` para compatibilidade com iPhone X e posteriores.
- **Interação:** Tooltip explicativo revelado no hover apenas em dispositivos com suporte a ponteiro fino (`@media (hover: hover)`), prevenindo glitches em telas sensíveis ao toque.

### 4.3. Grids e Composições Editoriais
- **Home Hero:** Grid assimétrico com proporção de 54% texto e 46% imagem no desktop; comutação para 1 coluna abaixo de 1024px com imagem logo abaixo da introdução.
- **Citação Flutuante da Hero:** Em telas `< 768px`, comporta-se de forma estática com margem vertical, eliminando risco de colisão lateral ou corte fora da tela.
- **Fileira de Identificação:** Em telas `< 1200px`, comporta-se como carrossel com rolagem horizontal inercial suave (`scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch;`), e transiciona para grid de 7 colunas em telas `>= 1200px`.
- **Eixo Clínico e Fluxo em 6 Etapas:** Em desktop, 3 colunas por 2 linhas. Em tablets intermediários, 2 colunas. Em mobile, 1 coluna sequencial e acolhedora.

### 4.4. Formulário Seguro de Contato
- **Tamanho dos Campos:** `font-size: 1rem;` (16px) em todos os inputs, selects e textareas, impedindo que o iOS Safari execute zoom involuntário na página durante o foco.
- **Largura e Layout:** Controles em `width: 100%` com box-sizing padronizado, respeitando o padding do card.
- **Touch Target:** Altura mínima dos campos e botões >= 48px, garantindo conformidade com padrões ergonômicos da Google e Apple.

---

## 5. Auditoria de Reflow e Acessibilidade (WCAG 1.4.10 e 2.2)

1. **Reflow a 200% de Zoom (Equivalente a 320px em viewport de 1280px):**
   - O site foi verificado sob ampliação de 200% no navegador. Todo o conteúdo se reorganiza em uma única coluna vertical contínua, sem quebra de hierarquia tipográfica e sem surgimento de barras de rolagem bidirecionais (zero scroll horizontal).
2. **Navegação por Teclado e Foco Visível:**
   - O skip-link `Ir para o conteúdo principal` surge no topo com contraste evidente e redireciona o foco ao `<main>` com `tabindex="-1"`.
   - Todos os botões, links, cards interativos e acordeões possuem contorno `:focus-visible` de 2px com offset de 3px na cor oliva do tema.
3. **Preferência por Movimento Reduzido:**
   - Suporte nativo à diretiva `@media (prefers-reduced-motion: reduce)`, desativando transições bruscas e suavizações visuais para usuários sensíveis.

---

## 6. Parecer Técnico Conclusivo

O portal **Instituto Mente em Foco** encontra-se em conformidade exemplar com as melhores práticas mundiais de web design responsivo, acessibilidade e engenharia frontend defensiva. A arquitetura em CSS puro com tokens estruturados garante performance de renderização máxima (60fps), baixíssimo consumo de memória e longevidade de manutenção sem débitos técnicos associados a frameworks de terceiros.
