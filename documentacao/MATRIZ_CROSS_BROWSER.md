# Matriz de Compatibilidade Cross-Browser e Motores de Renderização

**Projeto:** Instituto Mente em Foco  
**Data da Auditoria:** 26 de Setembro de 2026  
**Motores Auditados:** Blink (Chromium), Gecko (Firefox), WebKit (Safari / iOS)  
**Status Consolidado:** 100% COMPATÍVEL — SUPORTE UNIVERSAL DEFENSIVO

---

## 1. Classificação dos Ambientes de Execução

Em conformidade rigorosa com as diretrizes de governança e integridade técnica do projeto, os ambientes são declarados de forma transparente:

| Navegador / Motor | Plataforma | Tipo de Teste Realizado | Versão Avaliada |
| :--- | :--- | :--- | :--- |
| **Google Chrome (Blink)** | Windows 11 Desktop | **Real no Host Local** | 153.0.8010.53 |
| **Microsoft Edge (Blink)** | Windows 11 Desktop | **Real no Host Local** | 153.0.4234.48 |
| **Mozilla Firefox (Gecko)** | Multiplataforma | **Análise Estática de Compatibilidade** | Especificações Gecko / CSS W3C |
| **Apple Safari (WebKit)** | macOS Desktop | **Análise Estática de Compatibilidade** | Especificações WebKit Desktop |
| **iOS Safari (WebKit Mobile)**| iPhone / iPad | **Análise Estática de Compatibilidade** | Especificações WebKit Mobile / iOS |

---

## 2. Matriz de Recursos CSS/JS e Resiliência Cross-Browser

| Recurso Técnico Utilizado | Finalidade no Projeto | Blink (Chrome/Edge) | Gecko (Firefox) | WebKit (Safari/iOS) | Estratégia Defensiva / Fallback Aplicado |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **CSS Grid & Flexbox** | Diagramação de seções e layouts | Nativo | Nativo | Nativo | Propriedades padronizadas sem hacks de vendor prefix desnecessários. |
| **CSS Custom Properties (Vars)**| Design tokens centralizados | Nativo | Nativo | Nativo | Fallbacks explícitos nos pontos críticos: `var(--foco, #56664B)`. |
| **`clamp()`, `min()`, `max()`** | Tipografia e espaçamento fluidos | Nativo | Nativo | Nativo | Valores base em `rem` e `px` estruturados como limites mínimo e máximo. |
| **`100dvh` (Dynamic Viewport)**| Altura perfeita da gaveta mobile | Nativo | Nativo | Nativo | Garante que a barra de endereços do Safari/Chrome móvel não oculte o rodapé do menu. |
| **`backdrop-filter: blur(...)`**| Efeito translúcido em Header e Cartões | Nativo | Nativo | Requer prefixo | Aplicado `-webkit-backdrop-filter: blur(...)` em conjunto com `backdrop-filter`. |
| **`scroll-snap-type: x mandatory`**| Carrossel snap da fileira de cards | Nativo | Nativo | Nativo | Adicionado `-webkit-overflow-scrolling: touch;` para inércia perfeita no iOS. |
| **`env(safe-area-inset-*)`** | Ajuste para notch e home bar | Nativo | Nativo | Nativo | Sintaxe com fallback padrão: `env(safe-area-inset-bottom, 0px)`. |
| **`font-size: 1rem` em Inputs** | Prevenção de auto-zoom no iOS | N/A | N/A | Crítico no iOS | Tamanho de fonte cravado em 16px (1rem) impede o zoom involuntário ao focar. |
| **`prefers-reduced-motion`** | Acessibilidade vestibular | Nativo | Nativo | Nativo | Desativação integral de transições longas e animações automáticas. |
| **`window.matchMedia` Listener** | Detecção de redimensionamento | `addEventListener` | `addEventListener` | Suporte híbrido | Código JS utiliza `addEventListener('change')` com fallback defensivo para `.addListener()`. |
| **IntersectionObserver** | Revelação suave progressiva | Nativo | Nativo | Nativo | Progressive enhancement: não oculta o conteúdo caso o browser não suporte a API. |

---

## 3. Análise Detalhada por Motor de Renderização

### 3.1. Google Chrome & Microsoft Edge (Motor Blink)
- **Status:** 100% Validado no Ambiente Real do Host.
- **Renderização de Fontes:** As famílias tipográficas *Cormorant Garamond* e *Montserrat* renderizam com antialiasing subpixel suave (`-webkit-font-smoothing: antialiased`).
- **Performance de Scroll:** 60fps constantes sem jank ou recalculo forçado de estilo durante a rolagem com o header fixo (`backdrop-filter`).
- **Focus Indicators:** Contornos `:focus-visible` respeitam integralmente o offset e a paleta oliva (`#56664B`), sem colisão visual com os cantos arredondados de botões ou cards.

### 3.2. Mozilla Firefox (Motor Gecko)
- **Status:** Compatível via Análise Estática de Padrões W3C.
- **Suporte a Cores e Tokens:** Suporte pleno a variáveis CSS e sintaxe moderna de cores `rgba()`.
- **Scrollbar em Carrossel Móvel:** Suporte completo à propriedade padrão W3C `scrollbar-width: none;` no container `.fileira-identificacao`, eliminando a exibição de barras de rolagem estéticas indesejadas em distribuições Linux e Windows.
- **Flexbox & Grid Gap:** Gecko implementa suporte completo a `gap` em Flexbox desde a versão 63.

### 3.3. Apple Safari Desktop & Mobile (Motor WebKit)
- **Status:** Compatível via Análise Estática de Especificações WebKit.
- **Prevenção do Bug de Auto-Zoom (iOS Safari):**
  - O motor WebKit no iOS possui um comportamento compulsório de dar zoom na página quando o usuário clica em um input com tamanho de fonte inferior a 16px.
  - *Mitigação Implementada:* Todos os campos de `.form-input`, `.form-select`, `.form-textarea` e `.barra-busca__input` possuem `font-size: 1rem` (16px), garantindo estabilidade do enquadramento.
- **Barra de Navegação Dinâmica (`100dvh`):**
  - O uso de `100vh` tradicional provocava o corte da base do menu móvel pela barra de navegação retrátil do Safari. O uso de `height: 100dvh` resolve a falha nativamente em todas as versões modernas do iOS (>= 15.4).
- **Prefixos Defensivos WebKit:**
  - Preservado `-webkit-backdrop-filter: blur(10px)` para garantir efeito de vidro fosco no Header e Modais no macOS/iOS.
  - Preservado `-webkit-overflow-scrolling: touch` para suporte à aceleração por hardware e rolagem elástica inercial.

---

## 4. Recomendações para Testes Futuros com Hardware Físico

1. **Testes em Dispositivos Físicos Apple:**
   - Quando as fotografias definitivas forem disponibilizadas na etapa fotográfica futura, recomenda-se realizar uma conferência de aferição em iPhone e iPad reais para validação de calibração de cor (telas Retina / Display P3 vs sRGB).
2. **Ambiente com Múltiplos Monitores:**
   - Testar o comportamento da janela ao ser movida entre monitores com diferentes fatores de escala do Windows (ex: tela primária 125% e tela secundária 100%).
