# PLANO DE GERAÇÃO DE IMAGENS — SÉRIE ASTRA
## Instituto Mente em Foco — Processo Visual para o GPT Astra

> [!IMPORTANT]
> Este plano define o processo de produção visual para o Astra 03.
> NÃO gerar imagens sem validação da direção de arte.
> NÃO substituir fotos da Mari por IA.

---

## 1. OBJETIVO

Produzir assets visuais editoriais de alta qualidade para o Instituto Mente em Foco, garantindo consistência, ética e fidelidade à identidade visual do projeto.

Cada imagem deve:
- Parecer fotografia profissional editorial real (não banco de imagens)
- Ser ética (sem exploração de sofrimento, sem dramatização)
- Ser compatível com a paleta de design tokens do projeto
- Integrar-se ao layout com espaço negativo adequado
- Ser responsiva (crop desktop e mobile viáveis)

---

## 2. DIREÇÃO DE ARTE

**Referência obrigatória:** `DIRECAO_FOTOGRAFICA_IA.md`

**Resumo da linguagem visual:**
- Fotografia editorial realista
- Paleta quente e terrosa — areia #D8C5A8, off-white #F7F3EB, sálvia #A8B09A, oliva #56664B, dourado #C9A86A, taupe #6D655B
- Luz natural suave (janelas, tarde, difusa)
- Sem clichês clínicos
- Sem sofrimento explorado ou dramatizado
- Consistência entre todas as imagens do projeto
- Espaço negativo para sobreposição de texto em todas as imagens de hero

> [!NOTE]
> A referência ao arquivo `DIRECAO_FOTOGRAFICA_IA.md` é obrigatória antes de qualquer geração.
> Se o arquivo não estiver acessível, solicitar ao responsável antes de prosseguir.

---

## 3. IMAGENS REAIS — GRUPO A (NÃO GERAR POR IA)

> [!CAUTION]
> ESTES SLOTS SÃO BLOQUEADOS PARA GERAÇÃO POR IA.
> Aguardar fornecimento das fotografias reais pela cliente.
> Nenhuma imagem simulada de Mari Menezes deve ser gerada em nenhuma hipótese.

| ID | Descrição | Ratio | Status |
|----|-----------|-------|--------|
| IMG-001 | Foto Hero de Mari Menezes | 4:5 | ⏳ PENDENTE — aguardando cliente |
| IMG-002 | Foto Sobre Mim de Mari Menezes | 4:5 | ⏳ PENDENTE — aguardando cliente |

**Slots reservados:** Hero da página inicial e seção Sobre Mim.
**Ação:** Implementar placeholders de dimensão correta até chegada das fotos reais.

---

## 4. IMAGENS IA — GRUPO B

Todas as imagens temáticas editoriais a serem geradas por IA. Briefs completos disponíveis em `BRIEFS_DE_GERACAO_DE_IMAGEM.md`.

| ID | Nome | Página | Ratio | Status |
|----|------|--------|-------|--------|
| IMG-003 | *(reservado — verificar documentação)* | — | — | ⏳ Verificar |
| IMG-004 | Psicologia | /servicos/psicologia/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-005 | Traumas | /servicos/traumas/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-006 | Separação e Recomeços | /servicos/separacao-recomecos/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-007 | Novos Relacionamentos | /servicos/novos-relacionamentos/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-008 | Neuropsicologia | /servicos/neuropsicologia/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-009 | Avaliação Psicológica | /servicos/avaliacao-psicologica/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-010 | Avaliação Neuropsicológica | /servicos/avaliacao-neuropsicologica/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-011 | Reabilitação Neurocognitiva | /servicos/reabilitacao-neurocognitiva/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-012 | Avaliação Hub | /servicos/avaliacao/ | 16:9 | ✅ BRIEF PRONTO |
| IMG-013 | OG Image Institucional | Redes sociais (og:image) | 1200×630 (1.9:1) | ✅ BRIEF PRONTO |

