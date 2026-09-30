# PENDÊNCIAS VISUAIS PÓS-FOTOS — INSTITUTO MENTE EM FOCO
**CATÁLOGO DE AJUSTES VISUAIS E CALIBRAÇÕES CONDICIONADAS AO RECEBIMENTO DAS FOTOGRAFIAS DEFINITIVAS**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA CSS

---

## 1. CONTEXTO E PROPÓSITO DESTE DOCUMENTO

Durante as etapas de desenvolvimento e auditoria visual dos Prompts 01 a 20, foram rigorosamente preservados os slots de mídia estruturais com `aspect-ratio` nativo e placeholders nobres em SVG/CSS, respeitando a regra inegociável de **não utilizar imagens de banco genérico (stock photos) ou inteligência artificial gerativa**.

Este documento cataloga de forma exaustiva os ajustes visuais finos (recorte, `object-position`, gradientes de contraste e pontos focais) que deverão ser executados imediatamente após a entrega das fotografias reais produzidas no ensaio da profissional.

---

## 2. MATRIZ DE CALIBRAÇÃO VISUAL PÓS-FOTOS

| Slot / ID | Página e Seção | Proporção | Descrição / Objeto da Foto | Ponto Focal Recomendado | Ajuste CSS Específico a Aplicar | Risco de Contraste e Mitigação |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **IMG-001** | Home • Hero Principal | `4:5` | Retrato editorial de Mari Menezes em ambiente clínico acolhedor | Olhar / Busto superior (~20% do topo) | `object-position: center 20%;` | **ENTREGUE & ATIVA:** Foto real da profissional vinculada ao model `Profissional.foto_principal`. Enquadramento e contraste certificados sem overflow horizontal. |
| **IMG-002** | Home • Seção Introdução | `1:1` | Composição botânica delicada ou detalhe do consultório | Centro geométrico | `object-position: center center;` | Sem texto sobreposto. Atenção para que os tons verdes da folhagem harmonizem com `--cor-salvia` e `--cor-oliva`. |
| **IMG-003** | Home • Áreas: Psicologia | `4:3` | Consultório, poltrona de atendimento ou acolhimento | Centro / Terço superior | `object-position: center 30%;` | **Texto sobreposto:** O overlay `rgba(45, 41, 38, 0.75)` na base garante contraste WCAG AAA para o título em branco. Calibrar opacidade se a foto for muito clara. |
| **IMG-004** | Home • Áreas: Neuropsicologia | `4:3` | Instrumentos de avaliação cognitiva ou mesa de trabalho serena | Centro / Detalhes de prancheta | `object-position: center 40%;` | Verificar se reflexos em mesas de madeira não criam pontos quentes sob o título da especialidade. |
| **IMG-005** | Home • Áreas: Traumas | `4:3` | Detalhe sutil, luz natural atravessando janela ou arte acolhedora | Centro suave | `object-position: center center;` | Evitar composições dramáticas ou sombrias; manter o tom de esperança e reconstrução. |
| **IMG-006** | Home • Áreas: Separação | `4:3` | Caminho sereno, espaço aberto acolhedor ou novo horizonte | Centro / Terço médio | `object-position: center 35%;` | Preservar a harmonia com o gradiente escuro inferior. |
| **IMG-007** | Home • Áreas: Novos Relacionamentos | `4:3` | Conexão, café, encontro ou ambiente de diálogo acolhedor | Centro / Ângulo aberto | `object-position: center 40%;` | Assegurar que os pontos de foco fiquem acima dos 30% inferiores do cartão. |
| **IMG-010** | Sobre Mim • Hero / Perfil | `4:5` | Retrato expressivo de Mari Menezes em postura atenta e humana | Olhar / Terço superior | `object-position: center 15%;` | Foto vertical ao lado da biografia formal. Verificar se a orientação da cabeça aponta suavemente para o texto. |
| **IMG-011** | Sobre Mim • Espaço Clínico | `16:9` | Foto ampla do consultório do Instituto Mente em Foco | Centro espacial | `object-position: center center;` | Banner horizontal de acolhimento. Ajustar enquadramento em mobile para destacar a poltrona de atendimento. |
| **IMG-012 a 017** | Páginas de Serviços Específicos | `16:9` | Capas conceituais para cada um dos 6 serviços clínicos | Terço superior | `object-position: center 25%;` | Banners de cabeçalho das páginas técnicas. Testar contraste dos títulos H1 em relação à luminosidade das fotos. |
| **IMG-020+** | Blog • Capas de Artigos | `16:9` | Fotografias editoriais temáticas para cada publicação | Centro / Regra dos terços | `object-position: center center;` | Assegurar padrão fotográfico coeso com a paleta oficial (evitar saturação excessiva). |

---

## 3. CHECKLIST OPERACIONAL PARA INSERÇÃO DAS FOTOS DEFINITIVAS

Quando os arquivos digitais de alta resolução forem disponibilizados:

1. **Otimização Prévia de Mídia:**
   * Converter os arquivos originais para o formato moderno **WebP** com compressão de qualidade a 85%.
   * Limitar a dimensão máxima horizontal a `1920px` para banners panorâmicos e `1200px` para retratos verticais.
   * Certificar-se de que o peso final de cada arquivo não ultrapasse **350 KB** (idealmente $< 200\text{ KB}$).
2. **Submissão via Django Admin:**
   * Acessar o painel administrativo (`/admin/nucleo/profissional/1/change/` e `/admin/servicos/areaatuacao/`).
   * Fazer o upload das imagens nos campos correspondentes (o validador Pillow já configurado inspecionará o binário e gerará caminhos UUID únicos).
3. **Inspeção de `object-position`:**
   * Testar a renderização em 390px (iPhone), 768px (iPad) e 1440px (Desktop).
   * Caso o corte automático central corte o topo da cabeça ou pontos vitais, ajustar a propriedade `object-position` no CSS específico da página.
4. **Verificação de Legibilidade:**
   * Confirmar se todos os textos sobrepostos nos cartões de áreas e banners mantêm razão de contraste mínima de **4.5:1** em relação à fotografia de fundo.

---

## 4. CONCLUSÃO

A arquitetura do site está 100% preparada e estruturada para receber as fotografias definitivas sem necessidade de qualquer alteração estrutural em HTML, sem migrações de banco de dados e sem risco de regressão responsiva.
