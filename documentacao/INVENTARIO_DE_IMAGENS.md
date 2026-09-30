# INVENTÁRIO DE IMAGENS E ASSETS — INSTITUTO MENTE EM FOCO
**MAPEAMENTO COMPLETO DE SLOTS, PROPORÇÕES, DIRETRIZES DE PERFORMANCE E STATUS DE FORNECIMENTO**
**VERSÃO:** 2.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

> [!CAUTION]
> **DOCUMENTO SUPERSEDIDO — PROMPT 23 (29/09/2026)**
>
> Este inventário foi substituído pelo documento mais completo e atual:
>
> **→ Use: [`MAPA_DE_PRODUCAO_DE_IMAGENS.md`](MAPA_DE_PRODUCAO_DE_IMAGENS.md)**
>
> O novo documento inclui todos os 13 slots de imagem (IMG-001 a IMG-013), blocos de blog, direção fotográfica, restrições éticas por imagem e distinção clara entre Grupo A (fotos reais da Mari — PENDENTES) e Grupo B (imagens temáticas IA — BRIEFS PRONTOS).
>
> Este arquivo é mantido apenas como referência histórica do Prompt 00.

> [!IMPORTANT]
> **REGRA ABSOLUTA — FOTOGRAFIAS DEFINITIVAS AINDA NÃO FORNECIDAS:**  
> As fotografias definitivas da cliente ainda não foram inseridas no projeto. Portanto:
> - **NÃO** realizar otimização fotográfica prematura em arquivos provisórios.
> - **NÃO** tratar placeholders como imagens definitivas.
> - **NÃO** gerar versões WebP/AVIF de placeholders.
> - **NÃO** alterar o enquadramento ou proporção das áreas fotográficas.
> - **NÃO** substituir placeholders por imagens stock ou geradas por IA.
> - **MANTENHA OS PLACEHOLDERS EXISTENTES**, ocupando exatamente as dimensões e proporções previstas.

---


## 1. Diretrizes Técnicas de Infraestrutura de Imagens

Todas as áreas fotográficas do Instituto Mente em Foco seguem padrões estritos para garantir estabilidade visual (**CLS = 0**) e rapidez de exibição (**LCP otimizado**):

1. **Aspect-Ratio Nativo no CSS:**  
   Todo container de mídia utiliza classes dedicadas (`.ratio-4-5`, `.ratio-16-9`, `.ratio-4-3`, `.media-frame`) com a propriedade `aspect-ratio: X / Y;` e `width: 100%; height: 100%;` declarados. Isso reserva o espaço dimensional exato antes mesmo do download do arquivo, impedindo qualquer salto de layout (*layout shift*).
2. **Object-Fit e Object-Position:**  
   Todas as imagens e placeholders utilizam `object-fit: cover` para garantir preenchimento harmônico sem distorção anamórfica, e `object-position` calibrado (ex: `center top` para retratos, preservando cabeças e expressões faciais; `center center` para capas e ambientações).
3. **Estratégia de Prioridade (LCP vs Lazy Loading):**  
   - **Imagens Acima da Dobra (LCP Candidates):** Devem possuir `loading="eager"`, `fetchpriority="high"` e `decoding="async"`, sem atraso por animações de revelação ou scripts bloqueantes.
   - **Imagens Abaixo da Dobra:** Devem possuir `loading="lazy"` e `decoding="async"` nativos do navegador.
4. **Orientações para Quando as Fotos Finais Forem Fornecidas:**  
   - Formatos recomendados: **WebP** e **AVIF** para navegadores modernos, mantendo **JPEG** progressivo ou **PNG** otimizado como fallback.
   - Compressão recomendada: Fator de qualidade entre 80 e 85 (perceptualmente sem perdas, sem artefatos em peles ou texturas).
   - Metadados: Limpeza de EXIF/geolocalização e preservação de perfil de cores sRGB.
   - Resoluções responsivas recomendadas: Gerar versões em `1x` e `2x` (Retina/HiDPI) para uso em `srcset` e `sizes`.

---

## 2. Inventário Mapeado por Slot de Imagem (Prompt 15 — Seção 252)

