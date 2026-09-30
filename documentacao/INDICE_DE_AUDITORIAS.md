# ÍNDICE DE AUDITORIAS E DOCUMENTOS
## Instituto Mente em Foco — Guia de Prioridade de Leitura para o Astra

> [!NOTE]
> Este índice orienta o GPT Astra 6 sobre quais documentos ler e em qual ordem.
> **PRIORIDADE 1:** Ler antes de qualquer auditoria.
> **PRIORIDADE 2:** Consultar para contexto específico da área auditada.
> **REFERÊNCIA:** Consultar apenas se necessário para informação histórica específica.

> [!CAUTION]
> Documentos marcados como **HISTÓRICO** podem estar desatualizados.
> Verificar sempre o código real — o código é a única fonte de verdade confiável.

---

## PRIORIDADE 1 — Ler Antes de Qualquer Auditoria

> [!IMPORTANT]
> Estes documentos formam o contexto mínimo obrigatório para qualquer sessão de auditoria.
> Leia todos antes de inspecionar código ou emitir qualquer diagnóstico.

| ARQUIVO | PROMPT | OBJETIVO | ESTADO | NOTAS |
|---|---|---|---|---|
| `CONTEXTO_PARA_GPT_ASTRA_6.md` | 23 | Transferência de contexto técnico verificado para o Astra | ✅ Atual | **Leia primeiro. Substitui contextos anteriores.** |
| `AUDITORIA_FINAL_PRE_ASTRA.md` | — | Estado consolidado do projeto antes das auditorias Astra | ⚠️ A criar | Documento planejado — verificar se existe |
| `CONTRADICOES_ENCONTRADAS.md` | — | Registro de contradições entre docs e código real | ⚠️ A criar | Principal: health check text/plain vs. JSON |
| `ARQUITETURA_PLANEJADA.md` | — | Diagrama e descrição da arquitetura modular | ✅ Existe | Verificar se condiz com código atual |
| `MAPA_DE_PAGINAS.md` | — | Mapa de todas as páginas, rotas e templates | ✅ Existe | Conferir contra `urls.py` real |
| `DESIGN_SYSTEM.md` | — | Tokens, tipografia, componentes, CSS modular | ✅ Existe | Fonte de verdade visual |
| `GUIA_DO_ADMIN.md` | — | Funcionamento do Django Admin customizado | ✅ Existe | |
| `INVENTARIO_DE_SECRETS.md` | — | Lista de variáveis sensíveis e onde são usadas | ✅ Existe | |
| `MATRIZ_VARIAVEIS_AMBIENTE.md` | — | Todas as env vars, valores padrão, obrigatoriedade | ✅ Existe | |
| `PENDENCIAS_DO_CLIENTE.md` | — | Itens bloqueadores aguardando o cliente | ✅ Existe | |
| `PENDENCIAS_VISUAIS_POS_FOTOS.md` | — | O que fazer assim que as fotos reais chegarem | ✅ Existe | |
| `CHECKLIST_GO_LIVE.md` | — | Checklist completo para go-live em produção | ✅ Existe | |
| `PLANO_DE_AUDITORIAS_ASTRA.md` | — | Planejamento das sessões Astra 01–Final | ⚠️ A criar | Documento planejado |
| `MAPA_DE_PRODUCAO_DE_IMAGENS.md` | — | Status de todas as imagens (Grupo A e B) | ⚠️ A criar | Documento planejado |
| `DIRECAO_FOTOGRAFICA_IA.md` | — | Briefs de geração de imagens editoriais (IMG-003 a IMG-013) | ⚠️ A criar | Documento planejado |

---

## PRIORIDADE 2 — Consultar por Área de Auditoria

### 🔐 Segurança

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_DE_SEGURANCA.md` | Auditoria de segurança detalhada | ⚠️ HISTÓRICO — verificar contra código |
| `CHECKLIST_DE_SEGURANCA_PRODUCAO.md` | Checklist de hardening para produção | ✅ Útil como referência |
| `SEGURANCA_E_HARDENING.md` | Guia de hardening aplicado | ✅ Existe |
| `AUDITORIA_DE_ABUSO_E_RATE_LIMIT.md` | Auditoria de rate limit e proteção contra abuso | ⚠️ HISTÓRICO — LocMemCache não distribuído |
| `PROTECAO_CONTRA_ABUSO.md` | Estratégias de proteção contra abuso | ✅ Existe |
| `GUIA_DE_INCIDENTES_DE_ABUSO.md` | Procedimentos de resposta a incidentes | ✅ Existe |
| `MATRIZ_DE_RATE_LIMIT.md` | Matriz completa de rate limiting | ✅ Existe |
| `TERCEIROS_E_COOKIES.md` | Análise de terceiros, cookies e rastreamento | ✅ Existe |

### ⚡ Performance

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_DE_PERFORMANCE.md` | Auditoria de performance | ⚠️ HISTÓRICO |
| `PERFORMANCE_E_CORE_WEB_VITALS.md` | Análise de Core Web Vitals | ✅ Existe |
| `GUIA_DE_IMAGENS_E_PERFORMANCE.md` | Otimização de imagens e impacto na performance | ✅ Existe |

