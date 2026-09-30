# GUIA DE CONSISTÊNCIA VISUAL — INSTITUTO MENTE EM FOCO
**MANUAL DE DIREÇÃO CRIATIVA, REGRAS DE COMPOSIÇÃO, TIPOGRAFIA E ÉTICA VISUAL**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA CSS

---

## 1. PRINCÍPIOS DE DIREÇÃO CRIATIVA E ATMOSFERA VISUAL

O design do **Instituto Mente em Foco** é a expressão visual de um consultório de psicologia clínica contemporâneo, acolhedor e profundamente humano. Ele reflete a filosofia de cuidado personificada no tripé:

$$\textbf{COMPREENDER} \quad \bullet \quad \textbf{CUIDAR} \quad \bullet \quad \textbf{RECONSTRUIR}$$

### 1.1 O que o Design É
* **Sereno e Acolhedor:** Tons terrosos, cerâmicos e botânicos que reduzem o estresse visual e convidam à reflexão.
* **Editorial e Maduro:** Tipografia serifada nobre com respiros generosos inspirados em publicações editoriais de alta qualidade.
* **Claro e Confortável:** Contraste tipográfico deliberadamente superior às exigências mínimas da WCAG 2.1 AA (mínimo de 4.5:1, priorizando 7:1 em textos contínuos).
* **Rigoroso e Ético:** Respeito absoluto às resoluções do Conselho Federal de Psicologia (CFP). Ausência total de promessas de cura, contadores regressivos, pop-ups invasivos ou apelos sensacionalistas.

### 1.2 O que o Design NÃO É
* **Não é Corporativo/Frio:** Evita-se o branco estéril `#FFFFFF` em fundos predominantes e tons azuis hospitalares despersonalizados.
* **Não é "Marketing Agressivo":** Proibidos gatilhos de urgência ("Últimas vagas", "Agende agora ou perca"), cores neon, alertas piscantes ou sombras pesadas e vulgares.
* **Não é Minimalismo Vazio:** O espaço em branco é intencional e acolhedor, valorizando o texto e a pessoa, sem empobrecer a narrativa visual.

---

## 2. PALETA DE CORES E GOVERNANÇA CROMÁTICA

O sistema cromático compõe-se de exatamente 6 cores primárias primitivas, combinadas com superfícies semânticas:

```
[--cor-off-white: #F7F3EB]  Superfície Principal (Luz natural, aconchego)
[--cor-fundo-secundario: #EFE9DE]  Superfície Secundária (Areia suave, respiro de seção)
[--cor-areia: #D8C5A8]      Tom Natural (Apoio, badges, detalhes quentes)
[--cor-salvia: #A8B09A]     Verde Botânico (Ícones, leveza orgânica)
[--cor-oliva: #56664B]      Verde Institucional Nobre (Ações primárias, títulos, rodapé)
[--cor-dourado: #C9A86A]    Dourado Champanhe (Numeração, divisores sutis, acentos)
[--cor-texto-principal: #2D2926]  Café Escuro Orgânico (Legibilidade sem dureza)
```

### 2.1 Regras de Aplicação de Fundo e Contraste
1. **Alternância de Superfícies:** Páginas longas devem alternar o fundo entre `--cor-fundo-principal` (Off-White) e `--cor-fundo-secundario` (Areia suave) para demarcar suavemente a transição de temas sem recorrer a divisores artificiais.
2. **Superfícies Escuras com Moderação:** O fundo Verde Oliva escuro (`--cor-oliva`) é reservado exclusivamente para o Rodapé Institucional e a Seção de CTA Final, criando um fechamento nobre e imersivo.
3. **Proibição de Cores Fora da Paleta:** É expressamente vedado o uso de pretos puros (`#000000`), brancos hospitalares absolutos em fundos de página ou verdes saturados em elementos de ação.

---

## 3. SISTEMA TIPOGRÁFICO E RITMO EDITORIAL

A tipografia do projeto baseia-se na harmonia entre duas famílias tipográficas consagradas:

* **Títulos, Citações e Números Display:** `'Cormorant Garamond', Georgia, serif;`
  * Expressa sofisticação, humanidade, empatia e solidez intelectual.
  * Pesos recomendados: `500` (médio) para títulos principais; `400i` (itálico) para frases de acolhimento e citações.
* **Textos Correntes, Navegação, Formulários e Botões:** `'Montserrat', sans-serif;`
  * Garante leitura desimpedida, precisão geométrica e clareza em todas as resoluções.
  * Pesos: `400` (regular para parágrafos), `500` (médio para navegação/botões) e `600` (destaques e labels).