---

## 5. LOTE PILOTO (PRIMEIRAS 3 IMAGENS PARA VALIDAÇÃO)

> [!IMPORTANT]
> Gerar APENAS estas 3 imagens no primeiro ciclo.
> NÃO gerar todas as 11 imagens de uma vez.
> O lote piloto valida se a linguagem fotográfica está consistente antes de expandir.

### Imagens do lote piloto:

**1. IMG-006: Separação e Recomeços**
- Tema com restrições visuais claras (sem clichês de separação)
- Permite testar tratamento ético e editorial em tema sensível
- Testa representação de pessoa em movimento/autonomia

**2. IMG-005: Traumas**
- Tema sem pessoas obrigatórias
- Permite testar composição de luz e ambiente pura
- Testa a capacidade de transmitir emoção sem figura humana

**3. IMG-008: Neuropsicologia**
- Tema abstrato — composição de objetos
- Permite testar composição sem figura humana e sem elementos proibidos tecnológicos
- Testa flat-lay editorial e hierarquia visual

### Por que estas 3:

São visualmente distintas entre si:
- **IMG-006:** Pessoa em paisagem natural (exterior, movimento)
- **IMG-005:** Atmosfera de luz e ambiente (interior, sem pessoa)
- **IMG-008:** Composição de objetos (flat-lay, cognição)

Isso permite avaliar se a **linguagem fotográfica permanece consistente** em diferentes abordagens formais antes de expandir para as demais imagens.

---

## 6. CRITÉRIOS DE APROVAÇÃO

Para cada imagem gerada, aplicar este checklist completo:

### Qualidade Visual
- [ ] Parece fotografia profissional real
- [ ] Não parece banco de imagens genérico
- [ ] Não parece imagem gerada por IA (naturalismo)
- [ ] Mãos e rostos naturais (quando houver)

### Ética e Adequação
- [ ] Tema representado sem literalidade
- [ ] Nenhum elemento ético inadequado
- [ ] Sem dramatização de sofrimento
- [ ] Sem instrumentos psicológicos identificáveis
- [ ] Sem imagem de Mari simulada
- [ ] Sem clichês clínicos

### Identidade Visual
- [ ] Paleta compatível com design tokens
- [ ] Composição integra com layout (espaço negativo adequado)
- [ ] Consistência com outras imagens aprovadas

### Responsividade e Implementação
- [ ] Crop mobile possível (4:5 ou 1:1 sem perder leitura)
- [ ] Crop desktop adequado (16:9 ou 1.9:1 conforme especificado)
- [ ] Sem texto gerado na imagem
- [ ] Sem logos ou marcas

---

## 7. FLUXO DE PRODUÇÃO

```
Validação pelo Astra 03
        ↓
Consulta ao DIRECAO_FOTOGRAFICA_IA.md
        ↓
Geração do Lote Piloto (3 imagens)
        ↓
Revisão Visual + Revisão Ética
        ↓
┌─────────────────────────────────────┐
│  Aprovado?                          │
│  SIM → Expansão para restante       │
│  NÃO → Regenerar ou ajustar prompt  │
└─────────────────────────────────────┘
        ↓
Crop para mobile e desktop
        ↓
Nomeação descritiva (kebab-case)
        ↓
Otimização (WebP, dimensões corretas)
        ↓
Implementação no template/CMS
        ↓
Definição de alt text (após ver imagem real)
        ↓
Teste de responsividade
        ↓
Teste de performance (LCP, CLS)
```

> [!WARNING]
> A definição do alt text deve ocorrer SOMENTE após ver a imagem real gerada.
> Nunca definir alt text baseado no prompt — a imagem real pode diferir.

---

## 8. IMPLEMENTAÇÃO

### Formato e Otimização
- **Formato principal:** WebP
- **Fallback:** PNG ou JPG (para browsers sem suporte a WebP)
- **Qualidade WebP:** 85% (balancear qualidade e tamanho)
- **Dimensões mínimas:** Conforme especificado no brief de cada imagem

