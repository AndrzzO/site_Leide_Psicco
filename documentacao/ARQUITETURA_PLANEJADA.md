# ARQUITETURA PLANEJADA — INSTITUTO MENTE EM FOCO
**DOCUMENTO DE ARQUITETURA DE SOFTWARE E PADRÕES TÉCNICOS DJANGO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **STACK:** DJANGO 6.0+

---

## 1. DIRETRIZES ARQUITETURAIS GERAIS

O projeto do **Instituto Mente em Foco** adota o princípio de **Simplicidade Técnica, Robustez e Alta Manutenibilidade** (*KISS - Keep It Simple, Sensible*).

### 1.1 Premissas Estruturais
* **Server-Rendered Tradicional (SSR):** Processamento integral pelo motor do Django (Django Templates + Class-Based Views ou Function-Based Views organizadas).
* **Ausência de Overengineering:** Não utilizar frameworks SPA (React, Vue, Angular), não criar APIs REST complexas sem necessidade real, não fragmentar o sistema em microserviços ou microssistemas distribuídos.
* **Frontend Nativo:** HTML5 semântico, CSS moderno estruturado em Design Tokens (CSS Variables) com metodologia BEM ou utilitária limpa, e JavaScript vanilla enxuto exclusivo para interações essenciais (menu mobile, accordion do FAQ, máscaras de formulário, toasts de feedback).
* **CMS Nativo:** Utilização do Django Admin customizado de forma elegante para gerenciar artigos, serviços, configurações institucionais e mensagens recebidas.

---

## 2. MODULARIZAÇÃO DE APLICAÇÕES DJANGO (APPS)

Para evitar dispersão e acoplamento, o sistema é organizado em **5 aplicações coesas**, cada qual com escopo e fronteira bem delimitados:

```
instituto_mente_em_foco/
├── config/                  # Núcleo de configurações do projeto Django
├── nucleo/                  # Utilitários globais, context processors, tags, páginas de erro
├── paginas/                 # Páginas estáticas/institucionais (Home, Sobre, Políticas)
├── servicos/                # Catálogo e detalhamento das áreas de atuação e avaliações
├── conteudos/               # Blog institucional, artigos, categorias e autores
└── contato/                 # Formulário de contato seguro, captação e link WhatsApp
```

### 2.1 Detalhamento dos Apps e Responsabilidades

#### A. `config` (Projeto Global)
* `settings.py`: Configurações centralizadas alimentadas por variáveis de ambiente (`.env`).
* `urls.py`: Roteador principal com inclusão limpa das rotas de cada app e rotas para sitemap e robots.
* `wsgi.py` / `asgi.py`: Pontos de entrada para deploy de produção.

#### B. `nucleo` (Base e Compartilhados)
* **Responsabilidade:** Recursos transversais que atendem todo o ecossistema do site.
* **Modelos:** `ConfiguracaoSite` (Singleton ou registro único para telefone, WhatsApp, e-mail institucional, Instagram, CRP, status de agendamento e scripts de SEO).
* **Context Processors:** Disponibilização automática dos dados institucionais e do link do WhatsApp para todos os templates sem duplicação de queries.
* **Handlers de Erro:** Views customizadas para respostas HTTP 400, 403, 404 e 500, com design acolhedor e navegação de retorno.
* **Template Tags & Filters:** Filtros para formatação amigável de datas, sanitização e utilitários visuais.

#### C. `paginas` (Apresentação Institucional)
* **Responsabilidade:** Renderização das páginas estáticas e da página inicial (Home).
* **Views:**
  * `HomeView`: Reúne seções do Hero, momentos da vida, identificação da demanda, cards de serviços, apresentação de Mari Menezes, prévia de conteúdos e FAQ.
  * `SobreView`: Apresentação aprofundada da profissional Mari Menezes, abordagem clínica, método e posicionamento ético.
  * `PrivacidadeView` & `TermosView`: Textos legais de conformidade com a LGPD e termos de uso.

#### D. `servicos` (Áreas de Atuação e Especialidades)
* **Responsabilidade:** Gestão e exibição das áreas de atuação clínica e avaliativa.
* **Modelos Previstos:**
  * `AreaAtuacao`: Título, slug, subtítulo/resumo, descrição detalhada, ícone identificador, imagem de capa/card, ordem de exibição, ativo (`bool`).
