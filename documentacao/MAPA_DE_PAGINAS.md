# MAPA DE PÁGINAS — INSTITUTO MENTE EM FOCO
**MAPEAMENTO DE ROTAS, CONTEÚDOS, OBJETIVOS E METAS DE SEO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

---

## 1. VISÃO GERAL DA NAVEGAÇÃO

A navegação do site é projetada para ser linear, intuitiva e desprovida de atritos. O usuário deve conseguir transitar com naturalidade da percepção da sua dor ou dúvida até o canal de acolhimento e agendamento.

```
                    ┌─────────────────────────┐
                    │      INÍCIO (HOME)      │
                    │           /             │
                    └────────────┬────────────┘
                                 │
    ┌────────────────────────────┼────────────────────────────┐
    │                            │                            │
┌───▼──────────┐         ┌───────▼────────┐           ┌───────▼────────┐
│  SOBRE MIM   │         │  ÁREAS / SERV. │           │   CONTEÚDOS    │
│ /sobre-mim/  │         │ (Ver abaixo)   │           │  /conteudos/   │
└───┬──────────┘         └───────┬────────┘           └───────┬────────┘
    │                            │                            │
    └────────────────────────────┼────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │         CONTATO         │
                    │        /contato/        │
                    │   + WhatsApp Direto     │
                    └─────────────────────────┘
```

---

## 2. MATRIZ DETALHADA DE PÁGINAS

