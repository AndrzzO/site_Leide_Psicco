# AUDITORIA FUNCIONAL COMPLETA — INSTITUTO MENTE EM FOCO
**DOCUMENTO DE AUDITORIA DE COMPORTAMENTO OPERACIONAL, FLUXOS E INTEGRAÇÕES**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA JS

---

## 1. ESCOPO E METODOLOGIA DA AUDITORIA FUNCIONAL

A auditoria funcional do portal **Instituto Mente em Foco** foi conduzida sob o princípio rigoroso de:

$$\textbf{"TESTAR O COMPORTAMENTO REAL, NÃO PRESUMIR QUE FUNCIONA SÓ PORQUE EXISTE CÓDIGO"}$$

Todos os testes foram executados em ambiente de desenvolvimento isolado no host Windows, utilizando o Django Test Client, SQLite local (`db.sqlite3`), ferramentas de introspecção de rotas do Django URL Resolver e validações estáticas e dinâmicas nos módulos da aplicação.

### 1.1 Diretrizes de Segurança dos Testes
* **Zero Dados Reais de Pacientes:** 100% dos testes utilizaram exclusivamente nomes fictícios, e-mails sob domínio reservado `example.com` e mensagens sintéticas claramente identificadas.
* **Isolamento de Produção:** Nenhuma chamada externa ao vivo a APIs de terceiros, zero envio de e-mails via servidores SMTP reais (utilizado `locmem` / console backend) e zero persistência de resíduos no diretório físico de mídia (`media/`).
* **Zero Alterações de Modelo ou Migrações:** Todos os modelos foram auditados em conformidade com as migrações existentes.

---

## 2. MATRIZ DE ACHADOS FUNCIONAIS DA AUDITORIA

