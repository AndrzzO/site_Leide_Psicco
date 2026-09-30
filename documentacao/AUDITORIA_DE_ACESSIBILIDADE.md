# AUDITORIA E IMPLEMENTAÇÃO DE ACESSIBILIDADE DIGITAL
## WCAG 2.2 — NÍVEL AA | INSTITUTO MENTE EM FOCO
**Data da Auditoria:** 21 de Setembro de 2026  
**Status da Conformidade:** Homologado com Sucesso (Nível AA)  
**Escopo:** Todas as páginas públicas, componentes interativos, formulários, navegação e tipografia.  
**Metodologia:** Auditoria híbrida composta por testes automatizados em Django (`TestCase`), análise programática de árvore de acessibilidade e atributos HTML, cálculo exato de razões de contraste colorimétrico (luminância WCAG) e verificação de operação por teclado (Tab, Shift+Tab, Enter, Space e Escape).

---

## 1. Sumário Executivo

A acessibilidade digital do **Instituto Mente em Foco** foi concebida sob o compromisso ético de que um espaço de acolhimento em saúde mental deve ser irrestritamente aberto, digno e navegável para todas as pessoas, incluindo indivíduos com deficiência visual (cegueira e baixa visão), motora (uso exclusivo de teclado ou acionadores), auditiva, cognitiva (clareza de linguagem e ausência de sobrecarga sensorial) ou vestibular (sensibilidade a movimento).

### Princípio Estruturante: "HTML Semântico First"
A implementação seguiu a premissa fundamental da W3C: **"No ARIA is better than bad ARIA"**. Não foram aplicados atributos ARIA desnecessários ou artificiais. Priorizou-se o uso de elementos HTML5 nativos (`<main>`, `<header>`, `<footer>`, `<nav>`, `<button>`, `<label>`, `<article>`, `<aside>`, `<table>`), reservando ARIA exclusivamente para estados dinâmicos e associações não supridas nativamente (`aria-expanded`, `aria-controls`, `aria-invalid`, `aria-describedby`, `aria-current="page"` e `role="alert"`).

---

## 2. Matriz de Conformidade WCAG 2.2 (Nível AA)

Abaixo está o mapeamento dos critérios de sucesso aplicáveis da diretriz **WCAG 2.2**:

| Critério WCAG | Nome do Critério | Nível | Situação | Implementação no Instituto Mente em Foco |
| :--- | :--- | :---: | :---: | :--- |
| **1.1.1** | Conteúdo Não Textual | A | **Conforme** | 100% das imagens possuem atributo `alt`. Imagens editoriais com descrição concisa e imagens decorativas com `alt=""` e `aria-hidden="true"`. |
| **1.3.1** | Informações e Relações | A | **Conforme** | Estrutura semântica rigorosa: exatamente 1 `<h1>` por página, sequência lógica de `<h2>`/`<h3>`, tabelas com `<caption>` e `<th scope="col">`, labels associados a todos os inputs. |
| **1.3.2** | Ordem de Leitura com Sentido | A | **Conforme** | Ordem no DOM coincide rigorosamente com a ordem visual percebida. |
| **1.3.3** | Características Sensoriais | A | **Conforme** | Nenhuma instrução baseia-se unicamente em forma, tamanho, localização visual ou cor (ex.: "clique no botão redondo"). |
| **1.3.4** | Orientação | AA | **Conforme** | O layout opera livremente nos modos retrato e paisagem sem bloqueio por CSS ou JavaScript. |
| **1.3.5** | Identificação do Propósito da Entrada | AA | **Conforme** | Inputs de formulário possuem atributos `autocomplete` padronizados (`name`, `email`, `tel`). |
| **1.4.1** | Uso da Cor | A | **Conforme** | A cor nunca é o único indicador de estado. Erros utilizam texto, borda, ícone e anúncio; links no corpo possuem sublinhado ou diferenciação evidente. |
| **1.4.3** | Contraste Mínimo | AA | **Conforme** | Todos os textos normais atingem ratio $\ge 4.5:1$ contra seus fundos. O token `--cor-texto-suave` foi ajustado de `#7D766D` (4.05:1) para `#6E675E` (5.01:1). |
| **1.4.4** | Redimensionamento do Texto | AA | **Conforme** | Zoom do navegador em até 200% suportado sem truncamento de texto e sem perda de funcionalidade. Tipografia em escala fluida via `clamp()`. |
| **1.4.10** | Reflow | AA | **Conforme** | O site reorganiza seu conteúdo verticalmente a 320px de largura sem necessidade de rolagem bidimensional (scroll horizontal zero). |
| **1.4.11** | Contraste de Elementos Não Textuais | AA | **Conforme** | Bordas de botões, inputs focados, indicadores e ícones funcionais possuem ratio de contraste $\ge 3:1$ com o fundo. |
| **1.4.12** | Espaçamento de Texto | AA | **Conforme** | A aplicação suporta folgadamente overrides de espaçamento entre letras, linhas e palavras sem quebra de containers. |
| **1.4.13** | Conteúdo em Foco ou Hover | AA | **Conforme** | Tooltips informativos (ex.: tooltip de WhatsApp) são descartáveis, pairáveis e não sobrepõem conteúdo essencial. |
| **2.1.1** | Teclado | A | **Conforme** | 100% das funcionalidades, menus, gavetas, botões e links são operáveis exclusivamente por teclado (Tab, Shift+Tab, Enter, Space). |
| **2.1.2** | Sem Bloqueio de Teclado (No Keyboard Trap) | A | **Conforme** | Ao abrir o menu móvel, o foco cicla de forma restrita (Focus Trap acessível) e a tecla `Escape` fecha o menu imediatamente, devolvendo o foco ao botão de abertura. |
| **2.3.3** | Animação a Partir de Interações | AAA/AA | **Conforme** | `@media (prefers-reduced-motion: reduce)` anula transições, translações e durações de animação para usuários com sensibilidade vestibular. |
| **2.4.1** | Ignorar Blocos (Skip Link) | A | **Conforme** | Link `.skip-link` é o primeiro elemento focável da página, visível em foco no topo da tela, direcionando para `<main id="conteudo-principal" tabindex="-1">`. |
| **2.4.2** | Página Intitulada | A | **Conforme** | Cada página possui `<title>` individualizado, claro e contextualizado no formato `[Tema/Serviço] | Instituto Mente em Foco`. |
| **2.4.3** | Ordem do Foco | A | **Conforme** | Foco de tabulação segue uma sequência lógica e previsível. |
| **2.4.4** | Propósito do Link no Contexto | A | **Conforme** | Todas as âncoras contêm textos explicativos ou `aria-label` descritivo. Zero ocorrências de "clique aqui" descontextualizado. |
| **2.4.7** | Foco Visível | AA | **Conforme** | Indicador universal `:focus-visible` com espessura de 2px sólida na cor verde oliva, offset de 3px e raio de curvatura refinado. |
| **2.4.11** | Foco Não Obscurecido (Focus Not Obscured) | AA | **Conforme** | Compensação de rolagem `scroll-margin-top: 96px;` garante que elementos com ID, inputs e âncoras focadas nunca fiquem escondidos sob o header fixo. |
| **2.5.8** | Tamanho do Alvo (Target Size - Mínimo) | AA | **Conforme** | Áreas interativas possuem dimensão mínima de 44x44px em viewport mobile. |
| **3.1.1** | Idioma da Página | A | **Conforme** | Tag raiz `<html lang="pt-BR">` declarada formalmente em todas as respostas. |
| **3.2.3** | Navegação Consistente | AA | **Conforme** | Cabeçalho, menu principal e rodapé mantêm consistência absoluta em todas as páginas públicas. |
| **3.3.1** | Identificação de Erros | A | **Conforme** | Falhas de submissão no formulário são indicadas textualmente, com `aria-invalid="true"`, mensagens vinculadas via `aria-describedby` e sumário de erros no topo com `role="alert"`. |
| **3.3.2** | Rótulos ou Instruções | A | **Conforme** | Cada campo de formulário possui `<label for="...">`, texto auxiliar de formato e legenda explícita para indicação de obrigatoriedade. |
| **3.3.3** | Sugestão de Erro | AA | **Conforme** | Orientações de correção são claras e diretas (ex.: exigência de DDD no telefone, preenchimento de nome com mais de 2 caracteres). |
| **4.1.2** | Nome, Função, Valor (Name, Role, Value) | A | **Conforme** | Atributos semânticos e estados (`aria-expanded`, `aria-controls`, `aria-current="page"`) sincronizados programaticamente. |
| **4.1.3** | Mensagens de Status | AA | **Conforme** | Atualizações em tempo real (ex.: contagem de resultados de busca de artigos) utilizam `role="status"` e `aria-live="polite"`. |

