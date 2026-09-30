# MAPA DE LINKS INTERNOS E ARQUITETURA DE NAVEGAÇÃO
## INSTITUTO MENTE EM FOCO

Este documento mapeia formalmente o **grafo de interlinking** do site do Instituto Mente em Foco, garantindo que não existam páginas órfãs, que a navegação seja contextual e que o fluxo do visitante conduza naturalmente ao acolhimento e contato.

---

## 1. PRINCÍPIOS DE INTERLINKING DO PROJETO

1. **Zero Páginas Órfãs:** Toda página pública possui múltiplos links de entrada provenientes de menus, rodapé e seções contextuais de conteúdo.
2. **Textos-Âncora Naturais e Informativos:** Os links utilizam textos descritivos que esclarecem o destino (ex: *"Conhecer atuação em Novos Relacionamentos"*, *"Entenda a Avaliação Neuropsicológica"*), evitando âncoras vazias como "clique aqui" ou repetições forçadas de palavras-chave.
3. **Profundidade Máxima de 2 Cliques:** Qualquer página de serviço ou artigo do site pode ser alcançada a partir da Home em no máximo 2 cliques.
4. **Respeito aos Rascunhos:** Artigos em status de rascunho nunca recebem links públicos nem figuram em listagens, garantindo integridade editorial.

---

## 2. GRAFO GERAL DE LINKS POR URL

| URL de Origem | URLs de Destino Interno | Tipos de Conexão |
| :--- | :--- | :--- |
| **`/` (Home)** | `/sobre-mim/`<br>`/servicos/psicologia/`<br>`/servicos/neuropsicologia/`<br>`/servicos/traumas/`<br>`/servicos/separacao-e-recomecos/`<br>`/servicos/novos-relacionamentos/`<br>`/servicos/avaliacao/`<br>`/servicos/reabilitacao-neurocognitiva/`<br>`/conteudos/`<br>`/contato/`<br>`/politica-de-privacidade/`<br>`/politica-de-cookies/` | Header global, cards fotográficos de áreas, destaques de serviços, seção de apresentação, preview de artigos, FAQ e rodapé global. |
| **`/sobre-mim/`** | `/`<br>`/servicos/psicologia/`<br>`/servicos/neuropsicologia/`<br>`/servicos/traumas/`<br>`/contato/`<br>`/conteudos/` | Header, bloco de áreas de atuação clínica (`itens_relacionados`), CTA de acolhimento e rodapé. |
| **`/servicos/psicologia/`** | `/`<br>`/servicos/traumas/`<br>`/servicos/separacao-e-recomecos/`<br>`/contato/`<br>`/sobre-mim/` | Header, cards de continuidade do cuidado (`itens_relacionados`), CTA final e rodapé. |
| **`/servicos/traumas/`** | `/`<br>`/servicos/psicologia/`<br>`/servicos/separacao-e-recomecos/`<br>`/contato/` | Header, cards de serviços relacionados, CTA de acolhimento e rodapé. |
| **`/servicos/separacao-e-recomecos/`** | `/`<br>`/servicos/novos-relacionamentos/`<br>`/servicos/psicologia/`<br>`/contato/` | Header, card bidirecional para *Novos Relacionamentos*, card para *Psicologia*, CTA e rodapé. |
| **`/servicos/novos-relacionamentos/`** | `/`<br>`/servicos/separacao-e-recomecos/`<br>`/servicos/psicologia/`<br>`/contato/` | Header, card bidirecional para *Separação e Recomeços*, card para *Psicologia*, CTA e rodapé. |
| **`/servicos/neuropsicologia/`** | `/`<br>`/servicos/avaliacao-neuropsicologica/`<br>`/servicos/reabilitacao-neurocognitiva/`<br>`/servicos/psicologia/`<br>`/contato/` | Header, cards de encaminhamento para *Avaliação* e *Reabilitação*, CTA e rodapé. |
| **`/servicos/avaliacao/` (Hub)** | `/`<br>`/servicos/avaliacao-psicologica/`<br>`/servicos/avaliacao-neuropsicologica/`<br>`/servicos/neuropsicologia/`<br>`/servicos/reabilitacao-neurocognitiva/`<br>`/contato/` | Header, botões comparativos de triagem para as avaliações específicas, cards relacionados, CTA e rodapé. |
| **`/servicos/avaliacao-psicologica/`** | `/`<br>`/servicos/avaliacao/`<br>`/servicos/avaliacao-neuropsicologica/`<br>`/servicos/psicologia/`<br>`/contato/` | Header, breadcrumb de retorno ao Hub de Avaliação, cards comparativos, CTA e rodapé. |
| **`/servicos/avaliacao-neuropsicologica/`** | `/`<br>`/servicos/avaliacao/`<br>`/servicos/reabilitacao-neurocognitiva/`<br>`/servicos/neuropsicologia/`<br>`/servicos/avaliacao-psicologica/`<br>`/contato/` | Header, breadcrumb de retorno ao Hub, cards técnicos de intervenção pós-laudo, CTA e rodapé. |
| **`/servicos/reabilitacao-neurocognitiva/`** | `/`<br>`/servicos/avaliacao-neuropsicologica/`<br>`/servicos/neuropsicologia/`<br>`/servicos/psicologia/`<br>`/contato/` | Header, destaque da necessidade de avaliação prévia com link para *Avaliação Neuropsicológica*, CTA e rodapé. |
| **`/conteudos/` (Blog Index)** | `/`<br>`/conteudos/<slug>/`<br>`/conteudos/categoria/<slug>/`<br>`/servicos/.../`<br>`/contato/` | Header, chips de filtro de categoria, cards de artigos com link ao detalhe, CTA e rodapé. |
| **`/conteudos/<slug>/` (Artigo)** | `/`<br>`/conteudos/`<br>`/conteudos/categoria/<slug>/`<br>`/servicos/<servico_relacionado>/`<br>`/contato/` | Breadcrumb hierárquico, link contextual para o serviço relacionado no corpo e no rodapé do artigo, artigos complementares e CTA. |
| **`/contato/`** | `/`<br>`/politica-de-privacidade/`<br>`/politica-de-cookies/`<br>WhatsApp oficial | Header, links para termos de privacidade no formulário, atalhos de contato direto e rodapé. |
| **`/politica-de-privacidade/`** | `/`<br>`/contato/`<br>`/politica-de-cookies/` | Header, links de canal de privacidade, rodapé e navegação institucional. |
| **`/politica-de-cookies/`** | `/`<br>`/contato/`<br>`/politica-de-privacidade/` | Header, links de esclarecimento institucional e rodapé. |

