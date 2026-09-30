# INVENTÁRIO DE COMPONENTES VISUAIS — INSTITUTO MENTE EM FOCO
**CATÁLOGO SISTEMÁTICO DE COMPONENTES DE INTERFACE, VARIANTES, TOKENS E ESTILOS UNIFICADOS**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA CSS

---

## 1. INTRODUÇÃO E DIRETRIZES DE ENGENHARIA UI

Este documento estabelece o inventário completo e detalhado de todos os componentes de interface do usuário (UI) implementados no **Instituto Mente em Foco**. Cada componente foi projetado seguindo as premissas de:

1. **HTML Semântico:** Uso exclusivo de tags nativas adequadas (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<details>`, `<footer>`, `<button>`, `<a>`).
2. **Arquitetura CSS Desacoplada:** Zero dependência de frameworks utilitários compilados (Tailwind/Bootstrap). Utilização de CSS Vanilla modular com Design Tokens centralizados em `tokens.css`.
3. **Consistência de Estados:** Definição estrita e homogênea para `:hover`, `:active`, `:focus-visible` e `@media (prefers-reduced-motion: reduce)`.
4. **Reserva Dimensional e Acessibilidade:** Componentes de mídia com `aspect-ratio` nativo (CLS = 0) e touch targets em conformidade com WCAG 2.5.8 ($\ge 44\times 44\text{px}$).

---

## 2. COMPONENTES ESTRUTURAIS E DE NAVEGAÇÃO GLOBAL

### 2.1 Header Institucional (`.cabecalho-site`)
* **Seletor Principal:** `.cabecalho-site`
* **Localização / Inclusão:** `templates/componentes/header.html` (incluso no `base/base.html`).
* **Propriedades Físicas:**
  * Altura fixa de 84px (`--altura-header: 84px`).
  * `position: sticky; top: 0; z-index: 100;`
  * Fundo translúcido com acabamento cerâmico: `rgba(247, 243, 235, 0.94)` com `backdrop-filter: blur(12px)`.
  * Borda inferior de contenção: `1px solid var(--cor-borda-suave)`.
* **Subcomponentes:**
  * Logo institucional (`.logo-site` / `.marca-clinica`): tipografia serifada *Cormorant Garamond* com subtítulo refinado em *Montserrat*.
  * Menu Desktop horizontal (`.navegacao-principal`): visível em telas $\ge 1080\text{px}$.
  * Botão de Ação Primária ("Agendar atendimento"): pílula compacta de alto contraste.
  * Acionador Mobile Hambúrguer (`#menu-mobile-toggle`): botão acessível com `aria-expanded` e `aria-controls`.

### 2.2 Menu Mobile Off-Canvas (`.menu-mobile`)
* **Seletor Principal:** `.menu-mobile`, `.menu-mobile__painel`, `.menu-mobile__backdrop`
* **Localização / Inclusão:** `templates/componentes/header.html`
* **Comportamento & Transições:**
  * Drawer lateral deslizante posicionado à direita (`right: 0`).
  * Largura responsiva fluida: `min(380px, 86vw)`.
  * Superfície opaca sólida em `--cor-fundo-principal` com sombra profunda.
  * Backdrop escuro com desfoque de fundo (`rgba(0, 0, 0, 0.45)` com `backdrop-filter: blur(4px)`).
  * Animação por translação de hardware (`transform: translateX(100%)` para `translateX(0)` em 280ms ease-out).
  * Acessibilidade completa via teclado (Escape, tab-trap e restauração de foco).

### 2.3 Rodapé Institucional (`.rodape-site`)
* **Seletor Principal:** `.rodape-site`
* **Localização / Inclusão:** `templates/componentes/footer.html`
* **Superfície & Grid:**
  * Fundo institucional escuro em Verde Oliva Nobre: `var(--cor-oliva)`.
  * Tipografia em alto contraste: textos em `--cor-texto-claro` (`#F7F3EB`) e títulos com realce suave.
  * Grid responsivo de 4 colunas em desktop, adaptando-se para 2 colunas em tablet e 1 coluna em mobile:
    1. Marca, síntese clínica, selo ético e CRP da psicóloga responsável.
    2. Navegação institucional rápida.
    3. Especialidades e áreas clínicas.
    4. Atendimento direto, canais de contato e redes sociais verificadas.
  * Barra de direitos autorais inferior com divisor sutil em dourado e link para Política de Privacidade.

### 2.4 Botão Flutuante do WhatsApp (`.btn-whatsapp-flutuante`)
* **Seletor Principal:** `.btn-whatsapp-flutuante`
* **Localização / Inclusão:** `templates/componentes/whatsapp_flutuante.html`
* **Comportamento & Estilo:**
  * Posição fixa no canto inferior direito (`bottom: 24px; right: 24px; z-index: 90;`).
  * Suporte a áreas seguras em smartphones (`env(safe-area-inset-bottom, 24px)`).
  * Fundo em Verde Oliva Nobre / Sálvia escurecido (`#4D6B42`), rejeitando o tom néon agressivo de marketing invasivo.
  * Sombra suave de elevação (`0 4px 16px rgba(0, 0, 0, 0.18)`), transição de escala controlada no hover (`transform: translateY(-2px) scale(1.03)`).
  * Condição no CMS: renderizado estritamente se o número estiver cadastrado.

---

## 3. BOTÕES E COMPONENTES DE AÇÃO

Todos os botões do sistema herdam as premissas estruturais da classe base `.btn`:
* `display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;`
* `min-height: 48px; min-width: 48px;` (ergonomia tátil e WCAG 2.5.8 garantidos).
* `font-family: var(--fonte-texto); font-weight: 500; font-size: 0.9375rem; letter-spacing: 0.02em;`
* `border-radius: var(--radius-pill);` (formato em pílula elegante característico da referência visual).
* `text-decoration: none; cursor: pointer; transition: all 200ms ease;`

| Variante | Classe CSS | Cor de Fundo | Cor do Texto | Borda | Estado Hover | Uso Recomendado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primário** | `.btn--primario` | `var(--cor-oliva)` | `var(--cor-texto-claro)` | Nenhuma | `#44523B`, elevação suave `translateY(-2px)` | Chamadas principais para ação (Agendamento, Contato) |
| **Secundário** | `.btn--secundario` | Transparente | `var(--cor-texto-principal)` | `1.5px solid var(--cor-borda)` | Fundo `var(--cor-fundo-secundario)`, borda `var(--cor-oliva)` | Ações informativas complementares ("Conhecer serviços") |
| **WhatsApp** | `.btn--whatsapp` | `var(--cor-whatsapp)` | `#FFFFFF` | Nenhuma | `var(--cor-whatsapp-hover)`, `translateY(-2px)` | Conversas diretas via WhatsApp na página de contato |
| **Dourado** | `.btn--dourado` | `var(--cor-dourado)` | `var(--cor-oliva)` | Nenhuma | `#B59356`, sombra tênue | Fechamento nobre sobre fundos escuros (CTA Final) |
| **Retorno** | `.botao-retorno` | Transparente | `var(--cor-texto-principal)` | Nenhuma | Seta transladada -4px para esquerda | Voltar para artigos ou listagens anteriores |
| **Link com Seta** | `.link-seta` | Transparente | `var(--cor-oliva)` | Nenhuma | Seta transladada +4px para direita | Links inline de navegação editorial e cartões |

---

## 4. CARDS E SUPERFÍCIES DE CONTEÚDO

### 4.1 Card Fotográfico com Overlay (`.card-foto`)
* **Uso:** Áreas de atuação na Home (5 cards) e destaques de serviços.
* **Aspect-Ratio:** `4:3` fixo.
* **Superfície & Efeitos:**
  * Imagem fotográfica de fundo com `object-fit: cover`.
  * Gradiente de sobreposição escuro: `linear-gradient(180deg, rgba(45, 41, 38, 0.05) 0%, rgba(45, 41, 38, 0.75) 100%)`.
  * Título em *Cormorant Garamond* em cor branca (`#FFFFFF`), peso 500, com badge temática superior.
  * Transição suave no `:hover`: leve zoom de imagem (`scale(1.04)`) contido por `overflow: hidden`.

### 4.2 Card de Identificação Acolhedora (`.card-identificacao`)
* **Uso:** Seção dos 7 momentos de vida na Home (Seção 03).
* **Superfície & Dimensões:**
  * Fundo branco puro (`var(--cor-superficie)`).
  * Formato esguio vertical: altura mínima de 220px, preenchimento interno equilibrado (`var(--espaco-6)`).
  * Borda sutil: `1px solid var(--cor-borda-suave)` com raio de curvatura moderado (`var(--radius-md)`).
  * Ícone linear estilizado no topo seguido de texto reflexivo em itálico de leitura acolhedora.

### 4.3 Card de Artigo Editorial (`.card-artigo`)
* **Uso:** Grade de publicações no Blog e prévias na Home.
* **Estrutura:**
  * Frame fotográfico superior com proporção `16:9` (`.ratio-16-9`).
  * Corpo textual contendo: Badge de categoria clínica, data editorial, título H3 expressivo e excerto conciso.
  * Link de avanço discreto com seta animada.

### 4.4 Card de Destaque WhatsApp (`.card-whatsapp-destaque`)
* **Uso:** Página de Contato (`/contato/`).
* **Estilo Unificado:**
  * Fundo nobre em Verde Oliva (`var(--cor-oliva)`) com tipografia off-white clara.
  * Borda perimetral suave em dourado champanhe (`var(--cor-dourado)`).
  * Ícone do WhatsApp de alta fidelidade e botão dedicado de início rápido de conversa.

---

## 5. COMPONENTES DE MÍDIA E PLACEHOLDERS

### 5.1 Sistema de Proporções Nativas (`.media-frame`)
A aplicação utiliza classes utilitárias rígidas baseadas na propriedade CSS nativa `aspect-ratio`, impedindo integralmente qualquer deslocamento de layout (*Cumulative Layout Shift* - CLS):
* `.ratio-4-5`: Reservado para retratos verticais da profissional (Hero da Home `IMG-001`, Sobre Mim `IMG-010`). Proporção $4:5$ (`aspect-ratio: 4 / 5`).
* `.ratio-4-3`: Reservado para capas de serviços e cartões de especialidades clínicas. Proporção $4:3$ (`aspect-ratio: 4 / 3`).
* `.ratio-1-1`: Reservado para composições botânicas e detalhes decorativos. Proporção $1:1$ (`aspect-ratio: 1 / 1`).
* `.ratio-16-9`: Reservado para capas de artigos do blog e banners amplos. Proporção $16:9$ (`aspect-ratio: 16 / 9`).

### 5.2 Componente Nobre de Placeholder (`.placeholder-imagem`)
* Enquanto as fotografias definitivas não são inseridas, a aplicação renderiza um placeholder visual elegante em vez de caixas cinzas genéricas ou imagens de stock artificiais.
* **Composição:** Fundo em degradê cerâmico sutil (`linear-gradient(135deg, var(--cor-fundo-secundario) 0%, var(--cor-areia) 100%)`), padrão geométrico sutil em filigrana, ícone de retrato ou tema da área e identificador da imagem (ex: `IMG-001 • Proporção 4:5`).

---

## 6. COMPONENTES DE FORMULÁRIO E BUSCA

### 6.1 Campos de Entrada de Dados (`.form-input`, `.form-select`, `.form-textarea`)
* **Tipografia:** `font-size: 1rem;` (16px estrito para neutralizar o auto-zoom compulsório do Safari iOS).
* **Superfície:** Fundo off-white macio com borda perimetral suave `1.5px solid var(--cor-borda)`.
* **Estado de Foco (`:focus`):** Realce nítido e elegante com borda em `var(--cor-oliva)` e anel de foco exterior `box-shadow: 0 0 0 3px rgba(86, 102, 75, 0.20);` com outline nulo.
* **Estado de Erro (`.tem-erro`):** Borda avermelhada controlada (`var(--cor-erro)`) com mensagem explicativa logo abaixo associada via `aria-describedby`.

### 6.2 Barra de Busca do Blog (`.barra-busca`)
* Campo integrado com ícone vetorial de lupa, preenchimento ergonômico, botão de submissão limpo e sanitização defensiva contra entradas excessivas.

---

## 7. COMPONENTES EDITORIAIS E ACCORDIONS

### 7.1 Acordeom Acessível de Perguntas Frequentes (`.faq-item`)
* Implementado com HTML nativo semântico: tags `<details>` e `<summary>`.
* Zero necessidade de bibliotecas JavaScript pesadas de animação.
* Ícone chevron suave girando 180° via CSS puro quando `open`.
* Foco visível acessível por tabulação direta do teclado.

### 7.2 Passos do Atendimento (`.step`)
* Numeração nobre em Dourado Champanhe (`01`, `02`, `03`, `04`) em fonte display *Cormorant Garamond*.
* Linha conectora vertical ou horizontal suave unindo o fluxo clínico do acolhimento.

---

## 8. SÍNTESE DO INVENTÁRIO

Com a unificação dos estilos, resolução dos tokens legados e testes em todas as 16 rotas, o **Instituto Mente em Foco** dispõe de um catálogo coeso, escalável, livre de redundâncias e com total integridade visual e funcional.