* **Páginas Mapeadas:**
  * `/psicologia/`
  * `/neuropsicologia/`
  * `/traumas/`
  * `/separacao-e-recomecos/`
  * `/avaliacao/` (abrangendo Avaliação Psicológica e Neuropsicológica)
  * `/reabilitacao-neurocognitiva/`

#### E. `conteudos` (Blog e Educação em Saúde)
* **Responsabilidade:** Publicação de artigos reflexivos, didáticos e informativos.
* **Modelos Previstos:**
  * `CategoriaArtigo`: Nome, slug, descrição.
  * `Artigo`: Título, slug, resumo (`meta_description`), conteúdo formatado, imagem de capa com texto alternativo, autor, categoria, data de publicação, atualizado em, status (`rascunho`/`publicado`), tempo de leitura estimado.
* **Views e Rotas:**
  * `/conteudos/` (Listagem paginada com filtro por categoria).
  * `/conteudos/<slug>/` (Página de leitura do artigo com bloco de compartilhamento ético e artigos relacionados).

#### F. `contato` (Canais de Atendimento e Formulário)
* **Responsabilidade:** Recepção de mensagens de visitantes e redirecionamento para o canal oficial do WhatsApp.
* **Modelos Previstos:**
  * `MensagemContato`: Nome, WhatsApp/telefone, e-mail, assunto/tipo de atendimento, mensagem, data de envio, consentimento de privacidade (`bool`), lido (`bool`).
* **Segurança do Formulário:**
  * Proteção CSRF obrigatória.
  * Honeypot invisível para bloqueio de spambots automatizados.
  * Rate limiting básico para evitar sobrecarga de requisições.
  * Disparo de e-mail de notificação para a profissional (via SMTP seguro configurado por variáveis de ambiente).

---

## 3. ESTRUTURA DE DIRETÓRIOS DO PROJETO

```
SiteDjangoLeide/
├── documentacao/            # Memória técnica persistente do projeto
│   ├── CONTEXTO_MESTRE.md
│   ├── ARQUITETURA_PLANEJADA.md
│   ├── MAPA_DE_PAGINAS.md
│   ├── INVENTARIO_DE_IMAGENS.md
│   ├── CHECKLIST_DE_QUALIDADE.md
│   └── PENDENCIAS_DO_CLIENTE.md
├── manage.py
├── .env.example             # Modelo das variáveis de ambiente
├── .gitignore               # Exclusões de ambiente virtual, banco local e mídias
├── requirements.txt         # Dependências mínimas e pinadas
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                    # Agrupamento opcional ou raiz para os apps
│   ├── nucleo/
│   ├── paginas/
│   ├── servicos/
│   ├── conteudos/
│   └── contato/
├── templates/               # Templates globais organizados por herança
│   ├── base.html            # Layout principal (Header, Footer, Metas, Tokens)
│   ├── nucleo/
│   │   ├── includes/
│   │   │   ├── header.html
│   │   │   ├── footer.html
│   │   │   ├── whatsapp_fab.html
│   │   │   └── banner_cta.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   └── 500.html
│   ├── paginas/
│   │   ├── home.html
│   │   ├── sobre.html
│   │   └── privacidade.html
│   ├── servicos/
│   │   ├── lista.html
│   │   └── detalhe.html
│   ├── conteudos/
│   │   ├── lista.html
│   │   └── detalhe.html
│   └── contato/
│       └── form.html
├── static/                  # Arquivos estáticos de desenvolvimento
│   ├── css/
│   │   ├── tokens.css       # Variáveis de cores, tipografia, espaçamentos
│   │   ├── reset.css        # Normalização consistente
│   │   ├── base.css         # Estilos globais e componentes estruturais
│   │   ├── layout.css       # Header, Hero, Footer, Grids
│   │   └── pages/           # Estilos pontuais por seção (home.css, etc.)
│   ├── js/
│   │   ├── main.js          # Menu móvel, acessibilidade, microinterações
│   │   └── contato.js       # Validação e máscara simples de telefone
│   ├── img/
│   │   ├── brand/           # Logos, favicon, marcas d'água
│   │   ├── icons/           # SVGs minimalistas inline ou em sprite
│   │   └── placeholders/    # Imagens temporárias com proporções exatas
└── media/                   # Diretório de uploads (fotos de artigos, capas)
```