| # | Página | URL Prevista | Objetivo Principal | CTA Principal | Conteúdo Chave | Necessidade de Imagem | Necessidade de SEO | Estado Atual |
|---|---|---|---|---|---|---|---|---|
| **01** | **Início (Home)** | `/` | Apresentar o Instituto, acolher o visitante, identificar demandas emocionais, expor áreas e conduzir ao agendamento. | "Quero conhecer o atendimento" & "Falar pelo WhatsApp" | Hero institucional, bloco "momentos da vida", 7 cards de identificação, 5 cards de áreas, apresentação resumida de Mari Menezes, prévia de artigos, FAQ e banner final. | Sim (Alta prioridade): Foto Mari Menezes (Hero ~4:5), foto botânica (~1:1), 5 capas de especialidades (~4:3). | Altíssima: Title e Meta Description institucionais, Open Graph, Schema Organization / MedicalBusiness. | **Implementada / Definitiva (Prompt 05)** |
| **02** | **Sobre Mim** | `/sobre-mim/` | Apresentar detalhadamente a trajetória, abordagem, ética e visão clínica da Psicóloga Mari Menezes. | "Conhecer o atendimento" & WhatsApp | Biografia humanizada, posicionamento integrado (Psicologia + Neuropsicologia), princípios de escuta e ética profissional (sem dados inventados). | Sim: Retrato editorial da profissional (~4:5, `IMG-010`), ambientação do consultório (`IMG-028`). | Alta: Title otimizado para busca pelo nome da profissional, Schema Person / Psychologist. | **Implementada / Definitiva (Prompt 07)** |
| **03** | **Psicologia** | `/servicos/psicologia/` | Esclarecer o funcionamento da psicoterapia clínica individual, indicações e objetivos do acompanhamento. | "Agendar atendimento" & WhatsApp | O que é a psicoterapia, 11 temas trabalhados com cuidado sem diagnósticos, sigilo terapêutico e acolhimento. | Sim: Imagem editorial de acolhimento e escuta (~16:9, `IMG-011`). | Alta: Palavras-chave semânticas ("Psicoterapia", "Acompanhamento emocional", "Psicóloga clínica"). | **Implementada / Definitiva (Prompt 07)** |
| **04** | **Neuropsicologia** | `/servicos/neuropsicologia/` | Apresentar a investigação das relações entre funcionamento cerebral, cognição, emoções e comportamento. | "Agendar atendimento" & WhatsApp | Investigação clínica ética, 8 aspectos cognitivos ("conforme a demanda"), quando considerar uma avaliação, pontes para Avaliação e Reabilitação. | Sim: Imagem editorial (~16:9, `IMG-012`). | Alta: Palavras-chave ("Neuropsicologia", "Funcionamento cognitivo", "Cérebro e emoções"). | **Implementada / Definitiva (Prompt 08)** |
| **05** | **Traumas** | `/servicos/traumas/` | Oferecer acolhimento e compreensão para vivências dolorosas e experiências difíceis do passado. | "Buscar apoio para minha história" & WhatsApp | Mensagem "Quando uma experiência termina, suas marcas podem permanecer", 4 eixos de repercussão, respeito ao tempo individual, frase mestre. | Sim: Imagem sutil, serena, que transmita recomposição e delicadeza (sem melodrama, `IMG-013`). | Alta: Palavras-chave ("Superação de traumas", "Acompanhamento emocional", "Acolhimento de crises"). | **Implementada / Definitiva (Prompt 07)** |
| **06** | **Separação & Recomeços** | `/servicos/separacao-e-recomecos/` | Apoiar a reconstrução pessoal após rupturas conjugais, lutos relacionais e mudanças de ciclo. | "Dar o primeiro passo para o recomeço" & WhatsApp | Mensagem "Separar-se também é reorganizar a própria vida", 7 aspectos essenciais trabalhados, ponte para Novos Relacionamentos. | Sim: Imagem reflexiva, horizontes abertos, serenidade (~16:9, `IMG-014`). | Alta: Palavras-chave ("Término de relacionamento", "Recomeço emocional", "Luto relacional"). | **Implementada / Definitiva (Prompt 07)** |
| **06b**| **Novos Relacionamentos** | `/servicos/novos-relacionamentos/` | Refletir sobre escolhas, limites e expectativas em novas etapas da vida afetiva. | "Conhecer o atendimento" & WhatsApp | Mensagem "Recomeçar não significa esquecer", dois eixos reflexivos (desejo de afeto vs. medo de sofrer), influência do passado e limites. | Sim: Imagem editorial de afeto e diálogo (~16:9, `IMG-027`). | Alta: Palavras-chave ("Novos relacionamentos", "Medo de amar", "Limites no relacionamento"). | **Implementada / Definitiva (Prompt 07)** |
| **07** | **Avaliação (Página Hub)** | `/servicos/avaliacao/` | Diferenciar formalmente Avaliação Psicológica e Avaliação Neuropsicológica, apresentando o fluxo geral. | "Agendar atendimento" & WhatsApp | Distinção e complementaridade conforme a demanda, 2 blocos principais com rotas aprofundadas, fluxo em 6 etapas e orientação técnica. | Sim: Imagem editorial (~16:9, `IMG-012`). | Alta: Palavras-chave ("Avaliação Neuropsicológica", "Avaliação Psicológica", "Investigação cognitiva"). | **Implementada / Definitiva (Prompt 08)** |
| **07a**| **Avaliação Psicológica** | `/servicos/avaliacao-psicologica/` | Esclarecer a investigação estruturada de aspectos emocionais, de personalidade e comportamento. | "Agendar atendimento" & WhatsApp | Metodologia clínica, 6 etapas oficiais do fluxo, devolutiva ética e documento técnico quando indicado. | Sim: Imagem editorial (~16:9, `IMG-013`). | Alta: Palavras-chave ("Avaliação psicológica", "Investigação afetiva e comportamental"). | **Implementada / Definitiva (Prompt 08)** |
| **07b**| **Avaliação Neuropsicológica** | `/servicos/avaliacao-neuropsicologica/` | Mapear o perfil cognitivo e funcional minucioso no contexto da Neuropsicologia. | "Agendar atendimento" & WhatsApp | Dimensões cognitivas examinadas conforme a demanda, fluxo em 6 etapas oficiais, devolutiva e ponte para reabilitação. | Sim: Imagem editorial (~16:9, `IMG-012`). | Alta: Palavras-chave ("Avaliação neuropsicológica", "Mapeamento cognitivo", "Funções executivas"). | **Implementada / Definitiva (Prompt 08)** |
| **08** | **Reabilitação Neurocognitiva** | `/servicos/reabilitacao-neurocognitiva/` | Explicar estratégias individualizadas no cotidiano após avaliação e quando houver indicação. | "Agendar atendimento" & WhatsApp | "Após avaliação e quando houver indicação", estratégias individualizadas, funcionamento cognitivo, vida cotidiana e objetivos da pessoa (sem falsas promessas). | Sim: Imagem editorial (~16:9, `IMG-015`). | Média/Alta: Palavras-chave ("Reabilitação neurocognitiva", "Estratégias cognitivas no cotidiano"). | **Implementada / Definitiva (Prompt 08)** |
| **09** | **Conteúdos (Blog)** | `/conteudos/` | Servir como centro de educação em saúde emocional e cognitiva, autoridade orgânica e atração qualificada. | "Explorar artigos" | Grade paginada de artigos categorizados por temas (Psicologia Clínica, Relacionamentos, Traumas, Neuropsicologia), busca textual e destaque. | Sim: Capa de cada artigo (~16:9) e hero institucional. | Altíssima: Hub de conteúdo com URLs canônicas, paginação amigável e meta tags dinâmicas. | **Implementada / Definitiva (Prompt 09)** |
| **10** | **Artigo Individual** | `/conteudos/<slug>/` | Aprofundar temas específicos com linguagem sensível, fundamentada e acolhedora. | "Gostaria de conversar sobre esse tema?" (CTA contextual ao final) | Texto sanitizado em Markdown seguro, autoria de Mari Menezes, tempo de leitura, data, conexão clínica com serviço relacionado e artigos afins. | Sim: Capa principal de alta resolução (~16:9), acessibilidade com alt. | Máxima: Open Graph completo, Schema BlogPosting, tags canônicas, sanitização estrita anti-XSS. | **Implementada / Definitiva (Prompt 09)** |
| **11** | **Contato & Atendimento** | `/contato/` | Facilitar o contato direto, seguro e ético por mensagem ou WhatsApp comercial, com minimização de dados (LGPD). | "Enviar mensagem" & "Conversar pelo WhatsApp" | Hero editorial, card WhatsApp com link centralizado, dados institucionais condicionais, aviso contra dados sensíveis e formulário com PRG e rate limiting. | Sim: Retrato editorial acolhedor (~4:5, `IMG-010`). | Média: Title e Meta focados em acolhimento e canais oficiais do Instituto. | **Implementada / Definitiva (Prompt 10)** |
| **12** | **Política de Privacidade** | `/politica-de-privacidade/` (alias `/privacidade/`) | Garantir conformidade com a LGPD (Lei 13.709/2018) quanto à coleta mínima de dados e governança. | "Voltar para Contato" | 14 seções factuais detalhadas, minimização de dados, aviso contra dados clínicos, canal institucional e data de atualização. | Não (layout estritamente textual e legível). | Baixa. | **Implementada / Definitiva (Prompt 11)** |
| **13** | **Política de Cookies** | `/politica-de-cookies/` (alias `/cookies/`) | Informar com transparência ativa o uso estrito de cookies de primeira parte e ausência de rastreamento. | "Voltar para Contato" | Tabela técnica com csrftoken, sessionid e messages, ausência de analytics/pixels e guia de gerenciamento no navegador. | Não necessária. | Baixa. | **Implementada / Definitiva (Prompt 11)** |
| **14** | **Páginas de Erro (400, 403, 404, 500)** | N/A (Status HTTP) | Manter o acolhimento do usuário mesmo diante de rotas inexistentes ou falhas de servidor. | "Retornar com segurança para a página inicial" | Mensagem empática ("A página que você procura não foi encontrada, mas estamos aqui para ajudar você."), atalhos para páginas principais. | Opcional: Ícone acolhedor ou ilustração botânica sutil. | Não indexáveis (`noindex, nofollow`). | **Templates Prontos** (com base semântica) |
| **15** | **Robots.txt** | `/robots.txt` | Governança técnica de rastreamento para buscadores web sem revelar rotas administrativas privadas. | N/A (Arquivo de texto puro) | Diretivas condicionais: bloqueio universal em homologação/dev (`Disallow: /`) e liberação com link para sitemap em produção (`Allow: /` + `Sitemap:`). | Não aplicável. | Crítica: Rota técnica fundamental. | **Implementada / Definitiva (Prompt 12)** |
| **16** | **Sitemap.xml** | `/sitemap.xml` | Mapeamento estruturado de URLs públicas para indexação eficiente em mecanismos de busca. | N/A (Documento XML padronizado) | Rotas institucionais, serviços ativos, artigos publicados (exclui rascunhos e futuros) e categorias ativas com artigos. | Não aplicável. | Crítica: XML nativo via `django.contrib.sitemaps`. | **Implementada / Definitiva (Prompt 12)** |

