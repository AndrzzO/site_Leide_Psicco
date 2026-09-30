# MATRIZ DE FLUXOS FUNCIONAIS — INSTITUTO MENTE EM FOCO
**MAPEAMENTO SISTEMÁTICO DE JORNADAS DE USUÁRIO, ENTRADAS, RESULTADOS E COBERTURA DE TESTES**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA JS

---

## 1. INTRODUÇÃO E CLASSIFICAÇÃO DE ATORES

Esta matriz detalha os fluxos operacionais completos executados no sistema do **Instituto Mente em Foco**, catalogando as interações para cada categoria de usuário:

* **Visitante / Paciente Potencial:** Usuário anônimo navegando pela interface pública à procura de acolhimento, informações clínicas, leitura de artigos ou agendamento de atendimento via WhatsApp / Contato.
* **Administrador / Psicóloga Mari Menezes:** Usuário autenticado com privilégios de staff no Django Admin responsável pela gestão de conteúdos, publicação de artigos e triagem de contatos.
* **Sistema / Daemon Operacional:** Processos automáticos do backend executando expurgo de retenção de contatos (LGPD), aplicação de rate limit e geração de sitemaps.

---

## 2. MATRIZ DETALHADA DE FLUXOS OPERACIONAIS

| ID | FLUXO | TIPO DE USUÁRIO | ENTRADA | PASSOS EXECUTADOS | RESULTADO ESPERADO | ERROS POSSÍVEIS TRATADOS | TESTE AUTOMATIZADO? | TESTE MANUAL? | STATUS |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **FLX-01** | Visita à Home e Apresentação | Visitante | URL `/` | 1. Acesso à rota raiz.<br>2. Leitura da Hero.<br>3. Rolagem pelas 11 seções clínicas. | Renderização de 100% dos blocos, Hero assimétrico, 7 cards de acolhimento e 5 áreas. | Falha de carregamento de mídia (tratada com placeholders nativos). | SIM (`paginas/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-02** | Navegação para Especialidades Clínicas | Visitante | Clique em card ou menu | 1. Seleção de área clínica (ex: `/servicos/psicologia/`).<br>2. Leitura dos detalhes técnicos e abordagens. | Exibição de página especializada com cabeçalho institucional e CTAs. | Rota inexistente (retorna 404 acolhedor). | SIM (`servicos/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-03** | Início de Contato via WhatsApp | Visitante | Clique no CTA de WhatsApp | 1. Clique em botão "Falar pelo WhatsApp" ou botão flutuante.<br>2. Redirecionamento para API wa.me. | Abertura do WhatsApp com mensagem de acolhimento pré-formatada em UTF-8. | Número não configurado (degrada graciosamente para página de Contato). | SIM (`nucleo/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-04** | Envio de Mensagem pelo Formulário | Visitante | Dados de contato no form | 1. Acesso a `/contato/`.<br>2. Preenchimento de nome, e-mail/telefone e mensagem.<br>3. Aceite da política.<br>4. Submissão. | Gravação segura no banco, redirecionamento PRG (HTTP 302 -> 200) e mensagem de confirmação. | Dados incompletos (erros nos campos); honeypot preenchido (descarte); rate limit excedido (HTTP 429). | SIM (`contato/tests.py`, `tests_rate_limit.py`) | SIM | **OPERACIONAL** |
| **FLX-05** | Consulta e Busca no Blog | Visitante | Termo de busca em `/conteudos/` | 1. Digitação de termo na barra de pesquisa.<br>2. Submissão via GET `?q=...`.<br>3. Navegação entre páginas de resultado. | Exibição de artigos correspondentes com query preservada na paginação. | Termo muito longo (truncado a 100 chars); tentativa de XSS (escapada); sem resultados (empty state claro). | SIM (`conteudos/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-06** | Leitura de Artigo Editorial | Visitante | Slug do artigo | 1. Clique em card de artigo na listagem ou Home.<br>2. Leitura do texto em Markdown.<br>3. Clique em serviço relacionado. | Renderização segura em HTML sanitizado, metadados de leitura e box de serviço vinculado. | Artigo em rascunho ou data futura (retorna HTTP 404 protegido). | SIM (`conteudos/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-07** | Autenticação no Django Admin | Administrador | Usuário e Senha em `/admin/login/` | 1. Acesso à URL administrativa secreta.<br>2. Inserção de credenciais.<br>3. Submissão POST. | Autenticação bem-sucedida e direcionamento ao painel de controle. | Senha incorreta (erro genérico sem revelar existência de usuário); força bruta (bloqueio 429 após 5 falhas no combo ou 10 no IP). | SIM (`nucleo/tests_rate_limit.py`) | SIM | **OPERACIONAL** |
| **FLX-08** | Atualização de Configuração Global | Administrador | Edição em `ConfiguracaoSite` | 1. Acesso ao registro Singleton pk=1.<br>2. Alteração de canais de contato ou logotipo.<br>3. Salvar. | Persistência imediata com atualização instantânea nas páginas públicas via context processor. | Tentativa de criar segundo registro (bloqueada no model e no admin). | SIM (`nucleo/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-09** | Gestão de Especialidades (CRUD) | Administrador | Formulário de Área/Serviço | 1. Edição de título, resumo ou imagem.<br>2. Ativação/desativação de visibilidade na Home.<br>3. Salvar. | Atualização imediata da grade de especialidades na Home e nas páginas internas. | Upload de imagem não suportada ou corrompida (rejeitado com ValidationError). | SIM (`servicos/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-10** | Publicação Editorial de Artigo | Administrador | Formulário de Artigo | 1. Criação de artigo como Rascunho.<br>2. Redação em Markdown.<br>3. Alteração para Publicado com data válida.<br>4. Salvar. | Artigo torna-se visível na listagem do blog e é incluído dinamicamente no `sitemap.xml`. | Script malicioso injetado (sanitizado); rascunho acidentalmente público (impossibilitado por filtros ORM). | SIM (`conteudos/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-11** | Despublicação de Artigo | Administrador | Edição de Artigo | 1. Artigo publicado tem status revertido para Rascunho.<br>2. Salvar. | Artigo deixa imediatamente de constar na listagem pública, no sitemap e retorna 404 em acesso direto. | Cache stale (inexistente em dev; invalidado por salvamento). | SIM (`scratch/audit_deep.py`) | SIM | **OPERACIONAL** |
| **FLX-12** | Triagem de Mensagens Recebidas | Administrador | Módulo `MensagemContato` | 1. Visualização da listagem de contatos.<br>2. Abertura de mensagem para leitura.<br>3. Marcação do status `lida`. | Conteúdo exibido em modo somente leitura (readonly), preservando integralidade do registro. | Tentativa de edição da mensagem ou data original (bloqueada via readonly_fields). | SIM (`contato/tests.py`) | SIM | **OPERACIONAL** |
| **FLX-13** | Expurgo Periódico de Contatos (LGPD) | Sistema / Daemon | Comando `limpar_contatos_expirados` | 1. Disparo do comando com parâmetro `--dias 30`.<br>2. Varredura de mensagens anteriores ao limite temporal. | Exclusão definitiva de registros expirados com log seguro de auditoria sem expor dados pessoais. | Execução sem parâmetro ou sem configuração (aborto defensivo seguro sem exclusão). | SIM (`nucleo/tests_regressao.py`) | SIM | **OPERACIONAL** |

---

## 3. RESUMO DA COBERTURA DOS FLUXOS

* **Fluxos Testados com 100% de Sucesso:** 13/13.
* **Fluxos com Intervenção Humana/Manual Validada:** 13/13.
* **Cobertura Automatizada em Testes de Regressão:** 100% dos fluxos possuem asserções automatizadas na suíte de testes.
* **Integridade de Estados e Dados:** Zero vazamento de dados privados, zero inconsistências entre Admin e frontend e zero falhas de rota.