---

## 4. GESTÃO DE DADOS E BANCO DE DADOS

* **Desenvolvimento Local:** Uso transparente do `sqlite3` para agilidade, portabilidade e simplicidade de setup.
* **Aderência Padrão Django ORM:** Não utilizar construções SQL puras, triggers específicas de motor ou extensões proprietárias que impeçam a transição.
* **Preparação para Produção:** O projeto utiliza abstração padrão do Django, permitindo conexão imediata com `PostgreSQL` através de `dj-database-url` ou configuração padrão de ambiente, sem alterações nas regras de negócio.
* **Migrations:** Todas as alterações no modelo de dados devem ser gerenciadas via `makemigrations` e versionadas no repositório.

---

## 5. SEGURANÇA E CONFORMIDADE (LGPD)

### 5.1 Proteção do Ambiente
* Nenhuma chave sensível (`SECRET_KEY`, credenciais de banco, credenciais SMTP) poderá ser gravada no código-fonte.
* Utilização de biblioteca de configuração leve (`python-decouple` ou similar com suporte a `.env`).
* Em produção: `DEBUG = False`, `ALLOWED_HOSTS` estrito, ativação de `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `X_FRAME_OPTIONS = 'DENY'` e cabeçalhos de segurança contra MIME-sniffing.

### 5.2 Validação e Sanitização
* Validação de campos de formulário estritamente no lado servidor (Django Forms), com validação frontend servindo apenas como suporte de usabilidade.
* Upload de imagens com validação rigorosa de extensão, tamanho máximo e verificação de tipo MIME.
* Dados coletados minimizados: consentimento expresso de privacidade antes do envio do formulário de contato.

---

## 6. FLUXO DE REQUISIÇÃO (REQUEST/RESPONSE LIFECYCLE)

```
[Visitante / Navegador]
          │ (Requisição HTTP)
          ▼
   [Web Server / WSGI]
          │
          ▼
   [Django Middlewares] (Segurança, Sessão, CSRF)
          │
          ▼
   [URL Router (urls.py)]
          │
          ▼
   [View Específica] ───► [Model / ORM / Cache]
          │
          ▼
   [Template Engine] ◄─── [Context Processors (nucleo)]
          │
          ▼
   [HTML Renderizado com Design Tokens e Assets Estáticos]
          │
          ▼
