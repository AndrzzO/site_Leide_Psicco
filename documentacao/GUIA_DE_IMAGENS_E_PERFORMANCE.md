# GUIA PRÁTICO DE IMAGENS E PERFORMANCE
## DIRETRIZES DE ASSETS, PROPORÇÕES E CARREGAMENTO RÁPIDO
### INSTITUTO MENTE EM FOCO

> [!NOTE]
> Este guia orienta a cliente (Mari Menezes), a equipe administrativa e os editores de conteúdo sobre como preparar, enviar e gerenciar fotografias no site para garantir **máxima beleza visual aliada a carregamento ultrarrápido**.

---

## 1. Por Que o Tratamento de Imagens é Crucial?

Em sites modernos, as fotografias representam habitualmente entre **60% e 80% do peso total** transmitido pela rede. Imagens mal otimizadas ou gigantescas causam:
- Lentidão no carregamento em conexões móveis (3G/4G).
- Piora no índice **LCP (Largest Contentful Paint)** do Google.
- Abandono de visitantes antes mesmo de lerem a proposta terapêutica do Instituto.

Por outro lado, uma compressão excessiva ou agressiva pode deixar fotos borradas ou pixeladas, prejudicando a percepção de elegância e acolhimento da marca. O objetivo é o equilíbrio perfeito: **imagens nítidas e leves**.

---

## 2. Padrões de Proporção (Aspect Ratio) no Site

O site do Instituto Mente em Foco foi construído com containers inteligentes que mantêm proporções fixas para impedir solavancos na tela (**CLS = 0**).

| Proporção | Onde é Utilizada no Site | Dimensão Recomendada (1x / 2x Retina) | Exemplo de Uso |
|---|---|---|---|
| **4:5 (Vertical)** | Hero da Home, Bloco Sobre, Página Sobre Mim | **960 × 1200 px** | Retratos profissionais de meio-corpo |
| **16:9 (Horizontal Panorâmica)** | Capas de Páginas de Serviços e Capas de Artigos do Blog | **1600 × 900 px** | Imagens de abertura, temas de acolhimento |
| **4:3 (Horizontal Suave)** | Cards de Áreas de Atuação na Home, Foto do Consultório | **720 × 540 px** | Cards visuais, ambientação de consultório |
| **1:1 (Quadrada)** | Seção reflexiva, avatares e ícones | **800 × 800 px** | Folhagens, símbolos e fotos de perfil |

---

## 3. Formatos Recomendados e Nível de Qualidade

1. **Formatos Modernos:**
   - **WebP:** Altamente recomendado. Produz arquivos de 25% a 35% mais leves que o JPEG tradicional mantendo a mesma qualidade visual.
   - **AVIF:** Formato de última geração com compressão ainda superior.
   - **JPEG Progressivo / PNG Otimizado:** Formatos clássicos aceitos nativamente como fallback.
2. **Faixa de Peso Recomendada:**
   - **Retrato Principal do Hero:** Entre **150 KB e 300 KB**.
   - **Capas de Serviços e Artigos:** Entre **120 KB e 250 KB**.
   - **Cards de Áreas e Miniaturas:** Entre **50 KB e 100 KB**.
   - **Logos e Ícones:** Preferencialmente **SVG** (vetoriais, menos de 15 KB).
3. **Fator de Qualidade de Compressão:**
   - Ao exportar imagens em softwares (Photoshop, Canva, Figma, TinyPNG, Squoosh), utilizar nível de qualidade entre **80% e 85%**. Essa faixa remove dados imperceptíveis ao olho humano e reduz drasticamente o tamanho do arquivo.

---

## 4. Como Subir Imagens no Painel Administrativo do Django

O sistema conta com proteções automáticas de validação implementadas no backend:
1. **Limite Máximo por Arquivo:** O Django recusa automaticamente arquivos maiores que **5 MB** para evitar travamentos de upload ou estouro de cota do servidor.
2. **Formatos Permitidos:** São aceitos arquivos com extensões `.jpg`, `.jpeg`, `.png`, `.webp`.
3. **Texto Alternativo Obrigatório:** Ao cadastrar uma imagem (capa de artigo, foto da profissional, card de serviço), sempre preencha o campo **Texto Alternativo (alt)**:
   - *Exemplo correto:* `"Fotografia da Psicóloga Mari Menezes em ambiente acolhedor, sorrindo suavemente."`
   - *Exemplo incorreto:* `"foto1.jpg"` ou `"clique aqui"`.

---

## 5. Ferramentas Gratuitas e Simples para Otimização

A cliente ou os administradores não precisam dominar softwares gráficos complexos. Recomendamos o uso de ferramentas online gratuitas antes do upload:
- **[Squoosh.app](https://squoosh.app/):** Desenvolvido pelo Google, permite arrastar uma foto, ajustar a resolução, converter para WebP e visualizar a nitidez em tempo real.
- **[TinyPNG / TinyJPG](https://tinypng.com/):** Comprime arquivos JPG e PNG em lote com um único clique.
- **Canva:** Ao exportar, selecione o tamanho recomendado em pixels e opte por JPG ou PNG com qualidade padrão.