### Nomeação de Arquivos
Padrão: `kebab-case descritivo + sufixo de contexto`

Exemplos:
```
separacao-recomecos-editorial.webp
traumas-luz-interior.webp
neuropsicologia-organizacao.webp
psicologia-reflexao.webp
og-image-institucional.webp
```

### Implementação por Contexto

| Contexto | Implementação |
|----------|---------------|
| Páginas de serviço (hero interno) | CSS `background-image` ou `<img>` com `aspect-ratio: 16/9` |
| OG Image | Meta tag `og:image` — URL absoluta |
| Blog (imagem de capa) | Campo `imagem_capa` no model `Artigo` |

> [!NOTE]
> Imagens de blog devem ser geradas **somente quando o artigo estiver pronto para publicação**.
> Não gerar imagens de blog antecipadamente para artigos em rascunho.

---

## 9. QA FINAL

> [!IMPORTANT]
> Antes de qualquer implementação em produção, executar todos os itens abaixo.

### Validação Visual e Ética
- [ ] Validação visual por humano (não apenas pelo Astra)
- [ ] Validação ética: nenhuma imagem sugere paciente real
- [ ] Nenhuma imagem sugere diagnóstico específico
- [ ] Nenhuma imagem explora sofrimento

### Performance
- [ ] Teste de LCP (Largest Contentful Paint) — imagem hero não deve ser gargalo
- [ ] Teste de CLS (Cumulative Layout Shift) — dimensões definidas no HTML/CSS
- [ ] Tamanho de arquivo adequado (hero: idealmente < 150KB em WebP)

### Acessibilidade
- [ ] Alt text definido e apropriado para todas as imagens informativas
- [ ] Imagens decorativas com `alt=""`
- [ ] Teste com leitor de tela

---

## 10. ACESSIBILIDADE

### Regras para Alt Text

**Imagens decorativas (apenas estéticas):**
```html
<img src="..." alt="">
```

**Imagens informativas (contextualizam o conteúdo):**
```html
<img src="..." alt="Pessoa caminhando em jardim ao entardecer">
```

### O que NÃO escrever no alt text:
- ❌ `"Paciente superando trauma"`
- ❌ `"Mulher com depressão em terapia"`
- ❌ `"Terapeuta ajudando paciente ansioso"`
- ❌ Keyword stuffing: `"Psicologia psicóloga terapia online São Paulo"`

### O que escrever:
- ✅ Descrição objetiva e neutra da cena real
- ✅ Máximo de 125 caracteres
- ✅ Baseado na imagem real gerada, não no prompt

> [!WARNING]
> Definir o alt text SOMENTE após ver a imagem real gerada e aprovada.
> O alt text descreve o que está na imagem — não o conceito que motivou a geração.

---

## 11. AVISO ASTRA 03

O **Astra 03** (UI/UX, Frontend, Acessibilidade e Direção Visual) é responsável por:

1. **Auditar e aprovar** a direção de arte deste documento e do `DIRECAO_FOTOGRAFICA_IA.md`
2. **Gerar o lote piloto** de 3 imagens (IMG-006, IMG-005, IMG-008)
3. **Validar visual e eticamente** cada imagem do lote piloto
4. **Se aprovado:** expandir para as demais imagens do Grupo B
5. **Implementar** com otimização, responsividade e acessibilidade corretas

> [!CAUTION]
> NÃO gerar as 11 imagens de uma vez sem validar o lote piloto.
> NÃO implementar imagens não validadas.
> NÃO gerar imagens da Mari Menezes (Grupo A) sob nenhuma circunstância.
> NÃO definir alt text antes de ver a imagem real gerada.

---

*Documento criado para uso interno do projeto Instituto Mente em Foco.*
*Versão inicial — sujeito a revisão pelo Astra 03 antes do início da produção.*