[Navegador do Usuário: Resposta Rápida, Semântica e Acessível]
```

---

## 7. ESTADO APÓS PROMPT 01

A fundação técnica do projeto foi integralmente implementada conforme o planejamento, com a seguinte estrutura física e lógica:

1. **Configurações Centralizadas e Ambientes:**
   - Pacote `configuracoes` estruturado com subpasta `settings/` contendo `base.py`, `desenvolvimento.py` e `producao.py`.
   - Gestão de variáveis de ambiente com `python-decouple`, modelo `.env.example` e `.env` local seguro.
   - Suporte a `DATABASE_URL` via `dj-database-url` (SQLite local em dev, PostgreSQL configurado para produção).
2. **Apps Fundamentais Criados:**
   - `nucleo`: Contém `context_processors.py` (injeção dos dados da marca e link dinâmico do WhatsApp), views de erro 400, 403, 404 e 500, e endpoint `/health/`.
   - `paginas`: Contém a view temporária da raiz `/` (`inicio_temporario.html`).
   - `servicos`, `conteudos`, `contato`: Criados com `apps.py`, `models.py`, `admin.py`, `views.py` e `urls.py` preparados para os módulos futuros.
3. **Templates e Estilos Base:**
   - `templates/base/base.html` com marcação semântica, skip link para acessibilidade, meta tags e blocos modulares.
   - `templates/paginas/inicio_temporario.html` renderizando identidade institucional, assinaturas e status.
   - `templates/erros/` com templates dedicados para 400, 403, 404 e 500.
   - `static/css/tokens.css` com a paleta oficial (`--cor-areia`, `--cor-off-white`, `--cor-salvia`, `--cor-oliva`, `--cor-dourado`, `--cor-taupe`) e tokens estruturais.
   - `static/css/base.css` com reset moderno, acessibilidade e foco visível.
   - `static/js/base.js` em vanilla JS para suporte a acessibilidade e navegação por teclado.
4. **Verificações e Validações:**
   - `python manage.py check`: 0 erros encontrados.
   - `python manage.py test`: 7 testes unitários executados com 100% de sucesso.
   - `python manage.py collectstatic --dry-run`: 133 arquivos mapeados corretamente.
   - Rota `/` respondendo com HTTP 200 e conteúdo institucional verificado.

---

## 8. ESTADO APÓS PROMPT 02

A camada de modelagem essencial, CMS e persistência institucional foi implementada com êxito:

1. **Models Criados e Ativos:**
   - `ConfiguracaoSite` (`nucleo.models`): Singleton global para nome da instituição, frases, CTAs, contatos, telefones, WhatsApp, logos, favicon e Open Graph. Protegido contra exclusão acidental e duplicação no Admin.
   - `Profissional` (`nucleo.models`): Cadastro de Mari Menezes com biografia real, frases aprovadas, fotos editoriais (`foto_principal`, `foto_sobre`, `foto_secundaria`) e campos para registro no CRP e qualificações oficiais.
   - `RedeSocial` (`nucleo.models`): Canais oficiais com ícones controlados, URLs seguras e ordenação.
   - `AreaAtuacao` (`servicos.models`): Pilares institucionais da Home (Psicologia, Neuropsicologia, Traumas, Separação e Recomeços, Novos Relacionamentos) com imagens e resumos.
   - `Servico` (`servicos.models`): Detalhamento dos serviços clínicos e avaliações com FK para `AreaAtuacao`, ícones, descrições e suporte para SEO (`meta_titulo`, `meta_descricao`).
2. **Segurança e Validação de Uploads:**
   - Módulo `nucleo.validators` com limite de 10 MB e validação binária de formato e integridade via Pillow (`JPEG`, `PNG`, `WEBP`, `ICO`).
   - Módulo `nucleo.upload_paths` organizando uploads em subpastas seguras (`institucional/`, `profissionais/`, `areas/`, `servicos/`) com prevenção de Directory Traversal e colisão.
3. **Django Admin Configurado como CMS:**
   - Fieldsets organizados por blocos temáticos para usuários não-técnicos.
   - Pré-visualização segura de logotipos e fotografias diretamente na listagem e edição.
4. **Carga Inicial Idempotente:**
   - Comando `python manage.py popular_dados_iniciais` populando dados reais aprovados sem duplicatas.
5. **Resiliência do Context Processor:**
   - `dados_institucionais` atualizado para extrair dados da `ConfiguracaoSite` ativa com fallbacks automáticos.
6. **Bateria de Testes:**
   - 22 testes automatizados executados e aprovados com 100% de sucesso.

---

## 9. ESTADO APÓS PROMPT 09 (BLOG E CONTEÚDOS EDUCATIVOS)

O módulo de conteúdos educativos foi estruturado com foco em autoridade ética e segurança:
1. **Modelos:** `CategoriaArtigo` e `Artigo` (`conteudos/models.py`), com suporte a ciclo de vida (`rascunho`, `publicado`), publicação agendada, ordenação e destaque.
2. **Sanitização e Segurança:** Módulo `conteudos/sanitizacao.py` utilizando `markdown` e `bleach` com allowlist estrita de tags e atributos, proteção anti-XSS e bloqueio de `<h1>` inline para preservar integridade hierárquica do SEO.
3. **Views e Listagens:** Suporte a paginação limpa (9 itens/página), busca com termo `?q=`, filtro por categoria, cálculo de tempo de leitura (~200 palavras/min) e conexões clínicas com serviços afins.
4. **Resguardo Ético:** 9 tópicos iniciais mantidos em rascunho seguro, sem publicação pública indevida ou textos simulados.

---

## 10. ESTADO APÓS PROMPT 10 (CONTATO, WHATSAPP, PRG E MINIMIZAÇÃO DE DADOS)

O fluxo oficial de contato e acolhimento institucional foi implementado observando rigorosamente as diretrizes éticas e legais:
1. **Minimização de Dados (LGPD):** Modelo `MensagemContato` (`contato/models.py`) coletando exclusivamente `nome`, `email`, `telefone`, `servico_interesse`, `mensagem` e `aceite_privacidade`. Ausência absoluta de campos clínicos, diagnósticos, sintomas, medicamentos, documentos ou dados de telemetria invasiva (IP, User-Agent).
2. **Padrão Post/Redirect/Get (PRG):** Processamento de submissão com redirecionamento HTTP 302 para `/contato/` e feedback empático via `django.contrib.messages`, prevenindo reenviar acidental no reload (F5).
3. **Proteção Contra Bots e Abusos:**
   - Honeypot invisível (`campo_verificacao`) com descarte silencioso e log informativo.
   - Rate limiting transitório via Django cache (`LocMemCache`) com hash SHA-256 anônimo (5 requisições por 15 minutos), retornando HTTP 429 acolhedor.
   - Preservação da integridade: nenhuma chave de rate limit contém o IP original em texto claro no banco de dados.
4. **Resiliência do Envio de E-mail:** Disparo de notificação assíncrona/segura com captura de exceções para impedir que indisponibilidades transitórias de SMTP causem erro 500 para o visitante.
5. **Acessibilidade e Usabilidade:** Formulário 100% funcional sem JavaScript, com labels associados semanticamente (`for`/`id`), atributos `aria-describedby` e contraste de cores conforme as diretrizes WCAG.
6. **Integração Completa:** Rota `/contato/` responsiva (2 colunas em desktop, empilhada em mobile), card WhatsApp com número centralizado via `ConfiguracaoSite.whatsapp_link`, aviso claro sobre dados confidenciais e página factual de política de privacidade em `/politica-de-privacidade/`.

---

## 11. ESTADO APÓS PROMPT 11 (PRIVACIDADE, LGPD, COOKIES, RETENÇÃO E GOVERNANÇA)

A governança técnica de privacidade foi consolidada sobre a arquitetura existente sem introdução de artificialidades ou overengineering:
1. **Auditoria Real e Ausência de Rastreamento:** Verificação integral confirmando a ausência de Google Analytics, Meta Pixel, Google Tag Manager, Hotjar, CAPTCHAs invasivos, iframes e CDNs externas. Tipografia servida via Google Fonts e assets servidos localmente via `static/`.
2. **Documentos de Governança Criados:**
   - `documentacao/MAPA_DE_DADOS.md`: inventário dos 5 fluxos de dados reais, bases legais em pendência jurídica e confirmação de dados não coletados.
   - `documentacao/TERCEIROS_E_COOKIES.md`: catalogação dos terceiros reais (Google Fonts, WhatsApp, Instagram, Maps, SMTP, Host) e checklist obrigatório para adição futura de terceiros.
3. **Páginas de Políticas Atualizadas e Criadas:**
   - `/privacidade/` (e `/politica-de-privacidade/`): estruturada com as 14 seções factuais obrigatórias, sem promessas jurídicas genéricas ou dados inventados.
   - `/cookies/` (e `/politica-de-cookies/`): tabela técnica detalhando os cookies essenciais de primeira parte (`csrftoken`, `sessionid`, `messages`), atestando a ausência de cookies de rastreamento e orientando o gerenciamento no navegador.
4. **Decisão Técnica sobre Consentimento:** Banner de cookies deliberadamente **não implementado no estado atual**, pois a aplicação opera estritamente com cookies técnicos e necessários que, conforme as resoluções da ANPD, dispensam consentimento prévio, evitando *dark patterns* de falsa escolha.
5. **Mecanismo Seguro de Retenção e Expurgos:**
   - Configuração `CONTATO_RETENCAO_DIAS` via settings/env (padrão `None`, sem valor fictício).
   - Comando administrativo `python manage.py limpar_contatos_expirados` com modo `--dry-run`, bloqueio seguro caso a variável não esteja definida e log seguro com zero PII.
6. **Integridade Estrutural:** Zero migrações geradas (`makemigrations --check` limpo), isolamento de permissões no Django Admin (`has_add_permission = False`) e suíte de 120 testes aprovada com 100% de sucesso.

---
*Este plano arquitetural reflete com precisão o código real em funcionamento.*


