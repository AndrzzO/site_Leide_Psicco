# Guia de Engenharia Responsiva e Boas Práticas Cross-Device

**Projeto:** Instituto Mente em Foco  
**Destinatários:** Desenvolvedores e Mantenedores do Portal  
**Filosofia:** Mobile-First, CSS Puro, Design Tokens Semânticos, Acessibilidade e Resiliência Universal

---

## 1. Convenção Oficial de Breakpoints

O projeto adota uma estratégia escalonada e mobile-first orientada pelo conteúdo e pela hierarquia de componentes:

| Breakpoint | Valor CSS | Aplicação Principal no Projeto |
| :--- | :--- | :--- |
| **Micro-Mobile** | `<= 400px` | Quebra de linha fluida para botões (`white-space: normal`) e redução de padding. |
| **Mobile Narrow**| `480px` | Exibição condicional do botão CTA no cabeçalho; transição de pilhas verticais. |
| **Mobile Wide**  | `640px` | Rodapé comuta para 2 colunas; cards de conteúdo em grid duplo. |
| **Tablet Portrait** | `768px` | Grids editoriais em 2 colunas; citação flutuante da Home assume posicionamento absoluto. |
| **Desktop Threshold**| `1080px` | **Limiar Mestre:** Menu Desktop horizontal completo ativo; botão hambúrguer oculto; gaveta mobile desativada. |
| **Desktop Standard** | `1200px` | Fileira de 7 identificações comuta de carrossel de rolagem horizontal snap para grid linear contínuo. |
| **Container Max**| `1280px` / `1440px` | Limite de largura máxima dos containers `.container` e `.container-largo`. |

---

## 2. Tipografia Fluida com `clamp()`

Nunca utilize tamanhos de fonte estáticos em `px` para títulos ou cabeçalhos de seção. Utilize os tokens de escala definidos em `tokens.css`:

```css
/* Exemplo de uso correto de tokens de fonte */
.meu-titulo {
  font-family: var(--fonte-display);
  font-size: var(--fonte-hero); /* clamp(2.5rem, 1.95rem + 2.5vw, 4.25rem) */
  line-height: 1.15;
  text-wrap: balance; /* Evita palavras órfãs em telas estreitas */
}

.meu-paragrafo {
  font-family: var(--fonte-texto);
  font-size: var(--fonte-base); /* clamp(0.9375rem, 0.9rem + 0.2vw, 1rem) */
  line-height: 1.65;
  text-wrap: pretty;
}
```

---

## 3. Diretrizes para Touch Targets e Ergonomia Móvel

1. **Dimensão Mínima de Toque (WCAG 2.5.8):**
   - Qualquer elemento clicável ou acionável por toque (links, botões, ícones) deve possuir área mínima de **44x44px** (ou 48x48px no Android).
   - Caso o elemento visual seja menor (ex: ícone de 38px), utilize a técnica do pseudo-elemento invisível para expandir o alvo de toque:
   ```css
   .meu-icone-pequeno {
     position: relative;
     width: 38px;
     height: 38px;
   }
   .meu-icone-pequeno::after {
     content: "";
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     min-width: 44px;
     min-height: 44px;
     width: 100%;
     height: 100%;
   }
   ```
2. **Espaçamento entre Alvos de Toque:**
   - Mantenha no mínimo `8px` (`var(--espaco-2)`) de separação entre botões ou links adjacentes para evitar cliques acidentais em smartphones.

---

## 4. Regras Anti-Glitches para WebKit (iOS Safari)

1. **Prevenção de Auto-Zoom em Formulários:**
   - Nunca declare `font-size < 16px` (ou `< 1rem`) em tags `<input>`, `<select>` ou `<textarea>`. O iOS Safari realiza um zoom forçado de tela que desalinha a experiência do usuário.
2. **Uso de Altura de Viewport Dinâmica:**
   - Sempre utilize `height: 100dvh` para painéis em tela cheia (como modais ou gaveta de menu), evitando que a barra de endereços do navegador corte os botões de ação inferiores.
3. **Safe Area Insets com Fallback Seguro:**
   - Sempre forneça valor de fallback ao utilizar variáveis de ambiente:
   ```css
   padding-bottom: calc(1rem + env(safe-area-inset-bottom, 0px));
   ```

---

## 5. Regras para Imagens e Proporções de Aspect Ratio

> [!IMPORTANT]
> As fotografias definitivas ainda não foram adicionadas. Todos os slots fotográficos utilizam containers proporcionais estruturados com as seguintes classes e tokens:
> - Retrato da Profissional / Hero: `aspect-ratio: 4 / 5;`
> - Cards de Destaque / Serviços: `aspect-ratio: 4 / 3;`
> - Ícones / Avatares: `aspect-ratio: 1 / 1;`
> - Imagens de Artigos / Banners: `aspect-ratio: 16 / 9;`
> 
> Nunca force `height` estático em pixels sobre imagens `<img>` sem definir `object-fit: cover;`.

---

## 6. Checklist de Verificação Pré-Deploy Responsivo

Antes de publicar qualquer alteração no frontend:

- [ ] **Teste de 320px:** Abra as DevTools do navegador, redimensione para 320x568px e verifique no console se `document.documentElement.scrollWidth === document.documentElement.clientWidth`.
- [ ] **Teste de 1080px (Threshold):** Redimensione a largura entre 1079px e 1081px. O menu desktop deve sumir e o botão hambúrguer deve surgir sem qualquer piscamento (*flicker*) ou sobreposição visual.
- [ ] **Teste de Reflow 200%:** Aplique zoom de 200% na tela do desktop (1280px). Todo o conteúdo deve fluir verticalmente sem barras de rolagem horizontais.
- [ ] **Navegação por Teclado:** Pressione `Tab` a partir do topo; verifique se o skip-link aparece e se todos os botões recebem o anel de foco `:focus-visible`.
- [ ] **Teste do Menu Mobile:** Abra a gaveta, pressione `Tab` consecutivamente para atestar o **Focus Trap** (o foco não deve sair da gaveta) e pressione `Escape` para fechar.
- [ ] **Execução da Suíte de Testes:** Execute `python manage.py test` para assegurar que nenhuma rota quebrou.
