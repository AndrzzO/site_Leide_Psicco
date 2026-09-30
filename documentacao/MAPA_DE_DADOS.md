# MAPA DE DADOS PESSOAIS — INSTITUTO MENTE EM FOCO
**DOCUMENTO DE GOVERNANÇA, MAPEAMENTO DE FLUXOS E AUDITORIA DE PRIVACIDADE (LGPD)**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **ESTADO:** AUDITADO / REAL

---

## 1. DIRETRIZES FUNDAMENTAIS DA AUDITORIA

Este documento registra o **estado real e auditado** dos fluxos de dados pessoais tratados na plataforma digital do **Instituto Mente em Foco**. 

> [!IMPORTANT]
> **LIMITAÇÃO JURÍDICA E METODOLOGIA:**
> O mapeamento técnico reflete com exatidão o código-fonte, a modelagem de dados e as dependências operacionais em funcionamento. Nenhuma conformidade fictícia, base legal arbitrária ou prazo de retenção não deliberado pela instituição é inventado neste documento. Questões pendentes de validação formal por advogado ou pela responsável técnica são explicitamente registradas como **PENDENTES DE DEFINIÇÃO**.

---

## 2. INVENTÁRIO DETALHADO DOS FLUXOS DE DADOS

---

### FLUXO 01 — FORMULÁRIO DE CONTATO INSTITUCIONAL

* **Nome do Fluxo:** Recepção e Triagem de Mensagens Institucionais via Formulário Web.
* **Dados Tratados:**
  * `nome` (Nome completo fornecido pelo visitante — Texto, máx. 150 caracteres);
  * `email` (Endereço eletrônico — Formato de e-mail, opcional se telefone fornecido);
  * `telefone` (Telefone com DDD / WhatsApp — Texto normalizado, mín. 10 dígitos, opcional se e-mail fornecido);
  * `servico_interesse` (Chave estrangeira opcional vinculada ao catálogo público de serviços);
  * `mensagem` (Texto livre breve — Texto puro limitado a 2.000 caracteres);
  * `aceite_privacidade` (Confirmação booleana de leitura e concordância com a Política de Privacidade);
  * `criado_em` (Carimbo de data e hora gerado automaticamente pelo servidor no momento da gravação);
  * `lida` (Booleano de controle interno de triagem pela equipe, padrão `False`).
* **Origem dos Dados:** Informados voluntária e diretamente pelo visitante no formulário da rota `/contato/`.
* **Finalidade Técnica:**
  * Permitir que o visitante solicite informações gerais sobre atendimentos psicológicos, avaliações neuropsicológicas ou tire dúvidas;
  * Viabilizar o retorno do contato pela profissional Mari Menezes ou sua equipe administrativa por e-mail ou WhatsApp.
* **Armazenamento:**
  * Tabela `contato_mensagemcontato` no banco de dados relacional da aplicação (SQLite em desenvolvimento; PostgreSQL gerenciado em produção).
* **Acesso:**
  * Acesso restrito a usuários autenticados no Django Admin pertencentes à equipe com permissão expressa `contato.view_mensagemcontato`.
  * Visualização dos dados em modo somente-leitura (`readonly_fields`).
* **Compartilhamento / Terceiros:**
  * Provedor de infraestrutura/hospedagem que opera o banco de dados da aplicação (`PENDENTE_DEFINICAO`);
  * Provedor de serviço de envio de e-mails (SMTP) para despacho da notificação interna à clínica (`PENDENTE_DEFINICAO` em produção; console local em desenvolvimento).
* **Retenção Atual:**
  * Indeterminada no código até a definição da política institucional. Os registros permanecem no banco de dados até exclusão manual pelo Django Admin.
* **Retenção Definida?:**
  * **NÃO** (`PENDENTE_DEFINICAO`). Foi implementado mecanismo técnico configurável (`CONTATO_RETENCAO_DIAS`), que permanece inativo por padrão para não excluir dados arbitrariamente antes de aprovação formal.
* **Base Legal Definida?:**
  * **PENDENTE DE REVISÃO JURÍDICA**. (Possíveis enquadramentos pelo art. 7º da LGPD a validar: Consentimento — inc. I; Procedimentos preliminares relacionados a contrato a pedido do titular — inc. V; ou Legítimo Interesse — inc. IX).
* **Pendências Relacionadas:**
  * Aprovação formal do prazo de retenção e descarte de mensagens arquivadas;
  * Homologação jurídica da base legal específica;
  * Definição do provedor de e-mail transacional corporativo.

---

### FLUXO 02 — DIRECIONAMENTO PARA WHATSAPP COMERCIAL