---

## 3. AUDITORIA DE PÁGINAS ÓRFÃS

Uma página órfã é uma URL pública sem links internos que a apontem a partir do próprio domínio.

* **Páginas Auditadas:** 16 URLs públicas
* **Páginas Órfãs Encontradas:** 0
* **Páginas Órfãs Restantes:** 0

### Distribuição de Inbound Links (Métricas Reais):
* Home (`/`): 15 links de entrada
* Sobre Mim (`/sobre-mim/`): 15 links de entrada
* Psicologia (`/servicos/psicologia/`): 15 links de entrada
* Neuropsicologia (`/servicos/neuropsicologia/`): 15 links de entrada
* Traumas (`/servicos/traumas/`): 15 links de entrada
* Separação & Recomeços (`/servicos/separacao-e-recomecos/`): 15 links de entrada
* Avaliação Hub (`/servicos/avaliacao/`): 15 links de entrada
* Reabilitação Neurocognitiva (`/servicos/reabilitacao-neurocognitiva/`): 15 links de entrada
* Blog / Conteúdos (`/conteudos/`): 15 links de entrada
* Contato (`/contato/`): 15 links de entrada
* Privacidade (`/politica-de-privacidade/`): 15 links de entrada
* Cookies (`/politica-de-cookies/`): 15 links de entrada
* Avaliação Neuropsicológica (`/servicos/avaliacao-neuropsicologica/`): 4 links de entrada diretos e contextuais
* Avaliação Psicológica (`/servicos/avaliacao-psicologica/`): 2 links de entrada diretos e contextuais
* Novos Relacionamentos (`/servicos/novos-relacionamentos/`): 2 links de entrada diretos e contextuais

> [!NOTE]
> As páginas temáticas de segundo nível (`novos-relacionamentos`, `avaliacao-psicologica` e `avaliacao-neuropsicologica`) estão integradas organicamente nas suas respectivas páginas mães e nos cards de páginas relacionadas, preservando a limpeza e usabilidade do cabeçalho principal.

---

## 4. AUDITORIA DE TEXTOS-ÂNCORA (ANCHOR TEXTS)

A auditoria dos textos-âncora assegura naturalidade sem repetições robotizadas:

1. **Links Globais de Navegação:**
   * Utilizam nomes institucionais diretos: *"Início"*, *"Sobre Mim"*, *"Conteúdos & Artigos"*, *"Contato & Agendamento"*, *"Psicologia Clínica"*, *"Neuropsicologia Clínica"*, etc.
2. **Links de Continuidade de Cuidado (`itens_relacionados`):**
   * Utilizam convites reflexivos: *"Conhecer atuação"*, *"Entenda a Avaliação"*, *"Ver estratégias de reabilitação"*.
3. **Links de Fechamento de Página (CTAs):**
   * Utilizam chamadas focadas na autonomia do visitante: *"Conversar pelo WhatsApp"*, *"Entrar em contato"*, *"Comece por você"*.