---

## 3. ARTIGOS PREVISTOS PARA O LANÇAMENTO DO BLOG

Conforme diretriz do projeto, o app de conteúdos será preparado com a estrutura para os seguintes temas:

1. `quando-procurar-ajuda-psicologica`: *Quando é o momento de procurar ajuda psicológica?*
2. `por-que-algumas-experiencias-continuam-doendo`: *Por que algumas experiências continuam doendo mesmo depois de anos?*
3. `como-lidar-emocionalmente-com-o-fim-de-um-relacionamento`: *Como lidar emocionalmente com o término de um relacionamento?*
4. `por-que-e-tao-dificil-seguir-depois-de-uma-separacao`: *Por que é tão desafiador seguir em frente após uma separação?*
5. `o-medo-de-amar-novamente`: *O medo de amar novamente: compreendendo as defesas do coração.*
6. `como-estabelecer-limites-em-um-relacionamento`: *Limites saudáveis: como construí-los sem culpa nas relações interpessoais.*
7. `por-que-repetimos-determinados-padroes`: *Por que repetimos determinados padrões emocionais?*
8. `o-que-e-uma-avaliacao-neuropsicologica`: *O que é e como funciona uma avaliação neuropsicológica?*
9. `diferenca-entre-avaliacao-psicologica-e-neuropsicologica`: *Qual a real diferença entre avaliação psicológica e neuropsicológica?*