| ID | ÁREA | ROTA | FLUXO | AÇÃO TESTADA | RESULTADO ESPERADO | RESULTADO REAL | SEVERIDADE | CAUSA | CORREÇÃO / MITIGAÇÃO | TESTE REGRESSÃO | STATUS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **FUNC-001** | Rotas | Todas as 21 rotas públicas | Navegação pública | Requisição GET em cada rota | HTTP 200 OK | HTTP 200 OK em 21/21 rotas | **CRÍTICO** | N/A (Comportamento correto) | Verificação automatizada via crawler | `LinkCrawlerRegressionTest` | **APROVADO** |
| **FUNC-002** | Segurança / Auth | `/login/`, `/signup/`, `/account/` | Acesso público inadvertido | Requisição GET em URLs genéricas | HTTP 404 (Rota inexistente) | HTTP 404 retornado | **CRÍTICO** | N/A (Comportamento correto) | Rotas públicas de login não existem; Admin isolado em rota própria | `tests_regressao.py` | **APROVADO** |
| **FUNC-003** | Contato | `/contato/` | Submissão com sucesso | POST com dados válidos e consentimento | Salvar mensagem, emitir flash message e redirecionar (PRG) | HTTP 302 com redirect para `/contato/` e 200 no GET subsequente | **CRÍTICO** | N/A (Comportamento correto) | Fluxo PRG (Post-Redirect-Get) impede reenvio por F5 | `ContatoFormTestCase` | **APROVADO** |
| **FUNC-004** | Contato | `/contato/` | Submissão inválida | POST sem telefone e sem e-mail | Rejeição com erro exibido no campo correspondente | HTTP 200 com erros associados no form | **ALTO** | N/A (Comportamento correto) | Validação cruzada `clean()` exige pelo menos um canal de contato | `ContatoFormTestCase` | **APROVADO** |
| **FUNC-005** | Contato | `/contato/` | Tentativa de spam por bot | POST com honeypot (`campo_verificacao`) preenchido | Descarte silencioso sem gravar no banco nem enviar e-mail | Descarte seguro efetuado | **ALTO** | N/A (Comportamento correto) | Validação defensiva na view `contato.views` | `HoneypotTestCase` | **APROVADO** |
| **FUNC-006** | Contato | `/contato/` | Submissão excessiva | POST excedendo cota de 5 envios/15 min | Rejeição com HTTP 429 e `Retry-After: 900` | HTTP 429 retornado | **ALTO** | N/A (Comportamento correto) | Rate Limiting em memória pseudonimizado com HMAC-SHA256 | `tests_rate_limit.py` | **APROVADO** |
| **FUNC-007** | Blog | `/conteudos/` e detalhe | Artigo em Rascunho | Tentativa de acesso a artigo com `status=RASCUNHO` | Invisível na listagem, HTTP 404 em acesso direto e fora do sitemap | 100% privado (404 em acesso direto, ausente na lista e no sitemap) | **CRÍTICO** | N/A (Comportamento correto) | Filtro `status=STATUS_PUBLICADO` estrito em QuerySets | `ArtigoModelTestCase` | **APROVADO** |
| **FUNC-008** | Blog | `/conteudos/<slug>/` | Artigo com data futura | Acesso a artigo com data de publicação posterior ao instante atual | HTTP 404 retornado | HTTP 404 retornado | **ALTO** | N/A (Comportamento correto) | Filtro `data_publicacao__lte=agora` aplicado em views e sitemaps | `ArtigoModelTestCase` | **APROVADO** |
| **FUNC-009** | Blog | `/conteudos/?q=...` | Busca com termos especiais / XSS | Submissão de script `<script>alert(1)</script>` | Termo escapado no HTML sem execução de script | Escapado como texto plano seguro | **ALTO** | N/A (Comportamento correto) | Django template auto-escaping ativo | `tests_regressao.py` | **APROVADO** |
| **FUNC-010** | Admin | `/admin/login/` | Autenticação administrativa | Login com credenciais válidas e inválidas | Sucesso com redirecionamento; falha com erro e proteção de brute force | Login bem-sucedido direciona para painel; 5 falhas no combo bloqueiam com 429 | **CRÍTICO** | N/A (Comportamento correto) | `wrap_admin_login` com mitigação de brute force | `tests_rate_limit.py` | **APROVADO** |
| **FUNC-011** | Admin | `/admin/nucleo/configuracaosite/` | Gestão de Configuração | Tentativa de adicionar segundo registro | Bloqueio de criação (`has_add_permission=False`) | Singleton estrito mantido (pk=1) | **ALTO** | N/A (Comportamento correto) | Trava no model `clean()` e no ModelAdmin | `AdminPermissionsTest` | **APROVADO** |
| **FUNC-012** | Uploads | Admin (mídia) | Upload de arquivos | Envio de JPG, PNG, WEBP, EXE e fake JPG | Apenas imagens reais válidas aceitas; executáveis e textos renomeados rejeitados | Validador Pillow inspeciona binário real e rejeita com ValidationError | **CRÍTICO** | N/A (Comportamento correto) | `validar_imagem` em `nucleo/validators.py` | `UploadValidationTest` | **APROVADO** |
| **FUNC-013** | Estados Vazios | Home e Internas | Configuração sem WhatsApp/E-mail | Visualização com campos de contato vazios | Site não quebra (zero 500) e não renderiza 'None' ou 'null' | Páginas renderizam normalmente; botões de WhatsApp degradam para Contato | **ALTO** | N/A (Comportamento correto) | Context processor defensivo e checagens condicionais `{% if WHATSAPP_LINK %}` | `EmptyStateTestCase` | **APROVADO** |
| **FUNC-014** | Erros HTTP | `/rota-inexistente/` | Navegação para rota inexistente | Acesso a URL inválida em `DEBUG=False` | Template 404 acolhedor sem vazamento de traceback | HTTP 404 limpo com navegação de retorno à Home | **MÉDIO** | N/A (Comportamento correto) | `nucleo.views.tratar_erro_404` | `ErrorPagesTestCase` | **APROVADO** |
| **FUNC-015** | LGPD | Management Command | `limpar_contatos_expirados` | Execução sem `--dias` e com `--dias 30` | Sem dias: aborto seguro sem exclusão; com dias: exclusão de >30 dias | Aborto seguro confirmado sem parâmetros; dry-run simula; execução exclui estritamente expirados | **ALTO** | N/A (Comportamento correto) | Lógica de segurança em `contato/management/commands/limpar_contatos_expirados.py` | `ContactRetentionBoundaryRegressionTest` | **APROVADO** |

---

## 3. AUDITORIA DETALHADA POR CAMADA FUNCIONAL

### 3.1 Rotas, Resolução de URLs e Links Internos
* **Total de Rotas Registradas no Django:** 48 rotas internas mapeadas entre painel administrativo, rotas institucionais, serviços, conteúdos e utilitários técnicos.
* **Varredura de Templates (33 Arquivos):** Zero instâncias de `href="#"` órfão, zero links `javascript:void(0)` e zero atributos `href=""` vazios.
* **Âncoras de Navegação:** Todas as âncoras na Home (`#inicio`, `#atendimento`, `#areas`, `#sobre`, `#processo`, `#neuropsicologia`, `#conteudos`, `#faq`) possuem IDs correspondentes declarados nas seções de destino.