| ID | Página | Seção | Função | Aspect Ratio | Dimensões de Exibição Aprox. | Dimensões de Arquivo Recomendadas | Formato Futuro Recomendado | É LCP? | Lazy Load? | Object-Fit | Object-Position | Status Atual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **IMG-001** | Home (`/`) | Hero Principal | Retrato Oficial Mari Menezes | `4:5` | 480 × 600 px (Desk) / 340 × 425 px (Mob) | 960 × 1200 px (2x Retina) | WebP / AVIF (fallback JPG) | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center top` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-002** | Home (`/`) | Alguns momentos | Imagem Conceitual / Natureza | `1:1` | 400 × 400 px | 800 × 800 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-003** | Home (`/`) | Cards Atuação | Card: Psicologia Clínica | `4:3` | 360 × 270 px | 720 × 540 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-004** | Home (`/`) | Cards Atuação | Card: Neuropsicologia | `4:3` | 360 × 270 px | 720 × 540 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-005** | Home (`/`) | Cards Atuação | Card: Traumas | `4:3` | 360 × 270 px | 720 × 540 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-006** | Home (`/`) | Cards Atuação | Card: Separação & Recomeços | `4:3` | 360 × 270 px | 720 × 540 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-007** | Home (`/`) | Cards Atuação | Card: Novos Relacionamentos | `4:3` | 360 × 270 px | 720 × 540 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-008** | Global | Header / Footer | Logotipo do Instituto | Vetorial (~4:1) | 220 × 48 px (Desk) / 180 × 40 px (Mob) | Vetorial SVG nativo | SVG | **NÃO** | **NÃO** (No topo do documento) | `contain` | `left center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-009** | Global | Favicon / App | Ícone do Navegador | `1:1` | 32 × 32 px / 192 × 192 px / 512 × 512 px | Multi-resolução (SVG + PNG) | SVG / PNG | **NÃO** | **NÃO** (Head do documento) | `contain` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-010** | Sobre Mim (`/sobre-mim/`) | Hero Principal | Retrato Editorial Mari Menezes | `4:5` | 460 × 575 px | 920 × 1150 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center top` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-011** | Psicologia (`/servicos/psicologia/`) | Hero Interno | Capa Psicologia Clínica | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-012** | Neuropsicologia (`/servicos/neuropsicologia/`) | Hero Interno | Capa Neuropsicologia | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-013** | Traumas (`/servicos/traumas/`) | Hero Interno | Capa Traumas | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-014** | Separação (`/servicos/separacao-e-recomecos/`) | Hero Interno | Capa Separação & Recomeços | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-015** | Avaliação (`/servicos/avaliacao/`) | Hero Interno | Capa Avaliação Psicológica | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-016** | Reabilitação (`/servicos/reabilitacao-neurocognitiva/`) | Hero Interno | Capa Reabilitação Cognitiva | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-017** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 01 (Primeira Sessão) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-018** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 02 (Psicoterapia/Neuro) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-019** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 03 (Avaliação Adultos) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-020** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 04 (Memória/Sobrecarga) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-021** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 05 (Separação/Reconstrução)| `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-022** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 06 (Padrões Relacionais) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-023** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 07 (Traumas Não Elaborados)| `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-024** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 08 (Reabilitação Prática) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-025** | Conteúdos (`/conteudos/`) | Card Destaque / Detalhe | Capa Artigo 09 (Cuidar de Si) | `16:9` | 800 × 450 px | 1200 × 675 px | WebP / AVIF | **SIM (no Detalhe)** | **NÃO no Detalhe / SIM na Listagem** | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-026** | Global | Meta Tags / Social | Open Graph Social Card | `1.91:1` | 1200 × 630 px | 1200 × 630 px (< 200 KB) | JPG / PNG | **NÃO** (Invisível no DOM) | N/A | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-027** | Novos Relacionamentos (`/servicos/novos-relacionamentos/`) | Hero Interno | Capa Novos Relacionamentos | `16:9` | 1120 × 630 px | 1600 × 900 px | WebP / AVIF | **SIM** | **NÃO** (`eager` + `fetchpriority="high"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |
| **IMG-028** | Sobre Mim (`/sobre-mim/`) | Bloco Espaço | Foto Editorial Consultório | `4:3` | 560 × 420 px | 1120 × 840 px | WebP / AVIF | **NÃO** | **SIM** (`loading="lazy"`) | `cover` | `center center` | **AGUARDANDO FOTO DEFINITIVA** |

---

## 3. Especificação Técnica dos Placeholders Atuais

Enquanto as fotografias definitivas não forem enviadas, os elementos mantêm o layout protegido contra qualquer salto (CLS = 0) através dos componentes semânticos:

```css
/* Container de mídia com aspect-ratio rígido */
.media-frame.ratio-4-5 {
  aspect-ratio: 4 / 5;
  width: 100%;
}

.media-frame.ratio-16-9 {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.media-frame.ratio-4-3 {
  aspect-ratio: 4 / 3;
  width: 100%;
}

/* Componente placeholder que ocupa 100% do container reservado */
.placeholder-imagem {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: var(--cor-fundo-suave, #FAF6F0);
  border: 1px dashed var(--cor-taupe, #6D655B);
  color: var(--cor-taupe, #6D655B);
  text-align: center;
  padding: 1rem;
  box-sizing: border-box;
}
```