### 🔎 SEO

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_SEO_TECNICO.md` | Auditoria técnica de SEO | ⚠️ HISTÓRICO |
| `AUDITORIA_SEO_EDITORIAL.md` | Auditoria editorial de SEO (conteúdo) | ⚠️ HISTÓRICO |
| `SEO_TECNICO.md` | Guia de SEO técnico implementado | ✅ Existe |
| `MAPA_DE_INTENCOES_SEO.md` | Mapa de intenções de busca por página | ✅ Existe |
| `MAPA_DE_LINKS_INTERNOS.md` | Estrutura de links internos | ✅ Existe |

### ♿ Acessibilidade

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_DE_ACESSIBILIDADE.md` | Auditoria WCAG 2.2 AA | ⚠️ HISTÓRICO |
| `GUIA_RESPONSIVO.md` | Guia de responsividade e acessibilidade mobile | ✅ Existe |

### 🧪 Funcional

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_FUNCIONAL_COMPLETA.md` | Auditoria funcional de todos os fluxos | ⚠️ HISTÓRICO |
| `ESTRATEGIA_DE_TESTES.md` | Estratégia e filosofia de testes | ✅ Existe |
| `MATRIZ_DE_TESTES.md` | Matriz completa de casos de teste | ✅ Existe |
| `MATRIZ_DE_FLUXOS_FUNCIONAIS.md` | Fluxos funcionais críticos mapeados | ✅ Existe |
| `GUIA_DE_REGRESSAO.md` | Guia de testes de regressão | ✅ Existe |
| `AUDITORIA_DA_SUITE_DE_TESTES.md` | Auditoria da suite de testes automatizados | ✅ Existe |

### 📱 Responsividade

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_RESPONSIVA_E_CROSS_BROWSER.md` | Auditoria responsiva e cross-browser | ⚠️ HISTÓRICO |
| `MATRIZ_RESPONSIVA.md` | Matriz de breakpoints e comportamento | ✅ Existe |
| `MATRIZ_CROSS_BROWSER.md` | Matriz de compatibilidade cross-browser | ✅ Existe |

### 🎨 Visual / Design

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_VISUAL_FINAL.md` | Auditoria visual e UI | ⚠️ HISTÓRICO |
| `GUIA_DE_CONSISTENCIA_VISUAL.md` | Guia de consistência do design | ✅ Existe |
| `INVENTARIO_DE_COMPONENTES_VISUAIS.md` | Inventário de componentes visuais | ✅ Existe |
| `INVENTARIO_DE_IMAGENS.md` | Inventário de imagens e status | ✅ Existe |

### 🚀 Produção / Deploy

| ARQUIVO | OBJETIVO | ESTADO |
|---|---|---|
| `AUDITORIA_PRONTIDAO_PRODUCAO.md` | Auditoria de prontidão para produção | ⚠️ HISTÓRICO |
| `GUIA_DEPLOY_PRODUCAO.md` | Guia completo de deploy em produção | ✅ Existe |
| `DECISOES_DE_INFRAESTRUTURA.md` | Decisões de infraestrutura registradas | ✅ Existe |
| `PLANO_BACKUP_E_RESTAURACAO.md` | Plano de backup e restauração | ✅ Existe |
| `PLANO_ROLLBACK.md` | Procedimento de rollback | ✅ Existe |

---

## REFERÊNCIA — Consultar Se Necessário

> [!NOTE]
> Documentos mais históricos, específicos ou detalhados. Úteis para contexto adicional,
> mas não essenciais para início de auditoria.

| ARQUIVO | CONTEÚDO | ESTADO |
|---|---|---|
| `CONTEXTO_MESTRE.md` | Requisitos originais completos do projeto | ✅ HISTÓRICO — fonte primária de requisitos |
| `HISTORICO_DE_IMPLEMENTACAO.md` | Log de decisões e implementações ao longo do projeto | ✅ HISTÓRICO |
| `CHECKLIST_DE_QUALIDADE.md` | Checklist geral de qualidade | ⚠️ HISTÓRICO |
| `MAPA_DE_DADOS.md` | Mapeamento de dados e modelos | ✅ Existe — verificar contra `models.py` |
| `INVENTARIO_DE_ROTAS_E_LINKS.md` | Inventário completo de rotas | ✅ Existe — verificar contra `urls.py` |
| `PENDENCIAS_EDITORIAIS.md` | Pendências de conteúdo editorial | ✅ Existe |

---

## DOCUMENTOS NOVOS CRIADOS NO PROMPT 23

Os seguintes documentos foram criados nesta sessão (Prompt 23):

| # | ARQUIVO | DESCRIÇÃO |
|---|---|---|
| 1 | `CONTEXTO_PARA_GPT_ASTRA_6.md` | Pacote de transferência de contexto técnico verificado para o Astra 6 |
| 2 | `INDICE_DE_AUDITORIAS.md` | Este índice — guia de prioridade de leitura para o Astra |

> [!NOTE]
> Os demais documentos listados como **"A criar"** na tabela de Prioridade 1
> (`AUDITORIA_FINAL_PRE_ASTRA.md`, `CONTRADICOES_ENCONTRADAS.md`,
> `PLANO_DE_AUDITORIAS_ASTRA.md`, `MAPA_DE_PRODUCAO_DE_IMAGENS.md`,
> `DIRECAO_FOTOGRAFICA_IA.md`) são planejados para criação em prompts futuros
> conforme o andamento das auditorias Astra.

---

## LEGENDA DE ESTADOS

| Símbolo | Significado |
|---|---|
| ✅ Atual | Documento verificado e confiável como referência |
| ✅ Existe | Documento existe — verificar se condiz com código atual |
| ⚠️ HISTÓRICO | Documento histórico — pode estar desatualizado; verificar código real |
| ⚠️ A criar | Documento planejado mas ainda não existente |
| 🔴 | Release blocker — item crítico para go-live |