---

## 4. GOVERNANÇA DE SEO EDITORIAL E ON-PAGE (PROMPT 13)

A auditoria e consolidação editorial implementada no **Prompt 13** assegura:
* **H1 Canônico Único:** Cada uma das 16 URLs públicas renderiza estritamente 1 tag `<h1>`.
* **Hierarquia Estrita:** Títulos de seção em `<h2>` e subtópicos/cartões em `<h3>`.
* **Zero Páginas Órfãs:** Todos os serviços, páginas institucionais e artigos possuem múltiplos links de entrada e saída.
* **Documentação Complementar de SEO Editorial:**
  * [`AUDITORIA_SEO_EDITORIAL.md`](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_SEO_EDITORIAL.md) — Auditoria técnica e semântica completa de cada página.
  * [`MAPA_DE_INTENCOES_SEO.md`](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MAPA_DE_INTENCOES_SEO.md) — Matriz de intenções, dores humanas acolhidas e critérios de não-sobreposição.
  * [`MAPA_DE_LINKS_INTERNOS.md`](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MAPA_DE_LINKS_INTERNOS.md) — Grafo formal de interlinking e navegação contextual.
  * [`PENDENCIAS_EDITORIAIS.md`](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PENDENCIAS_EDITORIAIS.md) — Controle ético de dados e conteúdos deliberadamente não inventados.

---
*Mapeamento concluído e alinhado aos princípios de design, ética clínica e arquitetura do projeto.*