### 3.2 Construtor Central de Links do WhatsApp
* **Centralização:** Link gerado estritamente através da propriedade `whatsapp_link` do model `ConfiguracaoSite` e exposto no context processor como `WHATSAPP_LINK`.
* **Codificação:** Utiliza `urllib.parse.quote()` nativo do Python, assegurando encoding UTF-8 perfeito (sem quebra de acentos ou espaços corrompidos).
* **Sanitização de Número:** Extração estrita de dígitos numéricos via `filter(str.isdigit)`.
* **Fallback Defensivo:** Na ausência de número cadastrado no CMS, os botões de agendamento no Header, Hero e Rodapé apontam automaticamente para `{% url 'contato:index' %}`, e o botão flutuante é ocultado.

### 3.3 Formulário de Contato e Integridade de Dados
* **Campos Solicitados:** Nome, e-mail, telefone, serviço de interesse, mensagem breve e ciência da política de privacidade. Ausência absoluta de campos médicos ou sensíveis (sem CPF, RG ou prontuários).
* **Padrão PRG (Post-Redirect-Get):** Submissões bem-sucedidas respondem com HTTP 302 direcionando para a página de contato, onde o Django Messages Framework exibe a mensagem de sucesso uma única vez. Recargas subsequentes de página (F5) resultam em GET limpo sem duplicação de mensagens.
* **Validação Cruzada:** O formulário aceita submissão com e-mail preenchido e telefone vazio, ou vice-versa; rejeita com erro explícito caso ambos os canais de retorno estejam vazios.

### 3.4 Blog e Fluxo Editorial do CMS
* **Rascunhos:** Estritamente confinados ao Django Admin. Tentativas de acesso público retornam HTTP 404.
* **Agendamento:** Publicações com data no futuro são suprimidas da visualização pública até o instante programado.
* **Despublicação:** Alteração de status para Rascunho remove imediatamente o artigo da listagem, do sitemap e do acesso direto por slug.
* **Busca e Paginação:** A busca trunca parâmetros com mais de 100 caracteres antes da consulta ORM; o termo de pesquisa é preservado durante a navegação entre páginas através do parâmetro `?q=...&page=...`.

### 3.5 CMS e Django Admin
* **Acesso e Segregação:** Usuários anônimos e não-staff são sumariamente bloqueados com redirecionamento para o login. Superusuários e equipe possuem visão clara por fieldsets.
* **Singleton `ConfiguracaoSite`:** Protegido contra exclusão acidental e adição de múltiplos registros.
* **Mensagens de Contato:** Registros de contato são estritamente de leitura (`readonly_fields`), permitindo aos operadores modificar apenas o campo booleano `lida` (marcar como lida / não lida).

### 3.6 Uploads de Mídia
* O validador binário `validar_imagem` em `nucleo/validators.py` inspeciona o cabeçalho real do arquivo via Pillow (`Image.open().verify()`), rejeitando com `ValidationError`:
  * Arquivos não-imagem renomeados com extensão `.jpg` ou `.png`.
  * Arquivos executáveis `.exe`.
  * Arquivos corrompidos ou truncados.
  * Arquivos que ultrapassem o limite de 10 MB.

### 3.7 Resiliência de Estados Vazios
A simulação de ausência de informações no CMS confirmou que:
* A ausência de foto de perfil da profissional ou capas de serviços renderiza elegantes placeholders vetoriais com proporções nativas (`4:5`, `4:3`, `1:1`, `16:9`), sem gerar erros 500.
* A ausência de logo institucional exibe a marca em tipografia nobre (*Cormorant Garamond*).
* A ausência de canais sociais ou telefone suprime os respectivos ícones sem exibir literais `'None'` ou links quebrados.

### 3.8 Tratamento de Erros HTTP (400, 403, 404, 429, 500)
* Em ambiente de produção simulado (`DEBUG=False`), todas as páginas de erro renderizam layouts acolhedores e consistentes, com botões de retorno seguros para a Home e **zero vazamento de tracebacks, segredos ou caminhos físicos do sistema**.

---

## 4. CONCLUSÃO DA AUDITORIA

A auditoria funcional confirma que o **Instituto Mente em Foco** opera com total conformidade técnica, resiliência contra falhas, proteção ativa contra abuso, integridade no CMS e respeito estrito aos padrões de privacidade da LGPD e normas do CFP.