* **Nome do Fluxo:** Abertura de Conversa Direta via Link Oficial do WhatsApp.
* **Dados Tratados:**
  * Nenhum dado pessoal do visitante é coletado, processado ou gravado pelo servidor do Instituto.
  * O servidor apenas constrói uma URL estática parametrizada com o número de WhatsApp cadastrado no CMS (`ConfiguracaoSite.whatsapp_numero`) e uma mensagem padrão institucional (*"Olá, Mari. Conheci o Instituto Mente em Foco pelo site e gostaria de informações sobre o atendimento psicológico/neuropsicológico."*).
* **Origem dos Dados:** Clique voluntário e explícito do visitante no botão flutuante ou nos botões de chamada (CTAs).
* **Finalidade Técnica:** Redirecionar o visitante para a plataforma externa do WhatsApp/Meta, onde a conversa ocorre em canal criptografado de ponta a ponta gerido pela referida empresa.
* **Armazenamento:** Nenhum no site do Instituto.
* **Acesso:** Apenas os interlocutores no aplicativo WhatsApp.
* **Compartilhamento / Terceiros:** Meta Platforms Inc. / WhatsApp LLC.
* **Retenção Atual:** Não aplicável ao servidor web.
* **Retenção Definida?:** Não aplicável ao servidor web.
* **Base Legal Definida?:** Ação iniciada direta e exclusivamente pelo titular.
* **Pendências Relacionadas:** Nenhuma no código web.

---

### FLUXO 03 — AUTENTICAÇÃO E GESTÃO ADMINISTRATIVA (DJANGO ADMIN)

* **Nome do Fluxo:** Gestão de Credenciais de Operadores do Painel Administrativo.
* **Dados Tratados:**
  * `username` (Identificador de usuário administrativo);
  * `password` (Hash criptográfico da senha via PBKDF2/SHA256, sem acesso ao texto plano);
  * `email` (E-mail corporativo do operador);
  * `is_staff` / `is_superuser` / permissões de grupo;
  * `last_login` e `date_joined`.
* **Origem dos Dados:** Cadastrados internamente via comando de console (`createsuperuser`) ou pelo administrador geral.
* **Finalidade Técnica:** Controle de acesso, autenticação e autorização para edição de conteúdos, artigos, fotos e visualização de contatos.
* **Armazenamento:** Tabelas nativas do Django (`auth_user`, `auth_group`, `auth_permission`) no banco de dados relacional.
* **Acesso:** Restrito ao titular da conta administrativa e ao administrador de infraestrutura.
* **Compartilhamento / Terceiros:** Apenas infraestrutura de hospedagem do banco de dados.
* **Retenção Atual:** Permanente enquanto o operador mantiver vínculo administrativo com a clínica.
* **Retenção Definida?:** SIM (vinculada à gestão operacional interna).
* **Base Legal Definida?:** Execução de contrato / legítimo interesse da segurança da informação.
* **Pendências Relacionadas:** Nenhuma pendência técnica.

---

### FLUXO 04 — SESSÕES E COOKIES ESSENCIAIS DE SEGURANÇA

* **Nome do Fluxo:** Controle de Segurança CSRF e Sessões Técnicas.
* **Dados Tratados:**
  * Token pseudoaleatório criptográfico de proteção contra requisições forjadas (`csrftoken`);
  * Identificador de sessão de operadores autenticados no Admin (`sessionid`);
  * Mensagens temporárias de feedback pós-submissão (`messages`).
* **Origem dos Dados:** Gerados automaticamente pelos middlewares nativos do Django (`CsrfViewMiddleware`, `SessionMiddleware`, `MessageMiddleware`).
* **Finalidade Técnica:**
  * Prevenção de ataques de CSRF (Cross-Site Request Forgery) em envios POST;
  * Manutenção do estado de login seguro de operadores;
  * Entrega de avisos de sucesso/erro sem reenvio ao atualizar a página (PRG).
* **Armazenamento:**
  * No navegador do usuário (cookies first-party estritamente necessários);
  * Chaves de sessão no banco de dados (`django_session`) apenas para usuários com sessão ativa.
* **Acesso:** Middleware do Django e navegador do visitante.
* **Compartilhamento / Terceiros:** Nenhum. Dados estritamente internos e de primeira parte.
* **Retenção Atual:**
  * `csrftoken`: 1 ano (padrão de segurança do Django);
  * `sessionid`: 2 semanas para sessões ativas;
  * `messages`: efêmero, destruído após a renderização da mensagem no navegador.
* **Retenção Definida?:** SIM (definida pelos padrões do framework).
* **Base Legal Definida?:** Legítimo interesse / Obrigação legal e técnica de segurança da informação.
* **Pendências Relacionadas:** Nenhuma.