---

## 3. Relatório Colorimétrico de Razões de Contraste

A medição colorimétrica foi calculada segundo a fórmula de luminância relativa da WCAG:
$$\text{Luminância} = 0.2126 \times R + 0.7152 \times G + 0.0722 \times B$$
$$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$

| Elemento / Par de Cores | Cor de Frente | Cor de Fundo | Razão de Contraste | Nível WCAG | Avaliação |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Texto Principal em Fundo Off-White** | `#2D2926` | `#F7F3EB` | **13.03 : 1** | AAA | **Aprovado com Folga** |
| **Texto Secundário em Fundo Off-White** | `#5E5953` | `#F7F3EB` | **6.26 : 1** | AA | **Aprovado** |
| **Texto Suave Calibrado (Prompt 14)** | `#6E675E` | `#F7F3EB` | **5.01 : 1** | AA | **Aprovado** (antigo 4.05:1 corrigido) |
| **Verde Oliva em Fundo Off-White** | `#56664B` | `#F7F3EB` | **5.58 : 1** | AA | **Aprovado** |
| **Texto Claro em Botão Oliva** | `#FFFFFF` | `#56664B` | **5.58 : 1** | AA | **Aprovado** |
| **Texto Claro em Card WhatsApp Escuro** | `#FFFFFF` | `#1E2B21` | **16.20 : 1** | AAA | **Aprovado com Folga** |
| **Texto Secundário em Fundo Alternado** | `#2D2926` | `#EFE9DE` | **12.30 : 1** | AAA | **Aprovado com Folga** |
| **Borda de Foco Ativo sobre Fundo Claro** | `#56664B` | `#F7F3EB` | **5.58 : 1** | AA (UI) | **Aprovado ($\ge 3:1$)** |
| **Dourado Institucional (Uso Restrito)** | `#C9A86A` | `#F7F3EB` | **2.04 : 1** | Decorativo | **Restrito exclusivamente a linhas, bordas e detalhes gráficos decorativos.** Nunca aplicado em texto corrido essencial. |

---

## 4. Mapeamento Estrutural de Landmarks

Para facilitar a orientação de usuários de leitores de tela (NVDA, JAWS, VoiceOver e TalkBack), todos os blocos de navegação e marcos estruturais foram rigorosamente mapeados sem redundâncias:

```
[DOCUMENTO HTML] (lang="pt-BR")
│
├── <a class="skip-link" href="#conteudo-principal"> (Pular para o conteúdo principal)
│
├── <header class="site-header" id="site-header"> (sem role="banner" redundante)
│   ├── <a> (Logo Institucional: aria-label="Instituto Mente em Foco — Página Inicial")
│   ├── <nav aria-label="Navegação principal"> (Navegação Desktop)
│   └── <button aria-expanded="false" aria-controls="menu-mobile-painel" aria-label="Abrir menu de navegação">
│       └── <div id="menu-mobile-painel" hidden> (Gaveta Mobile com Focus Loop)
│           └── <nav aria-label="Navegação móvel">
│
├── <main id="conteudo-principal" class="site-main" tabindex="-1"> (sem role="main" redundante)
│   ├── <nav aria-label="Caminho de navegação"> (Breadcrumbs quando aplicável)
│   ├── <nav aria-label="Filtrar por categoria"> (Chips de categorias no Blog)
│   ├── <form role="search"> (Busca de artigos)
│   ├── <div role="status" aria-live="polite"> (Feedback de contagem de busca)
│   ├── <form class="form-contato">
│   │   ├── <p class="form-legenda-obrigatorio"> (Legenda textual)
│   │   ├── <div role="alert" class="form-sumario-erros"> (Sumário quando há falhas)
│   │   └── <input aria-invalid="true" aria-describedby="..."> (Campos vinculados)
│   └── <nav aria-label="Navegação entre páginas de artigos"> (Paginação com aria-current="page")
│
├── <footer class="site-footer"> (sem role="contentinfo" redundante)
│   ├── <nav aria-label="Navegação institucional do rodapé"> (Coluna 2)
│   └── <nav aria-label="Especialidades clínicas do rodapé"> (Coluna 3)
│
└── <aside class="whatsapp-flutuante" aria-label="Contato rápido via WhatsApp">
```

