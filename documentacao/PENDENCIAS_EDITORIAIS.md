# REGISTRO DE PENDÊNCIAS EDITORIAIS E INFORMAÇÕES DO CLIENTE
## INSTITUTO MENTE EM FOCO

Este documento lista formalmente todas as informações institucionais, cadastrais e de conteúdo clínico que **foram deliberadamente NÃO inventadas**, aguardando o fornecimento oficial por parte da cliente (Psicóloga Mari Menezes) para inclusão futura.

---

## 1. COMPROMISSO DE NÃO-INVENÇÃO ÉTICA

Em conformidade com o Código de Ética Profissional do Psicólogo (Resolução CFP nº 010/2005) e com as diretrizes do PROMPT 13:
* Não inventamos dados de identificação profissional.
* Não geramos artigos científicos fictícios com Inteligência Artificial para simular autoridade.
* Não criamos depoimentos de pacientes falsos ("social proof"), prática expressamente vedada no Código de Ética da Psicologia.
* Não inventamos endereço físico ou clínica presencial fictícia para forçar SEO local ("psicóloga em bairro X").

---

## 2. ITENS PENDENTES DE FORNECIMENTO PELA CLIENTE

| Item | Status Atual no Sistema | Como Atualizar Após Recebimento | Impacto no SEO |
| :--- | :--- | :--- | :--- |
| **Número do CRP de Mari Menezes** | Tratado como `PENDENTE_DEFINICAO` e omitido da exibição pública até definição | Inserir no Django Admin (`/admin/nucleo/profissional/`) | Reforçará a credibilidade institucional no rodapé e no Schema.org `Person`. |
| **Endereço Físico do Consultório** | Omitido dos templates e do Schema.org | Cadastrar em `ConfiguracaoSite` no Admin | Ativará o Schema `LocalBusiness`/`MedicalBusiness` e o SEO local. |
| **Redes Sociais Oficiais** | Model `RedeSocial` possui registros inativos ou com flags seguras | Ativar e preencher URLs oficiais no Admin | Integrará os metadados `sameAs` no Schema.org e links no rodapé. |
| **Artigos Autorais para o Blog** | Módulo de Blog implementado e aguardando textos reais; exibe aviso seguro de "Em breve novos conteúdos" | Cadastrar no Django Admin (`/admin/conteudos/artigo/`) | Aumentará a relevância temática orgânica para buscas de cauda longa. |
| **E-mail Institucional Definitivo** | Fallback seguro configurado no settings | Atualizar no Django Admin (`ConfiguracaoSite`) | Comunicação institucional oficial. |

---

## 3. CONTEÚDOS DELIBERADAMENTE NÃO CRIADOS

Os seguintes itens **jamais serão criados de forma automatizada**:
1. **Páginas de Cidades / Bairros Artificiais:** Não foram criadas URLs como `/psicologa-em-sao-paulo/` ou `/terapia-perto-de-mim/`. A atratividade geográfica dependerá exclusivamente de dados de localização física reais fornecidos pela proprietária.
2. **Promessas de Diagnóstico Online:** O site não oferece calculadoras de depressão, ansiedade ou quizzes que induzam a autodiagnósticos perigosos.
3. **Módulo de Comentários Abertos em Artigos:** O Blog opera estritamente como publicação institucional informativa, evitando exposição de dados de saúde de visitantes em comentários públicos.
4. **Popups Invasivos e Exit-Intents:** Nenhuma estratégia manipulativa de retenção de tráfego foi adotada, mantendo o ambiente sereno e respeitoso.