### 3.1 Escala Tipográfica Fluida
A escala utiliza `clamp()` calculada a partir da largura do viewport, eliminando saltos abruptos de breakpoint:
* **H1 / Título Hero:** `clamp(2.5rem, 1.95rem + 2.5vw, 4.25rem)` — `line-height: 1.15; text-wrap: balance; font-weight: 500;`
* **H2 / Título de Seção:** `clamp(2rem, 1.7rem + 1.2vw, 2.75rem)` — `line-height: 1.25; margin-bottom: var(--espaco-4);`
* **H3 / Título de Cartão:** `clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)` — `line-height: 1.35;`
* **Corpo de Texto (Body):** `clamp(0.9375rem, 0.9rem + 0.2vw, 1rem)` — `line-height: 1.7; max-width: 65ch; text-wrap: pretty;`
* **Eyebrow / Pré-Título:** `font-size: 0.8125rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; color: var(--cor-dourado);`

---

## 4. ESPAÇAMENTO E RITMO VERTICAL

O ritmo visual do site prioriza o conforto ocular do leitor através de respiros generosos e consistentes:

* **Distância entre Seções Principais (`padding-block`):**
  * Desktop ($\ge 1080\text{px}$): `clamp(5rem, 8vw, 7.5rem)` (~80px a 120px).
  * Mobile ($< 768\text{px}$): `clamp(3rem, 6vw, 4rem)` (~48px a 64px).
* **Largura Máxima de Leitura:**
  * Parágrafos editoriais não devem exceder `65ch` a `75ch` (`max-width: 65ch`), impedindo fadiga ocular no retorno de linha.
* **Gaps de Grids e Listas:**
  * Grids de cartões: `clamp(1.25rem, 2.5vw, 2rem)`.
  * Elementos inline / botões em cluster: `var(--espaco-4)` (16px).

---

## 5. CARDS, BORDAS, RAIOS E PROFUNDIDADE

### 5.1 Raios de Curvatura (Border-Radius)
* **Botões de Ação:** Formato em pílula absoluto (`--radius-pill: 9999px;`).
* **Cards e Módulos de Conteúdo:** Curvatura suave e moderna (`--radius-md: 12px;` ou `--radius-lg: 16px;`).
* **Campos de Formulário:** Curvatura ergonômica (`--radius-sm: 8px;`).

### 5.2 Elevações e Sombras
O Design System repudia sombras duras, pretas e artificiais. Toda profundidade é obtida por difusão suave:
* `--sombra-sm`: `0 2px 8px rgba(45, 41, 38, 0.04);` (repouso de cartões).
* `--sombra-md`: `0 8px 24px rgba(45, 41, 38, 0.08);` (hover e modais).
* `--sombra-lg`: `0 16px 40px rgba(45, 41, 38, 0.12);` (drawer móvel).

---

## 6. FOTOGRAFIA, ENQUADRAMENTO E PLACEHOLDERS

### 6.1 Regras de Proporção e Enquadramento
* **Retratos da Profissional (Hero e Sobre):** Proporção estrita $4:5$ (`aspect-ratio: 4 / 5`), enquadramento no busto/olhar com `object-position: center 20%`.
* **Capas de Serviços e Especialidades:** Proporção $4:3$ (`aspect-ratio: 4 / 3`), transmitindo equilíbrio e solidez clínica.
* **Imagens Botânicas e Detalhes:** Proporção $1:1$ (`aspect-ratio: 1 / 1`), foco em texturas naturais e iluminação difusa.
* **Capas do Blog:** Proporção $16:9$ (`aspect-ratio: 16 / 9`), facilitando a leitura da composição horizontal.

### 6.2 Critérios para Fotografias Definitivas
Quando as fotos profissionais reais forem fornecidas pelo cliente, devem obedecer às seguintes diretrizes:
* Paleta tonal natural (tons neutros, terrosos, linho, madeira clara, vegetação verde natural).
* Expressão serena, acolhedora e confiante, evitando poses artificiais de publicidade ou sorrisos exagerados.
* Iluminação natural indireta sem sombras duras no rosto.
* Fundo do consultório desfocado ou com elementos sutis de acolhimento (livros, plantas, poltrona confortável).

---

## 7. MICROINTERAÇÕES E ESTADOS DE FOCO

* **Duração de Transição:** Todas as animações e transições de interface devem situar-se entre `180ms` e `300ms` com aceleração suave `ease` ou `ease-out`.
* **Foco Acessível Obrigatório (`:focus-visible`):**
  * Contorno nítido de foco com anel exterior de 3px em `rgba(86, 102, 75, 0.25)` e borda na cor principal.
  * O indicador visual de foco nunca deve ser removido com `outline: none` sem um substituto equivalente.
* **Respeito a `prefers-reduced-motion`:**
  * Em dispositivos com redução de movimento ativada pelo usuário, transições e animações devem ser redefinidas para duração quase nula (`0.01ms`), eliminando movimentos de translação e zoom.

---

## 8. CONCLUSÃO E APLICAÇÃO PRÁTICA

Este guia assegura que qualquer nova página, artigo de blog ou seção adicionada futuramente ao site do **Instituto Mente em Foco** mantenha rigorosamente a mesma linguagem, elegância editorial, conforto visual e compromisso ético da entrega inicial.