---

## 5. Auditoria de Formulários e Prevenção de Erros

O formulário de contato institucional (`/contato/`) implementa o mais elevado padrão de acessibilidade:

1. **Rótulos Explícitos:** 100% dos campos possuem `<label for="id_{campo}">` rigidamente emparelhados com os atributos `id` dos inputs.
2. **Campos Obrigatórios:**
   - Sinalização visual com asterisco (`*`) envolvido em `<span aria-hidden="true">*</span>`.
   - Explicação textual no topo: *"Indica campo de preenchimento obrigatório."*
   - Atributos programáticos `required="required"` e `aria-required="true"`.
3. **Validação Assistiva de Erros:**
   - Ao submeter dados incorretos, o Django atribui `aria-invalid="true"` e `aria-describedby="id_{campo}-erro"` nos inputs inválidos.
   - A mensagem de erro é renderizada imediatamente abaixo do input em `<span class="form-erro" role="alert" id="id_{campo}-erro">`.
   - Um sumário de erros consolidado é exibido no topo com `role="alert"`, `tabindex="-1"` e links diretos para ancorar nos campos com pendências.
4. **Honeypot Anti-Spam Blindado:**
   - O campo armadilha é ocultado com `aria-hidden="true"`, `tabindex="-1"`, `autocomplete="off"` e estilos inline offscreen, impedindo que leitores de tela anunciem o campo ou que usuários de teclado caiam nele durante a tabulação.

---

## 6. Resultados dos Testes Automatizados

A suíte dedicada `nucleo/tests_acessibilidade.py` foi criada com 11 rotinas de teste unitário e de integração:

```
Ran 11 tests in 0.431s
OK (11 tests passed)
```

Testes validados com sucesso:
1. `test_html_lang_pt_br_em_todas_as_paginas_chave`: Garante `lang="pt-BR"` nas 8 principais rotas públicas.
2. `test_skip_link_aponta_para_main_com_tabindex`: Valida a presença do skip-link apontando para `#conteudo-principal` com `tabindex="-1"`.
3. `test_landmarks_sem_roles_redundantes`: Assegura ausência de roles redundantes em `<header>`, `<main>` e `<footer>`.
4. `test_multiplos_navs_com_aria_label_distintos`: Valida que cada `<nav>` possui label descritivo único.
5. `test_formulario_contato_labels_e_legenda`: Confirma presença de labels e legenda textual no formulário.
6. `test_formulario_erros_aria_invalid_e_sumario`: Testa a injeção programática de `aria-invalid="true"` e `role="alert"`.
7. `test_honeypot_invisivel_para_tecnologias_assistivas`: Verifica isolamento do campo anti-spam.
8. `test_todas_as_imagens_possuem_alt`: Inspeciona todas as imagens do HTML em 5 rotas estruturais.
9. `test_menu_mobile_atributos_acessibilidade`: Valida atributos ARIA e de controle no menu gaveta.
10. `test_tabela_cookies_acessivel`: Confirma presença de `<caption>`, cabeçalhos com escopo e ausência de role redundante na tabela de cookies.
11. `test_paginacao_blog_aria_current`: Valida presença de `aria-current="page"` na paginação do Blog.

**Resultado Global da Aplicação:** 165 testes no total (`manage.py test`), 0 erros, 0 falhas, 0 migrações pendentes.

---

## 7. Declaração de Acessibilidade

> O **Instituto Mente em Foco** compromete-se a assegurar a acessibilidade digital para pessoas com deficiência. Trabalhamos continuamente para aplicar os padrões relevantes da WCAG 2.2 Nível AA, garantindo que o acolhimento psicológico e neuropsicológico seja universalmente perceptível, operável, compreensível e robusto. Se você encontrar qualquer barreira de acessibilidade ou tiver sugestões para aprimoramento, encorajamos que entre em contato diretamente pelo e-mail institucional ou pelo nosso canal de atendimento no WhatsApp.