---

### FLUXO 05 — CONTROLE DE FREQUÊNCIA E PROTEÇÃO CONTRA ABUSO (RATE LIMITING)

* **Nome do Fluxo:** Prevenção de Abuso, Força Bruta e Sobrecarga de Requisições (Contato e Login Admin).
* **Dados Tratados:**
  * Digest criptográfico unidirecional HMAC-SHA256 gerado a partir da chave secreta da aplicação (`SECRET_KEY`) e do identificador de origem (`security:rl:v1:{escopo}:{tipo}:{digest}`);
  * Contadores numéricos voláteis de tentativas e chaves temporárias de bloqueio transitório.
* **Origem dos Dados:** Cabeçalho de rede do socket (`REMOTE_ADDR`, ou `HTTP_X_FORWARDED_FOR` exclusivamente se `TRUST_PROXY_CLIENT_IP = True`).
* **Finalidade Técnica:** Mitigação de força bruta no login administrativo, spam no formulário de contato e prevenção de DoS lógico de processamento/banco.
* **Armazenamento:**
  * Memória volátil do servidor via Django Cache (`LocMemCache` em desenvolvimento; cache compartilhado em produção multi-worker).
  * **O endereço IP em texto puro e os nomes de usuário NUNCA são gravados nas chaves de cache, no banco de dados ou em arquivos de log.**
* **Acesso:** Camada de serviço de segurança `nucleo.rate_limit` invocada nas views protegidas.
* **Compartilhamento / Terceiros:** Nenhum.
* **Retenção Atual:** Exclusão automática da chave após 900 segundos (15 minutos) via TTL nativo do cache.
* **Retenção Definida?:** SIM (15 minutos via TTL de expiração).
* **Base Legal Definida?:** Legítimo interesse e segurança da aplicação (art. 7º, IX da LGPD e Marco Civil da Internet).
* **Pendências Relacionadas:** Nenhuma no código; validação da infraestrutura de cache em produção.

---

## 3. DADOS DELIBERADAMENTE NÃO COLETADOS OU EVITADOS

A auditoria confirma que a plataforma **NÃO coleta, não armazena e não processa**:
1. **Dados de Identificação Civil:** CPF, RG, CNH, Título de Eleitor, Certidões.
2. **Dados Pessoais Sensíveis:**
   * Diagnósticos médicos ou psicológicos;
   * Sintomas clínicos ou queixas detalhadas de transtornos;
   * Prescrições medicamentosas ou laudos periciais;
   * Histórico de consultas anteriores;
   * Prontuário ou registros de evolução terapêutica;
   * Dados biométricos ou genéticos;
   * Origem racial ou étnica, convicção religiosa, opinião política ou filiação partidária/sindical;
   * Dados relativos à vida sexual ou orientação sexual.
3. **Dados de Telemetria e Rastreamento Invasivo:**
   * Endereço IP persistido em banco de dados;
   * User-Agent persistido em banco de dados;
   * Histórico de navegação externa ou referrers cruzados;
   * Identificadores de publicidade (IDFA, GAID).
4. **Documentos e Anexos:** Nenhum formulário público aceita upload de arquivos (PDF, DOCX, imagens).
5. **Dados de Pagamento:** Nenhum dado bancário, cartão de crédito ou conta financeira.
6. **Dados de Terceiros e Crianças/Adolescentes:** Não são solicitados dados de terceiros ou formulários de menores de idade sem representação formal prévia em consultório.

---

## 4. MATRIZ DE PENDÊNCIAS JURÍDICAS E OPERACIONAIS

| Item | Descrição da Pendência | Impacto | Ação Necessária |
|---|---|---|---|
| **Base Legal Formais** | Definição formal das hipóteses legais da LGPD para contato e arquivos de consulta | Médio | Validação por assessoria jurídica especializada |
| **Prazo de Retenção** | Estabelecer formalmente a política de retenção temporal de mensagens no site | Médio | Deliberação institucional (ex: 90 dias, 180 dias, 1 ano) |
| **Canal de Privacidade** | Definição de e-mail institucional oficial para atendimento aos direitos dos titulares | Médio | Criação de canal de comunicação ou indicação do e-mail da clínica |
| **Encarregado (DPO)** | Definição sobre necessidade ou dispensa de nomeação de Encarregado pelo porte da entidade | Baixo/Médio | Avaliação das resoluções da ANPD para agentes de tratamento de pequeno porte |
| **Provedores de Produção** | Definição contratual dos fornecedores de hospedagem e e-mail transacional | Médio | Seleção de parceiros com termos de adequação à LGPD |

---
*Mapeamento concluído em conformidade com o princípio da transparência e da minimização de dados da LGPD.*
