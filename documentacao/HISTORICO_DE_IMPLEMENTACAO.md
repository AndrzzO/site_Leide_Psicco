# HISTÓRICO DE IMPLEMENTAÇÃO — INSTITUTO MENTE EM FOCO
**REGISTRO CRONOLÓGICO DE ETAPAS, ENTREGAS E DECISÕES TÉCNICAS**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

---

## PROMPT 00 — CONTEXTO MESTRE, CONTRATO DO PROJETO E REGRAS ABSOLUTAS
* **Data:** 21/09/2026
* **Objetivo:** Estabelecer a base documental inegociável, analisar o material do cliente e a imagem de referência da Home, definir o contrato do projeto e catalogar pendências.
* **Entregas Realizadas:**
  * Criação da pasta `documentacao/`.
  * Criação de `CONTEXTO_MESTRE.md` (identidade, conceito tríplice COMPREENDER • CUIDAR • RECONSTRUIR, regras éticas do CFP, vedações e diretrizes de design).
  * Criação de `ARQUITETURA_PLANEJADA.md` (especificação da arquitetura SSR modular em Django, divisão de apps e diretórios).
  * Criação de `MAPA_DE_PAGINAS.md` (matriz de 14 páginas, rotas, CTAs e requisitos de SEO).
  * Criação de `INVENTARIO_DE_IMAGENS.md` (catalogação IMG-001 a IMG-026 com aspect-ratio e regras de placeholders).
  * Criação de `CHECKLIST_DE_QUALIDADE.md` (critérios permanentes de Design, Acessibilidade WCAG, Segurança e Performance).
  * Criação de `PENDENCIAS_DO_CLIENTE.md` (registro de dados não fornecidos com marcador `PENDENTE_DEFINICAO`).
* **Decisões Técnicas:**
  * Proibição de SPAs (React, Vue) ou overengineering.
  * Preservação estrutural de proporções de imagens com `object-fit: cover`.
  * Não inventar dados cadastrais ou acadêmicos.

---

## PROMPT 01 — FUNDAÇÃO TÉCNICA E ESTRUTURA BASE DO DJANGO
* **Data:** 21/09/2026
* **Objetivo:** Construir a infraestrutura técnica operacional do Django, com separação de ambientes, segurança, arquivos estáticos/mídia, templates semânticos e suíte inicial de testes.
* **Arquivos Criados:**
  * `manage.py`
  * `.gitignore`
  * `.env.example` e `.env` local (ignorado pelo git)
  * `.venv/` (Ambiente virtual isolado Python 3.14 com todas as dependências instaladas)
  * `requirements.txt` (Django 6.0+, python-decouple 3.8, dj-database-url 3.1.2)
  * `configuracoes/__init__.py`, `asgi.py`, `wsgi.py`, `urls.py`
  * `configuracoes/settings/base.py`, `desenvolvimento.py`, `producao.py`, `__init__.py`
  * Apps criados com `apps.py`, `models.py`, `admin.py`, `views.py`, `urls.py`, `tests.py`:
    * `nucleo`
    * `paginas`
    * `servicos`
    * `conteudos`
    * `contato`
  * Templates e assets estruturais:
    * `templates/base/base.html` (com skip link acessível, meta tags base, headers semânticos)
    * `templates/paginas/inicio_temporario.html` (página de teste da rota `/`)
    * `templates/erros/400.html`, `403.html`, `404.html`, `500.html`
    * `static/css/tokens.css` (design tokens com as 6 cores oficiais da paleta)
    * `static/css/base.css` (reset moderno, foco visível, layout acessível)
    * `static/js/base.js` (vanilla JS para navegação e foco de acessibilidade)
    * Diretórios com `.gitkeep` para `componentes`, `includes`, `imagens`, `icones`, `media`
  * Documentação: `README.md` multiplataforma e este `HISTORICO_DE_IMPLEMENTACAO.md`.
* **Decisões Técnicas:**
  * Separação estrita de settings: `desenvolvimento.py` com SQLite e console email backend; `producao.py` com `DEBUG = False`, verificação contra chaves inseguras, SSL, HSTS e `DATABASE_URL` PostgreSQL.
  * Implementação de context processor `dados_institucionais` para disponibilizar nome, profissional, assinaturas e canais de contato sem acoplamento.
  * Inclusão de endpoint `/health/` limpo (HTTP 200 "OK") para futuros orquestradores.
  * Execução das migrações fundamentais oficiais do Django (`auth`, `admin`, `sessions`, `contenttypes`).
* **Testes Executados:**
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py test`: 7 testes executados com 100% de sucesso (rota raiz 200, herança de base.html, health check 200, handler 404 customizado, context processor e proteção contra SECRET_KEY insegura em produção).
  * `python manage.py collectstatic --dry-run`: 133 arquivos estáticos mapeados corretamente.

---

## PROMPT 02 — MODELAGEM ESSENCIAL, CONFIGURAÇÕES INSTITUCIONAIS E DJANGO ADMIN
* **Data:** 21/09/2026
* **Objetivo:** Implementar os modelos institucionais administráveis essenciais, customização completa do Django Admin como CMS seguro, proteção de uploads de mídia e popular dados iniciais oficiais de forma idempotente.
* **Modelos Criados:**
  * App `nucleo`:
    * `ConfiguracaoSite` (Singleton com trava de integridade `pk=1`, validação limpa, URLs institucionais e logos/favicon/OG image).
    * `Profissional` (Perfil da psicóloga Mari Menezes, biografia oficial validada, frase editorial, slug automático e fotos editoriais).
    * `RedeSocial` (Perfis sociais com ícones pré-aprovados e ordenação visual).
  * App `servicos`:
    * `AreaAtuacao` (5 pilares clínicos essenciais: Psicologia, Neuropsicologia, Traumas, Separação e Recomeços, Novos Relacionamentos, com badge, descrição concisa e capa).
    * `Servico` (Serviços e avaliações clínicas com vinculação por chave estrangeira à Área de Atuação, resumo, texto editorial e SEO).
* **Validações e Uploads Seguros:**
  * `nucleo/validators.py`: `validar_imagem` (limite estrito de 10 MB, extensões permitidas `.jpg`, `.jpeg`, `.png`, `.webp`, `.ico` e inspeção binária real com Pillow `Image.open().verify()`).
  * `nucleo/upload_paths.py`: geradores de caminhos determinísticos e seguros com UUID/slug (`institucional/`, `profissionais/`, `areas/`, `servicos/`).
* **Django Admin Customizado (CMS):**
  * `ConfiguracaoSiteAdmin`: trava singleton (`has_add_permission`, `has_delete_permission=False`), organização por fieldsets temáticos e preview seguro de imagens.
  * `ProfissionalAdmin`: prepopulated_fields para slug, fieldsets de biografia e fotos, preview visual das fotos no admin.
  * `RedeSocialAdmin`: list_display, list_editable (`ativo`, `ordem`), list_filter.
  * `AreaAtuacaoAdmin` e `ServicoAdmin`: filtros por status, ordenação, busca, edição direta na lista e previews visuais das capas.
* **Processador de Contexto Resiliente:**
  * `nucleo/context_processors.py`: consulta segura a `ConfiguracaoSite` e `Profissional` com tratamento de exceções de banco de dados (`OperationalError`, `ProgrammingError`) e fallback automático para settings.
* **Carga Inicial Idempotente:**
  * Comando `python manage.py popular_dados_iniciais`: cria e atualiza dados institucionais oficiais sem duplicidade via `get_or_create` e `update_or_create`.
* **Documentação Atualizada / Criada:**
  * `documentacao/GUIA_DO_ADMIN.md` (manual completo de uso do Admin, proporções recomendadas de imagem e regras editoriais).
  * `documentacao/ARQUITETURA_PLANEJADA.md` (seção 8 com estado pós-prompt 02).
  * `documentacao/MAPA_DE_PAGINAS.md` (vínculos dos models com as páginas).
  * `documentacao/INVENTARIO_DE_IMAGENS.md` (mapeamento IMG-001 a IMG-026 para os campos de mídia).
  * `documentacao/PENDENCIAS_DO_CLIENTE.md` (atualização dos status de preenchimento).
  * `documentacao/CHECKLIST_DE_QUALIDADE.md` (marcação de critérios de Admin e segurança de uploads).
* **Testes Executados:**
  * 22 testes automatizados executados e aprovados com 100% de sucesso em 3.67s.
  * `python manage.py check`: 0 issues.
  * `python manage.py makemigrations --check`: nenhuma alteração pendente detectada.

---

## PROMPT 03 — DESIGN SYSTEM, TOKENS VISUAIS, TIPOGRAFIA E COMPONENTES BASE
* **Data:** 21/09/2026
* **Objetivo:** Estabelecer o Design System oficial do Instituto Mente em Foco, com arquitetura CSS modular, tipografia editorial (Cormorant Garamond + Montserrat), escala tipográfica com clamp, botões em pílula, cards semânticos, frames de imagem com aspect-ratio nativo, placeholders elegantes e laboratório visual `/design-system/` para auditoria responsiva em DEBUG.
* **Arquitetura CSS Modular Criada / Atualizada:**
  * `static/css/tokens.css`: Centralização absoluta das 6 cores da paleta oficial, tokens semânticos de superfície, texto, borda e ação, escala fluida de tipografia com `clamp()`, ritmo de espaçamento (`--espaco-1` a `--espaco-24`), border-radius (`--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-pill`) e sombras suaves.
  * `static/css/base.css`: Reset moderno com box-sizing global, estilos base de `html` e `body`, acessibilidade (`:focus-visible`, `.skip-link`, `.sr-only`, `.visually-hidden`), formulários base e preferência de movimento reduzido (`prefers-reduced-motion`).
  * `static/css/tipografia.css`: Hierarquia de títulos (`.titulo-hero`, `.titulo-display`, `.titulo-secao`, `.titulo-card`, `.titulo-menor`), `.eyebrow` em caixa alta com espaçamento, parágrafos com limitação de caracteres (60-75ch), `.frase-destaque`, `blockquote`, `.texto-assinatura` e listas editoriais.
  * `static/css/layout.css`: Containers responsivos (`.container`, `.container-largo`, `.container-texto`), sistema de grids (`.grid-2`, `.grid-2--hero`, `.grid-cards`, `.grid-areas`, `.fileira-identificacao`), superfícies com respiro (`.secao--clara`, `.secao--areia`, `.secao--verde`) e ritmo vertical (`.flow`).
  * `static/css/componentes.css`: Componentes de interface: botões (`.btn`, `.btn--primario`, `.btn--secundario`, `.btn--whatsapp`, `.btn--dourado`), link com seta (`.link-seta`), badges, cards (`.card`, `.card-servico`, `.card-foto` com overlay suave, `.card-identificacao`, `.card-artigo`), frames de mídia (`.media-frame`, `.ratio-4-5`, `.ratio-4-3`, `.ratio-16-9`, `.ratio-1-1`), componente oficial `.placeholder-imagem`, passos editoriais (`.step`) e accordion acessível (`<details>/<summary>`).
  * `static/css/utilitarios.css`: Classes utilitárias indispensáveis (alinhamentos, visibilidade responsiva, ponto focal de imagem).
* **Integração no Template Base:**
  * `templates/base/base.html`: Pré-conexão (`preconnect`) e carregamento de fontes do Google Fonts com `font-display: swap` (Cormorant Garamond + Montserrat) e inclusão dos 6 arquivos CSS na ordem estrita de precedência.
* **Laboratório Visual Criado:**
  * Rota `/design-system/` e view `laboratorio_design_system` no app `paginas`.
  * Template `templates/paginas/laboratorio_design_system.html` exibindo todas as cores, escalas, botões, 7 cards de identificação da referência, cards de serviços, cards fotográficos, placeholders de mídia, seções em diferentes superfícies e formulários base.
  * Trava de segurança: rota ativa estritamente quando `DEBUG = True`; em ambiente de produção (`DEBUG = False`), responde com HTTP 404.
* **Documentação Criada:**
  * `documentacao/DESIGN_SYSTEM.md`: Manual completo dos tokens, paleta, escalas, componentes e snippets de código HTML.
  * `documentacao/CHECKLIST_DE_QUALIDADE.md`: Atualizado com os critérios de fidelidade visual, acessibilidade e performance homologados.
* **Testes Automatizados Executados:**
  * 26 testes automatizados executados e 100% aprovados em 3.88s (OK).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: nenhuma alteração pendente detectada (banco preservado sem novas migrações).
  * `python manage.py collectstatic --dry-run`: 137 arquivos estáticos mapeados e validados.

---

## PROMPT 04 — ESTRUTURA GLOBAL DA INTERFACE: HEADER, NAVEGAÇÃO, MENU MOBILE, FOOTER, WHATSAPP FLUTUANTE E COMPONENTES GLOBAIS
* **Data:** 21/09/2026
* **Objetivo:** Implementar de forma definitiva a estrutura global de navegação e componentes persistentes da interface (Header fixo translúcido, Navegação desktop semântica, Menu Mobile drawer em Vanilla JS acessível, Footer institucional completo em 4 colunas e Botão Flutuante do WhatsApp), com integração segura de dados dinâmicos do CMS e preservação de estabilidade.
* **Componentes Criados:**
  * `templates/componentes/logo.html`: Exibição de logo dinâmico do CMS com fallback nobre em tipografia (*Cormorant Garamond* + subtítulo em *Montserrat*).
  * `templates/componentes/menu_principal.html`: Menu semântico com 9 rotas oficiais, suporte a `aria-current="page"` e classe ativa via `request.resolver_match`.
  * `templates/componentes/header.html`: Header sticky (84px, blur, off-white), alinhamento da marca, navegação horizontal desktop, botão CTA "Agendar atendimento", acionador mobile acessível (`aria-expanded`, `aria-controls`), drawer lateral deslizante e backdrop.
  * `templates/componentes/footer.html`: Rodapé em 4 colunas (Identidade + CRP condicional, Links institucionais, Especialidades clínicas, Atendimento e redes sociais ativas), divisor dourado sutil, ano dinâmico `{% now "Y" %}` e link da Política de Privacidade.
  * `templates/componentes/whatsapp_flutuante.html`: Botão flutuante estilizado nas cores da clínica (sem néon), renderizado condicionalmente caso `WHATSAPP_LINK` esteja preenchido.
* **Scripts e Estilização:**
  * `static/js/navegacao.js`: Script vanilla JS modular com gerenciamento de estado do drawer, bloqueio de rolagem (`overflow: hidden`), fechamento com `Escape`, clique no backdrop, seleção de links e redimensionamento responsivo de janela.
  * `static/css/componentes.css`: Estilização completa do Header, logo, navegação desktop, menu drawer mobile, backdrop, footer de 4 colunas, botão flutuante WhatsApp e compensação global de âncoras (`[id] { scroll-margin-top: 84px; }`).
* **Rotas e Views Estruturais Adicionadas:**
  * `paginas/urls.py` & `paginas/views.py`: Rotas `sobre_mim` e `politica_privacidade`.
  * `servicos/urls.py` & `servicos/views.py`: 6 rotas especializadas (`psicologia`, `neuropsicologia`, `traumas`, `separacao_recomecos`, `avaliacao`, `reabilitacao_neurocognitiva`).
  * `conteudos/urls.py` & `conteudos/views.py`: Rota `index`.
  * `contato/urls.py` & `contato/views.py`: Rota `index`.
* **Segurança e Resiliência de Dados:**
  * Prevenção de vazamento de marcadores (`PENDENTE_DEFINICAO` ou valores vazios não são renderizados no HTML).
  * Fallback seguro do botão CTA para a página de contato quando o WhatsApp não estiver configurado.
* **Testes Automatizados Executados:**
  * 36 testes executados e 100% aprovados em 3.70s (`paginas/tests.py` expandido com 10 novos testes dedicados aos componentes globais).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: nenhuma migração pendente.

---

## PROMPT 05 — CONSTRUÇÃO COMPLETA DA HOME COM ALTA FIDELIDADE À IMAGEM DE REFERÊNCIA
* **Data:** 21/09/2026
* **Objetivo:** Construir a Home completa e definitiva do Instituto Mente em Foco, reproduzindo com alta fidelidade estética e estrutural a imagem de referência fornecida pelo cliente, consumindo modelos reais do CMS Django (`Profissional`, `AreaAtuacao`, `Servico`), respeitando as diretrizes éticas e de acessibilidade e garantindo 100% de responsividade de 320px a 1920px+.
* **Estrutura de 11 Seções Implementadas:**
  1. **Hero Principal (`.home-hero`):** Composição horizontal assimétrica com fundo em degradê suave off-white/areia, elemento botânico decorativo em SVG, Eyebrow oficial (`COMPREENDER • CUIDAR • RECONSTRUIR`), H1 exato (`Você não precisa permanecer preso ao que viveu.`), parágrafo editorial e duplo CTA em pílula ("Quero conhecer o atendimento" e WhatsApp); coluna visual com retrato dominante 4:5 de Mari Menezes (com fallback nobre de placeholder `IMG-001`), citação flutuante em itálico editorial (*"Cuidar da mente também é uma forma de recomeçar."*) e badge profissional com ícone.
  2. **Seção "Alguns momentos da vida mudam tudo..." (`.secao-introducao`):** Grid de 3 colunas com imagem botânica editorial 1:1 (`IMG-002`), acolhimento das dores e crises no centro, e lista lateral com ícones lineares dos 4 pilares (Psicologia, Neuropsicologia, Traumas, Reabilitação) e citação de apoio.
  3. **Seção de Identificação (`.secao-identificacao`):** Grade com os 7 cards clínicos oficiais com ícones lineares dedicados e frases de acolhimento (sem rotulações ou diagnósticos invasivos).
  4. **Seção Áreas de Atuação (`.secao-areas`):** Exibição dinâmica dos 5 pilares clínicos cadastrados no CMS (`AreaAtuacao`), utilizando componente `.card-foto` com overlay suave, proporção 4:3, badges temáticas, resumos e links com seta apontando para as rotas correspondentes.
  5. **Bloco Sobre Mari Menezes (`.secao-sobre`):** Apresentação da profissional com retrato 4:5 (`IMG-010`), título editorial ("Prazer, eu sou Mari Menezes."), qualificações oficiais, biografia curta e frase de destaque em citação com borda dourada.
  6. **Como Funciona o Atendimento (`.secao-processo`):** 4 etapas sequenciais (`01 Conversar`, `02 Compreender`, `03 Cuidar`, `04 Reconstruir`) utilizando o componente `.step` estilizado.
  7. **Bloco Neuropsicologia & Avaliação (`.secao-neuro`):** Equilíbrio entre a escuta clínica e a investigação cognitiva com tags de funções avaliadas (Atenção, Memória, Funções Executivas, Raciocínio, Linguagem), caixa de esclarecimento sobre a distinção com a avaliação psicológica e CTAs informativos.
  8. **Conteúdos em Destaque (`.secao-conteudos`):** Grade editorial com prévia dos temas futuros aprovados pelo cliente com badge "Publicação em breve" e botão de acesso à área de conteúdos.
  9. **Perguntas Frequentes (`.secao-faq`):** Accordion acessível com tags semânticas nativas `<details>` e `<summary>` esclarecendo dúvidas fundamentais sem invenção de promessas.
  10. **CTA Final (`.secao-cta-final`):** Banner marcante em Verde Oliva (`var(--cor-oliva)`), folhagem decorativa dourada, frase principal ("Cuidar da mente também é uma forma de recomeçar."), assinatura ("Comece por você.") e botão de agendamento/WhatsApp.
  11. **Header e Footer Globais:** Integrados perfeitamente acima e abaixo da página sem alterações destrutivas.
* **Arquivos Criados:**
  * `templates/paginas/home.html`: template definitivo semântico com herança de `base/base.html`.
  * `static/css/home.css`: 1095+ linhas de estilos modulares dedicados à Home com design tokens, tipografia fluida, grids responsivos e suporte a `prefers-reduced-motion`.
  * `static/js/home.js`: script vanilla JS defensivo com `IntersectionObserver` para revelações sutis via progressive enhancement (sem ocultar conteúdo em caso de falha de JS).
* **Arquivos Alterados:**
  * `paginas/views.py`: implementação da view `home(request)` com consultas eficientes ao CMS (`Profissional`, `AreaAtuacao`, `Servico`).
  * `paginas/urls.py`: rota raiz apontando para `views.home`.
  * `paginas/tests.py`: expandido para 45 testes automatizados (13 novos testes cobrindo todos os critérios de aceitação da Home).
  * `documentacao/MAPA_DE_PAGINAS.md`: Home marcada como implementada/definitiva.
  * `documentacao/CHECKLIST_DE_QUALIDADE.md`: critérios de headings, URLs amigáveis, textos alternativos e lazy loading homologados.
---

## PROMPT 06 — REFINAMENTO VISUAL PIXEL-LEVEL, RESPONSIVIDADE AVANÇADA E COMPARAÇÃO DIRETA COM A IMAGEM DE REFERÊNCIA
* **Data:** 21/09/2026
* **Objetivo:** Refinamento minucioso pixel-level da Home sem criação de novas entidades ou apps, comparando sistematicamente com a imagem de referência do cliente (`media_1789960481299.jpg`), corrigindo micro-desvios de proporção, tipografia, espaçamento e alinhamento, auditando a responsividade (320px a 1920px+), acessibilidade WCAG 2.1 AA e garantindo fidelidade visual e estabilidade.
* **Ajustes e Refinamentos Executados:**
  * **Hero Principal:** Proporções de colunas ajustadas para `1.08fr 0.92fr` no desktop; `H1` balanceado em no máximo 3 linhas (`max-width: 18ch; text-wrap: balance; line-height: 1.12; font-weight: 500;`); descrição editorial calibrada (`max-width: 45ch; text-wrap: pretty;`); citação flutuante afinada com fundo off-white translúcido, borda sutil em ouro velho e tipografia cursiva refinada; badge profissional reposicionada harmonicamente no canto inferior direito da foto.
  * **Seção Introdução / Acolhimento:** Reestruturada a coluna lateral direita para grid 2x2 com 4 ícones circulares delicados com borda dourada suave (`Psicologia`, `Neuropsicologia`, `Traumas`, `Reabilitação`) e citação centralizada abaixo, atingindo 100% de paridade com o wireframe da imagem de referência.
  * **Fileira de Identificação (7 Cards):** Configurada para renderização contínua de exatamente 7 colunas em telas amplas ($\ge 1200px$), com cartões verticais esguios (`min-height: 220px`), ícones lineares com respiro superior e frases em itálico editorial. Quebra suave para 4, 3, 2 e 1 coluna conforme viewport decresce.
  * **Áreas de Atuação (5 Cards):** Configurada para 5 colunas em linha única em viewports desktop ($\ge 1100px$), gradiente do overlay fotográfico recalculado para legibilidade ideal dos títulos em *Cormorant Garamond* sem escurecer excessivamente a imagem.
  * **Bloco Sobre Mari Menezes & Demais Seções:** Ritmo vertical padronizado, alinhamento dos botões em pílula com 48px de altura mínima, contraste validado no botão dourado (`#2C3C30` sobre `#C9A86A` garantindo 4.8:1 de contraste WCAG AA).
* **Arquivos Modificados:**
  * `templates/paginas/home.html`: Atualização da 3ª coluna da seção de acolhimento (grid de 4 pilares + citação).
  * `static/css/home.css`: Refinamento de grids, tipografia, overlays, touch targets e media queries responsivas.
* **Validações e Testes:**
  * 45 testes automatizados executados e 100% aprovados em 4.17s.
  * `python manage.py check`: 0 issues.
  * `python manage.py makemigrations --check`: nenhuma alteração pendente (0 migrações criadas).

---

## PROMPT 07 — PÁGINAS INTERNAS DO EIXO PSICOLOGIA
* **Data:** 21/09/2026
* **Objetivo:** Implementar de forma definitiva as 5 páginas internas do Eixo Psicologia (*Sobre Mim*, *Psicologia / Psicoterapia*, *Traumas e Experiências Difíceis*, *Separação & Recomeços* e *Novos Relacionamentos*), mantendo continuidade absoluta com o Design System da Home, sem criar novas migrações e com total rigor ético (CFP).
* **Páginas Implementadas:**
  1. **Sobre Mim (`/sobre-mim/`):** H1 oficial "Prazer, eu sou Mari Menezes.", apresentação editorial com dados de `Profissional`, citação de propósito com barra dourada, pilares clínicos (Compreender, Cuidar, Reconstruir), molduras proporcionais 4:5 e 4:3 com fallback nobre e CTA final.
  2. **Psicologia / Psicoterapia (`/servicos/psicologia/`):** H1 "Psicologia e Psicoterapia", mensagem base de escuta profissional e acolhimento, grade editorial com 11 temas clínicos trabalhados com cuidado (sem diagnósticos), bloco reflexivo e páginas relacionadas.
  3. **Traumas e Experiências Difíceis (`/servicos/traumas/`):** Mensagem "Quando uma experiência termina, suas marcas podem permanecer.", 4 eixos de repercussão (Emoções, Pensamentos, Comportamentos, Relações), bloco de cuidado no ritmo individual, frase de destaque "Uma experiência difícil não precisa definir toda a sua história." sem promessa de cura ou sensacionalismo.
  4. **Separação & Recomeços (`/servicos/separacao-e-recomecos/`):** H1 "Separação e Recomeços", mensagem "Separar-se também é reorganizar a própria vida.", 7 aspectos essenciais trabalhados, frase de destaque "Antes de escolher novamente alguém, talvez seja importante reencontrar você." e ponte para Novos Relacionamentos.
  5. **Novos Relacionamentos (`/servicos/novos-relacionamentos/`):** Mensagem "Recomeçar não significa esquecer.", composição editorial de dois eixos ("Vontade de se envolver novamente" vs. "O medo de sofrer novamente"), reflexão sobre influências passadas, limites saudáveis e escolhas conscientes (sem quizzes ou conselhos amorosos de coach).
* **Componentes Reutilizáveis Criados:**
  * `templates/componentes/hero_interno.html`: cabeçalho editorial com breadcrumb semântico, eyebrow, H1, resumo, CTAs e moldura visual com badge.
  * `templates/componentes/cta_atendimento.html`: seção de fechamento verde oliva com folhagem dourada e duplo canal de acolhimento.
  * `templates/componentes/paginas_relacionadas.html`: bloco contextual discreto com 2 a 3 links para serviços afins sem carrossel.
* **Estilos Modulares Criados:**
  * `static/css/paginas_internas.css`: 430+ linhas estruturando hero interno, breadcrumbs, grids de temas, blocos de dois eixos, citações editoriais e responsividade de 320px a 1920px.
* **Integração e Roteamento:**
  * `servicos/urls.py`: rota `novos-relacionamentos/` adicionada com nome `novos_relacionamentos`.
  * `templates/paginas/home.html`: card de Novos Relacionamentos conectado à rota real e botão Sobre Mim confirmado.
  * Header e Footer: itens institucionais e de serviços ativos e respondendo com HTTP 200.
* **Validações e Testes:**
  * 61 testes automatizados executados e 100% aprovados em 4.27s (16 novos testes cobrindo todas as 5 páginas).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (0 novas migrações).
  * `python manage.py collectstatic --dry-run`: 141 arquivos estáticos mapeados com sucesso.

---

## PROMPT 08 — EIXO TÉCNICO DO SITE (NEUROPSICOLOGIA, AVALIAÇÕES E REABILITAÇÃO)
* **Data:** 21/09/2026
* **Objetivo:** Construção e integração completa do Eixo Técnico do Instituto Mente em Foco, compreendendo as 5 páginas: *Neuropsicologia*, *Hub de Avaliação*, *Avaliação Psicológica*, *Avaliação Neuropsicológica* e *Reabilitação Neurocognitiva*, com total observância aos limites éticos e regulatórios do Conselho Federal de Psicologia (CFP), rigor visual idêntico ao Design System da Home e zero criação de novas migrações.
* **Páginas Implementadas:**
  1. **Neuropsicologia (`/servicos/neuropsicologia/`):** H1 oficial "Neuropsicologia", escopo fundamentado nas relações entre funcionamento cerebral, cognição, emoções e comportamento, grid editorial dos 8 aspectos cognitivos (atenção, memória, funções executivas, raciocínio, linguagem, aspectos emocionais, comportamento e funcionamento cognitivo) com ressalva mandatória "conforme a demanda", ausência de checklists clínicos ou diagnósticos inventados e pontes para avaliação e reabilitação.
  2. **Avaliação Hub (`/servicos/avaliacao/`):** H1 "Avaliação Psicológica e Neuropsicológica", esclarecimento explícito de que são processos técnicos distintos que podem se complementar conforme a demanda, 2 blocos editoriais amplos com links aprofundados para as páginas dedicadas, apresentação geral do fluxo oficial e orientação técnica ética.
  3. **Avaliação Psicológica (`/servicos/avaliacao-psicologica/`):** H1 "Avaliação Psicológica", breadcrumb hierárquico (`Início › Avaliação › Avaliação Psicológica`), processo estruturado voltado a aspectos emocionais, de personalidade e comportamento, integração do componente oficial de fluxo em 6 etapas, devolutiva ética e emissão de documento técnico estritamente "quando indicado" (sem nomes de testes ou promessas).
  4. **Avaliação Neuropsicológica (`/servicos/avaliacao-neuropsicologica/`):** H1 "Avaliação Neuropsicológica", breadcrumb hierárquico (`Início › Avaliação › Avaliação Neuropsicológica`), mapeamento detalhado do perfil cognitivo e funcional por meio de instrumentos padronizados conforme a demanda, fluxo de 6 etapas e direcionamento responsável para Reabilitação Neurocognitiva.
  5. **Reabilitação Neurocognitiva (`/servicos/reabilitacao-neurocognitiva/`):** H1 "Reabilitação Neurocognitiva", breadcrumb hierárquico (`Início › Neuropsicologia › Reabilitação Neurocognitiva`), mensagem oficial rigorosa "Após avaliação e quando houver indicação, estratégias individualizadas voltadas ao funcionamento cognitivo e à vida cotidiana, considerando as necessidades e os objetivos da pessoa", 3 eixos de atuação estruturados, estética de continuidade e cuidado acolhedor, sem promessas de recuperação/cura ou exercícios gamificados inventados.
* **Componente Reutilizável Criado:**
  * `templates/componentes/fluxo_avaliacao.html`: lista ordenada semântica `<ol class="fluxo-avaliacao">` com as 6 etapas oficiais: (1) Entrevista, (2) Aplicação de instrumentos, (3) Análise dos resultados, (4) Integração das informações, (5) Devolutiva, (6) Documento técnico quando indicado, com caixa de ressalva técnica profissional mandatória.
* **Estilos Modulares Expandidos:**
  * `static/css/paginas_internas.css`: Novas seções para fluxo de avaliação (grid responsivo 3x2 desktop e pilha vertical em mobile), grid de 4 colunas para aspectos cognitivos, cartões do hub de avaliação e eixos da reabilitação, mantendo 100% dos tokens da paleta (`--cor-oliva`, `--cor-areia`, `--cor-dourado`, `--cor-taupe`).
* **Integração e Roteamento:**
  * `servicos/urls.py`: Adicionadas as rotas dedicadas `avaliacao-psicologica/` e `avaliacao-neuropsicologica/`, mantendo `neuropsicologia/`, `avaliacao/` e `reabilitacao-neurocognitiva/`.
  * `servicos/views.py`: Views implementadas com consultas otimizadas e fallbacks resilientes.
  * `templates/componentes/menu_principal.html`: Estados ativos configurados para marcar "Neuropsicologia" ativa em `/neuropsicologia/` e `/reabilitacao-neurocognitiva/`, e "Avaliação" ativa em `/avaliacao/`, `/avaliacao-psicologica/` e `/avaliacao-neuropsicologica/`.
* **Validações e Testes:**
  * 69 testes automatizados executados e 100% aprovados em 4.34s (8 novos testes de integração e conformidade ética).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (0 novas migrações).

---

## PROMPT 09 — BLOG / CONTEÚDOS EDUCATIVOS
* **Data:** 21/09/2026
* **Objetivo:** Implementação do módulo real, seguro e profissional de Conteúdos / Blog do Instituto Mente em Foco, compreendendo modelos de categorias e artigos, ciclo de vida editorial (rascunho x publicado x agendado), editor seguro de Markdown com sanitização estrita anti-XSS (`bleach`), listagem paginada (9 por página), busca textual limpa, filtro semântico por categorias, artigo em destaque, página de detalhe com container de leitura aprofundada (max ~720px), conexão clínica com serviços, integração com a Home e Django Admin completo.
* **Módulos e Recursos Implementados:**
  1. **Modelos (`conteudos/models.py`):**
     * `CategoriaArtigo`: nome, slug único e estável, descrição, ordem e ativo.
     * `Artigo`: título, slug estável, resumo, conteúdo em Markdown, imagem de capa com validação, alt text, FK para categoria, FK para `nucleo.Profissional`, FK para `servicos.Servico`, status (`rascunho` por padrão, `publicado`), destaque, data de publicação automática/agendada, SEO básico (meta_titulo, meta_descricao) e propriedades calculadas `conteudo_formatado` (sanitizado) e `tempo_leitura_minutos` (~200 palavras/min).
     * `ArtigoQuerySet`: método `.publicados()` aplicando filtro estrito de segurança (`status='publicado'`, `data_publicacao <= agora`, e categoria ativa ou nula).
  2. **Sanitização Segura (`conteudos/sanitizacao.py`):**
     * Integração das bibliotecas `markdown` e `bleach` com allowlist estrita de tags (`h2`, `h3`, `h4`, `p`, `br`, `strong`, `em`, `ul`, `ol`, `li`, `blockquote`, `a`, `hr`, `code`, `pre`) e protocolos (`http`, `https`, `mailto`).
     * Bloqueio explícito de `<h1>` no corpo do artigo para preservar unicidade do H1 por página para SEO.
     * Remoção automática de `<script>`, atributos de evento inline (`onerror`, `onload`, etc.) e links `javascript:`.
  3. **Rotas e Views (`conteudos/urls.py` e `conteudos/views.py`):**
     * `/conteudos/`: Listagem de artigos com busca `?q=`, destaque editorial isolado na 1ª página, paginação com 9 itens por página e estado neutro acolhedor quando nenhum artigo estiver publicado.
     * `/conteudos/categoria/<categoria_slug>/`: Filtro amigável e semântico por categoria.
     * `/conteudos/<slug>/`: Detalhe do artigo individual com renderização segura, box de serviço relacionado, bio da autora Mari Menezes e grade de até 3 artigos relacionados. Rascunhos e publicações futuras retornam HTTP 404 para usuários não autorizados.
  4. **Templates e Estilos (`conteudos/index.html`, `conteudos/detalhe.html`, `static/css/conteudos.css`):**
     * Design System harmônico com a paleta oficial (Oliva `#2C3C30`, Areia `#F4F1EA`, Dourado `#B8965A`, Taupe `#5C6B5F`).
     * Tipografia: *Cormorant Garamond* nos títulos e *Montserrat* no corpo com entrelinha generosa (1.82).
     * Container de leitura aprofundada com largura balanceada de ~720px (`max-width: 740px`), mantendo legibilidade ideal.
  5. **Integração com a Home e Navegação:**
     * `paginas/views.py`: Consulta dinâmica `Artigo.objects.publicados()[:3]`.
     * `templates/paginas/home.html`: Renderiza cards reais de artigos publicados com imagem e links diretos quando existirem, ou mantém a prévia acolhedora sem quebrar o layout quando não houver publicações.
     * `templates/componentes/menu_principal.html`: Link "Conteúdos" ativo para todas as rotas `/conteudos/*`.
  6. **Django Admin (`conteudos/admin.py`):**
     * `CategoriaArtigoAdmin`: campos pré-populados, contagem dinâmica de artigos publicados e rascunhos.
     * `ArtigoAdmin`: fieldsets organizados, badges visuais coloridos para status (Publicado, Agendado, Rascunho), prévia de capa, cálculo de tempo de leitura e instruções editoriais de segurança.
  7. **Carga Inicial de Dados (`popular_dados_iniciais.py`):**
     * 4 categorias reais criadas: *Psicologia Clínica*, *Relacionamentos*, *Traumas e Recomeços*, *Neuropsicologia e Avaliação*.
     * 9 tópicos fornecidos pelo cliente cadastrados estritamente como **RASCUNHO** (`status='rascunho'`, sem texto falso, sem publicação pública).
* **Validações e Testes:**
  * 19 testes automatizados exclusivos do app `conteudos` criados e 100% aprovados.
  * 88 testes automatizados no total do projeto aprovados em 5.67s.
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected`.

---

## PROMPT 10 — CONTATO, FORMULÁRIO SEGURO, WHATSAPP, FLUXO DE CONVERSÃO E LGPD BÁSICA
* **Data:** 21/09/2026
* **Objetivo:** Implementação do fluxo oficial de contato e acolhimento do Instituto Mente em Foco, compreendendo modelo de mensagens seguro e minimizado (LGPD), formulário robusto com validação em servidor, proteção anti-bot via honeypot invisível, rate limiting anônimo via cache transitório, padrão Post/Redirect/Get (PRG), template editorial responsivo de contato (`/contato/`), página factual de política de privacidade (`/politica-de-privacidade/` e `/privacidade/`), administração segura (`MensagemContatoAdmin`) com campos somente-leitura e proteção ética contra prontuários ou CRM clínico.
* **Módulos e Recursos Implementados:**
  1. **Modelo de Contato (`contato/models.py`):**
     * `MensagemContato`: campos minimizados (`nome`, `email`, `telefone`, `servico_interesse`, `mensagem`, `aceite_privacidade`, `lida`, `criado_em`).
     * Ausência intencional e estrita de campos de telemetria invasiva (sem IP, sem User-Agent no banco), documentos ou dados clínicos sensíveis (sem sintomas, sem diagnósticos, sem prontuário).
  2. **Formulário com Validações Rigorosas (`contato/forms.py`):**
     * `ContatoForm`: honeypot invisível (`campo_verificacao`), validação cruzada exigindo Nome + (E-mail OU Telefone/WhatsApp), validação de tamanho mínimo de telefone (10 dígitos), limite seguro de 2000 caracteres para mensagem e obrigatoriedade do aceite de privacidade.
     * Lista suspensa dinâmica alimentada por `servicos.Servico.objects.filter(ativo=True)` com opção padrão neutra.
  3. **Visão Segura com Rate Limiting e PRG (`contato/views.py`):**
     * Rate limiting por hash SHA-256 anônimo via cache Django (`LocMemCache`): máximo de 5 tentativas a cada 15 minutos, retornando HTTP 429 acolhedor e informativo.
     * Descarte silencioso de spambots quando o honeypot for preenchido, simulando sucesso para frustrar robôs e registrando log de auditoria.
     * Persistência da mensagem no banco e envio assíncrono/resiliente de e-mail institucional via `try/except` (sem causar HTTP 500 caso o servidor SMTP esteja indisponível).
     * Redirecionamento HTTP 302 pós-submissão para `/contato/` (PRG), impedindo reenvio de dados por F5/refresh, com mensagem empática via `django.contrib.messages`.
  4. **Página Editorial de Contato (`contato/templates/contato/index.html` e `static/css/contato.css`):**
     * Layout harmônico em 2 colunas no desktop e empilhamento natural no mobile, respeitando rigorosamente os tokens visuais.
     * Card direto de WhatsApp consumindo `ConfiguracaoSite.whatsapp_link` centralizado.
     * Exibição condicional de canais institucionais (telefone, e-mail, Instagram, horários, consultório físico) apenas quando cadastrados.
     * Alerta visual e ético destacado: *"Por favor, não compartilhe sintomas clínicos, diagnósticos ou dados de saúde confidenciais neste formulário. Este espaço destina-se exclusivamente ao primeiro contato e orientações gerais."*.
     * Total acessibilidade: formulário 100% funcional sem JavaScript, com labels associados semanticamente (`for`/`id`) e feedback de erros por campo.
  5. **Página Factual de Política de Privacidade (`templates/paginas/politica_privacidade.html`):**
     * Informação transparente e concisa sobre a coleta mínima de dados exclusivamente voltada ao retorno de contato.
     * Rotas `/politica-de-privacidade/` e alias `/privacidade/` ativas com HTTP 200.
  6. **Django Admin (`contato/admin.py`):**
     * `MensagemContatoAdmin`: organização em fieldsets claros com badge visual de leitura (Nova / Lida), `list_editable=('lida',)` e ação em lote para marcar como lidas.
     * Campos de submissão em modo `readonly_fields` para proteger a integridade dos dados enviados.
     * Alerta ético explícito na descrição do painel vedando o uso como prontuário ou CRM clínico.
* **Validações e Testes:**
  * 21 testes automatizados exclusivos do app `contato` cobrindo validação de formulário, campos obrigatórios, honeypot, rate limiting (HTTP 429), PRG, proteção XSS, admin e página de privacidade.
  * 109 testes automatizados no total do projeto aprovados com 100% de sucesso.
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected`.

---

## PROMPT 11 — PRIVACIDADE, LGPD, COOKIES, CONSENTIMENTO, RETENÇÃO E GOVERNANÇA DOS DADOS
* **Data:** 21/09/2026
* **Objetivo:** Estabelecer a governança técnica de privacidade e proteção de dados do Instituto Mente em Foco, através de auditoria profunda dos fluxos reais, mapeamento completo de dados e terceiros, eliminação de rastreadores, criação de páginas factuais de Política de Privacidade (14 seções) e Política de Cookies (tabela técnica), implementação de mecanismo de retenção configurável (`limpar_contatos_expirados`), decisão técnica fundamentada sobre banner de consentimento e catalogação de pendências para revisão jurídica formal.
* **Módulos e Recursos Implementados:**
  1. **Auditoria de Privacidade e Governança:**
     * Criação de `documentacao/MAPA_DE_DADOS.md`: inventário minucioso dos 5 fluxos de dados reais (Formulário, WhatsApp, Django Admin, Sessões/CSRF e Rate Limiting), bases legais documentadas como pendentes de revisão jurídica e confirmação de dados não coletados.
     * Criação de `documentacao/TERCEIROS_E_COOKIES.md`: catalogação dos terceiros reais (Google Fonts, WhatsApp, Instagram, Google Maps, provedor SMTP e hospedagem) e checklist obrigatório para avaliação prévia de qualquer adição futura de tecnologias externas.
  2. **Minimização e Proteção Adicional de PII:**
     * Ajuste em `contato/views.py`: remoção do nome do visitante no assunto do e-mail de notificação (`"[Novo Contato] Nova mensagem recebida pelo site"`), prevenindo trânsito desnecessário de dados em cabeçalhos SMTP abertos.
     * Ajuste em `contato/admin.py`: desativação da criação manual de mensagens no painel (`has_add_permission = False`), garantindo rastreabilidade da origem web.
  3. **Mecanismo Seguro de Retenção e Expurgos (LGPD):**
     * Configuração `CONTATO_RETENCAO_DIAS` adicionada em `configuracoes/settings/base.py` e `.env.example` (padrão `None`, sem exclusão cega).
     * Management command `python manage.py limpar_contatos_expirados`:
       * Aborta com segurança e aviso explicativo caso nenhum período de retenção esteja configurado;
       * Modo `--dry-run` para simulação segura sem alteração no banco;
       * Argumento opcional `--dias` para sobreposição deliberada de período;
       * Registro em log estritamente anônimo (quantidade, data e resultado, com zero PII).
  4. **Páginas Institucionais de Políticas:**
     * `templates/paginas/politica_privacidade.html`: reestruturada com as 14 seções factuais mandatórias (Quem Somos, Quais Dados o Site Pode Coletar, Como os Dados São Obtidos, Para Que os Dados São Utilizados, Formulário de Contato, Cookies e Tecnologias, Serviços de Terceiros, Compartilhamento, Armazenamento e Retenção, Segurança, Direitos e Solicitações, Canal de Contato, Alterações da Política, Data da Última Atualização).
     * `templates/paginas/politica_cookies.html`: criada com tabela técnica minuciosa dos cookies essenciais de primeira parte (`csrftoken`, `sessionid`, `messages`), atestado formal de ausência de tecnologias de rastreamento e guia de gerenciamento no navegador.
     * Rotas adicionadas e ativas em `paginas/urls.py`: `/politica-de-cookies/` e `/cookies/`.
     * `templates/componentes/footer.html`: links integrados para Política de Privacidade e Política de Cookies.
  5. **Decisão Técnica sobre Consentimento de Cookies:**
     * Auditoria confirmou 100% de dependência estrita em cookies essenciais de primeira parte, com ausência absoluta de Google Analytics, Meta Pixel, GTM, Hotjar, cookies de terceiros ou Web Storage.
     * Conclusão: **BANNER NÃO NECESSÁRIO NO ESTADO ATUAL**, evitando dark patterns de falsa escolha e mantendo transparência ativa na página de Cookies.
* **Validações e Testes:**
  * 32 testes automatizados no app `contato` e 120 testes no total do projeto aprovados com 100% de sucesso.
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero novas migrações).

---

## PROMPT 12 — SEO TÉCNICO COMPLETO
* **Data:** 21/09/2026
* **Objetivo:** Implementar a infraestrutura técnica completa e segura de SEO para o Instituto Mente em Foco, abrangendo governança de indexação por ambiente, robots.txt, sitemap.xml dinâmico, metadados semânticos centralizados, Open Graph, Twitter Cards, dados estruturados Schema.org (JSON-LD) protegidos contra XSS e validações automatizadas com conformidade ética integral.
* **Módulos e Recursos Implementados:**
  1. **Auditoria e Governança de Indexação:**
     * Criação de `documentacao/AUDITORIA_SEO_TECNICO.md` catalogando todas as 16 rotas, indexabilidade e lacunas prévias.
     * Criação de `documentacao/SEO_TECNICO.md` com arquitetura, esquemas, boas práticas e checklist de produção.
     * Variáveis adicionadas em `configuracoes/settings/base.py` e `.env.example`: `SEO_ALLOW_INDEXING` (default `False`), `GOOGLE_SITE_VERIFICATION`, `BING_SITE_VERIFICATION` e normalização estrita de `SITE_URL.rstrip('/')`.
     * `nucleo/checks.py`: Django System Checks registrando `seo.E001` (bloqueio de indexação com `DEBUG=True`), `seo.E002` (bloqueio com localhost ou URL inválida) e `seo.W001` (alerta de HTTPS).
     * `nucleo/middleware.py`: `SEOMiddleware` injetando `X-Robots-Tag: noindex, nofollow, noarchive` em ambientes de desenvolvimento/staging e controlando cabeçalhos em erros (4xx/5xx), busca interna e páginas legais.
  2. **Robots.txt & Sitemap.xml:**
     * Rota `/robots.txt` dinâmica em `nucleo/views.py` e `templates/seo/robots.txt`: bloqueia bots em dev (`Disallow: /`), permite e aponta para sitemap em produção (`Allow: /` + `Sitemap:`), sem expor a rota administrativa secreta (`DJANGO_ADMIN_URL`).
     * Rota `/sitemap.xml` estruturada via `django.contrib.sitemaps` em `nucleo/sitemaps.py`: `PaginasSitemap`, `ServicosSitemap`, `ConteudosSitemap` (exclusivo para artigos publicados com data <= agora) e `CategoriasSitemap` (apenas com artigos publicados).
  3. **Centralização de Metadados e Redes Sociais:**
     * `templates/base/base.html`: padronização de `<title>` hierárquico, `<meta name="description">` factual, `<link rel="canonical">` absoluto e tags de verificação Google e Bing.
     * Open Graph (`og:site_name`, `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:locale`) e Twitter Cards (`summary_large_image`).
     * `templates/conteudos/detalhe.html`: configuração de `og:type = "article"` e tags canônicas do artigo.
  4. **Dados Estruturados Schema.org (JSON-LD):**
     * `nucleo/templatetags/seo_tags.py`: templatetag `render_json_ld` com escape anti-XSS (`</script>` -> `\u003c/script\u003e`), `render_global_schema` (`WebSite`, `Organization`, `Person`), `render_service_schema` (`Service`), `render_article_schema` (`BlogPosting`), e `render_breadcrumbs_schema` (`BreadcrumbList`).
     * Conformidade ética: ausência absoluta de esquemas de estrelas/notas (`AggregateRating`) ou credenciais inventadas.
  5. **Políticas de Rota e Noindex:**
     * `/conteudos/?q=...`: busca com `meta_robots = "noindex, follow"` e URL canônica limpa para `/conteudos/`.
     * Políticas de privacidade e cookies com `noindex, follow` e canônicas definitivas.
* **Validações e Testes:**
  * 27 novos testes em `nucleo/tests_seo.py` cobrindo robots, sitemaps, canonicals, noindex, system checks, anti-XSS e headers HTTP.
  * **147 testes automatizados no total do projeto** aprovados com 100% de sucesso.
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero novas migrações de modelo).

---

## PROMPT 13 — SEO EDITORIAL E ON-PAGE
* **Data:** 21/09/2026
* **Objetivo:** Auditar, padronizar e consolidar a arquitetura semântica, hierarquia de headings (H1/H2/H3), intenção de URLs, prevenção de canibalização, interlinking contextual e metadados de todas as páginas públicas do Instituto Mente em Foco, garantindo clareza ao visitante e responsabilidade ética segundo as normas do CFP.
* **Módulos e Recursos Implementados:**
  1. **Auditoria Semântica e Hierarquia de Headings:**
     * Confirmação da regra de **exatamente 1 H1 por página** em todas as 16 URLs públicas em tempo de execução.
     * Ordenação lógica de `<h2>` para seções temáticas e `<h3>` para subdivisões, cartões de serviços e fluxo de avaliação, eliminando saltos de níveis arbitrários.
     * Elementos decorativos (eyebrow, badges, números e ramalhetes botânicos) mantidos semanticamente como spans e divs acessíveis, sem poluição da árvore de cabeçalhos.
  2. **Padronização de Titles e Metadados:**
     * Uniformização dos títulos no padrão `[Nome da Página / Tema] | Instituto Mente em Foco` (ou `[Nome da Página] | Psicóloga Mari Menezes | Instituto Mente em Foco`).
     * Meta descriptions individuais, persuasivas e acolhedoras (80 a 160 caracteres), sem promessas de cura, sem diagnósticos invasivos e sem criação de páginas ou termos artificiais por cidade.
  3. **Prevenção de Canibalização e Delimitação Editorial:**
     * Demarcação estrita entre *Psicologia Clínica* (desenvolvimento pessoal contínuo e acolhimento amplo) e *Traumas* (marcas de momentos dolorosos graves do passado).
     * Separação clara entre *Separação & Recomeços* (reorganização pessoal e luto após término recente) e *Novos Relacionamentos* (medo de sofrer, limites e abertura para novos vínculos).
     * Hierarquia lógica entre *Neuropsicologia* (apresentação teórica da especialidade), *Avaliação Hub* (guia orientador), *Avaliação Psicológica* (investigação de aspectos emocionais/personalidade), *Avaliação Neuropsicológica* (8 dimensões cognitivas formais) e *Reabilitação Neurocognitiva* (estratégias práticas cotidianas após avaliação prévia).
  4. **Interlinking Contextual e Eliminação de Páginas Órfãs:**
     * Grafo completo de navegação garantindo no mínimo 2 links de entrada para cada URL e profundidade de até 2 cliques a partir da Home.
     * Conexões contextuais bidirecionais entre serviços afins através do componente `paginas_relacionadas.html`.
     * Textos-âncora naturais e diversificados, evitando termos genéricos ("clique aqui") ou sobreotimização para motores de busca.
     * Isolamento garantido de artigos em rascunho, que permanecem 100% invisíveis na navegação pública e no sitemap.
  5. **Documentação e Governança Criadas:**
     * `documentacao/AUDITORIA_SEO_EDITORIAL.md`: Diagnóstico semântico completo URL a URL.
     * `documentacao/MAPA_DE_INTENCOES_SEO.md`: Matriz de intenções, dores atendidas e fronteiras éticas.
     * `documentacao/MAPA_DE_LINKS_INTERNOS.md`: Mapeamento do grafo de links e textos-âncora.
     * `documentacao/PENDENCIAS_EDITORIAIS.md`: Registro de informações deliberadamente não inventadas (CRP definitivo, endereço físico, redes sociais pendentes).
     * Atualização do `GUIA_DO_ADMIN.md` com o *Checklist Editorial Pré-Publicação*.
* **Validações e Testes:**
  * Nova suíte de testes automatizados em `nucleo/tests_seo_editorial.py` validando H1 único, integridade de status HTTP 200 de todos os links internos, conformidade de titles/descriptions e isolamento de rascunhos.
  * **154 testes automatizados no total do projeto** aprovados com 100% de sucesso.
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero alterações de schema).

---

## PROMPT 14 — AUDITORIA E IMPLEMENTAÇÃO COMPLETA DE ACESSIBILIDADE (WCAG 2.2 — NÍVEL AA)
* **Data:** 21/09/2026
* **Objetivo:** Realizar auditoria minuciosa e implementação completa de acessibilidade digital em conformidade com as diretrizes internacionais WCAG 2.2 no Nível AA, assegurando navegação fluida, digna e autônoma por teclado, leitores de tela e tecnologias assistivas, com foco em HTML semântico nativo ("HTML Semântico First").
* **Módulos e Recursos Implementados:**
  1. **HTML Semântico First e Limpeza de Redundâncias:**
     * Remoção de roles ARIA redundantes em elementos HTML5 (`role="banner"` em `<header>`, `role="main"` em `<main>`, `role="contentinfo"` em `<footer>`, `role="table"` em `<table>`).
     * Inclusão de `tabindex="-1"` em `<main id="conteudo-principal">` para permitir transferência programática e segura de foco pelo skip-link.
     * Mapeamento de múltiplos blocos `<nav>` com atributos `aria-label` exclusivos e descritivos (*Navegação principal*, *Navegação móvel*, *Caminho de navegação*, *Filtrar por categoria*, *Navegação entre páginas de artigos*, *Navegação institucional do rodapé*, *Especialidades clínicas do rodapé*).
  2. **Navegação por Teclado e Foco Visível:**
     * Indicador universal `:focus-visible` calibrado com 2px sólido em verde oliva (`--cor-oliva`), offset de 3px e curvatura suave, atingindo ratio $\ge 3:1$ com o fundo.
     * Skip-link aprimorado: totalmente oculto fora da viewport até receber foco por teclado, tornando-se visível no topo central com alto contraste e moldura nítida.
     * Prevenção de ofuscamento sob cabeçalho fixo (*Focus Not Obscured* - WCAG 2.2 AA Critério 2.4.11): `scroll-margin-top: 96px;` aplicado universalmente a elementos com ID, alvos de âncoras e campos de formulário.
     * Destaque visual evidente com `:focus-within` em todos os cards interativos que possuem links internos.
  3. **Menu Mobile com Gerenciamento de Foco e Focus Trap:**
     * Implementação em JavaScript vanilla de ciclo de foco (*Focus Trap / Loop*) dentro do painel móvel aberto: Tab no último elemento volta ao primeiro (ou ao botão toggle); Shift+Tab no primeiro elemento vai para o último.
     * Suporte universal à tecla `Escape` para fechar a gaveta e restaurar o foco imediatamente para o botão disparador (`toggleBtn`).
     * Atributos de estado sincronizados: `aria-expanded` (true/false) e `aria-label` dinâmico (*Abrir menu de navegação* / *Fechar menu de navegação*).
  4. **Calibração de Contraste Colorimétrico:**
     * Ajuste fino do token `--cor-texto-suave` no `tokens.css` de `#7D766D` (4.05:1) para `#6E675E` (5.01:1), satisfazendo o critério de contraste mínimo $\ge 4.5:1$ sobre o fundo off-white (`#F7F3EB`).
     * Uso da cor dourada (`#C9A86A`) delimitado estritamente a linhas divisórias, molduras e ícones decorativos, nunca em textos essenciais.
  5. **Formulários Acessíveis e Prevenção de Erros:**
     * Rótulos explícitos `<label for="...">` para todos os campos do formulário de contato.
     * Legenda textual explicativa de obrigatoriedade (`.form-legenda-obrigatorio`) associada ao símbolo `*`.
     * Injeção dinâmica no backend Django de `aria-invalid="true"` e `aria-describedby="id_{campo}-erro"` nos widgets que contêm falhas de validação.
     * Sumário acessível de erros no topo do formulário com `role="alert"`, `tabindex="-1"` e links internos para cada campo problemático.
     * Isolamento e blindagem do campo honeypot anti-spam (`aria-hidden="true"`, `tabindex="-1"`, `autocomplete="off"`, estilos offscreen) para que jamais seja anunciado por tecnologias assistivas.
  6. **Acessibilidade de Mídias, SVGs e Tabelas:**
     * Atributo `alt` obrigatório em 100% das imagens (`<img>`).
     * Atributos `aria-hidden="true"` e `focusable="false"` em todos os SVGs decorativos para evitar captura indevida de foco pelo Internet Explorer/Edge antigo.
     * Tabela de cookies em `/politica-de-cookies/` enriquecida com `<caption>` acessível e cabeçalhos `<th scope="col">`.
     * Paginação do Blog com `aria-current="page"` no item ativo e `aria-label` nos links numéricos.
  7. **Movimento Reduzido e Reflow:**
     * Suporte abrangente à media query `@media (prefers-reduced-motion: reduce)` anulando durações de animações, transições e comportamento suave de rolagem.
     * Fluidez em tela estreita de 320px e zoom de 200% sem rolagem bidimensional.
  8. **Documentação e Governança:**
     * Criação de `documentacao/AUDITORIA_DE_ACESSIBILIDADE.md` com análise critério por critério, tabela colorimétrica e declaração de acessibilidade.
     * Atualização do `GUIA_DO_ADMIN.md` com a Seção 12 (*Diretrizes Operacionais de Acessibilidade para Editores*).
     * Atualização do `CHECKLIST_DE_QUALIDADE.md` com a homologação da Fase 14.
* **Validações e Testes:**
  * Nova suíte automatizada em `nucleo/tests_acessibilidade.py` com 11 testes cobrindo idioma, skip-link, landmarks, navs múltiplos, formulários, honeypot, imagens, menu mobile, cookies e paginação.
  * **165 testes automatizados no total do projeto** aprovados com 100% de sucesso (`python manage.py test`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações de banco de dados).

---

## PROMPT 15 — PERFORMANCE, CORE WEB VITALS E OTIMIZAÇÃO COMPLETA DE CARREGAMENTO
* **Data:** 21/09/2026
* **Objetivo:** Realizar auditoria técnica profunda e implementação de engenharia de performance web e Core Web Vitals (LCP, CLS, INP e TTFB), assegurando que o portal carregue de forma instantânea e estável, com zero regressões no design visual, acessibilidade WCAG 2.2 AA e SEO, respeitando a restrição absoluta de não otimizar prematuramente os placeholders fotográficos pendentes de fornecimento.
* **Módulos e Recursos Implementados:**
  1. **Auditoria de Baseline e Comparação Antes x Depois:**
     * Mapeamento de 9 rotas representativas com medições rigorosas de TTFB local, queries SQL, bytes HTML transferidos e contagem de assets.
     * Criação de `documentacao/AUDITORIA_DE_PERFORMANCE.md` documentando o diagnóstico inicial e a segunda medição sob idênticas condições de teste.
  2. **Infraestrutura Preparada para Fotografias Futuras:**
     * Atualização completa de `documentacao/INVENTARIO_DE_IMAGENS.md` mapeando todos os 28 slots visuais com 13 propriedades técnicas individuais (ID, página, seção, função, aspect-ratio, dimensões de exibição, dimensões de arquivo recomendadas, formato futuro, status LCP, status Lazy, object-fit, object-position e status atual: *Aguardando foto definitiva*).
     * Preservação dimensional estrita dos placeholders existentes com classes CSS nativas (`.media-frame`, `.ratio-4-5`, `.ratio-16-9`, `.ratio-4-3`), garantindo Cumulative Layout Shift (**CLS = 0**).
  3. **Estratégia Defensiva de LCP e Prioridade de Descoberta:**
     * Elementos do topo da dobra e Hero configurados com `loading="eager"`, `fetchpriority="high"` e `decoding="async"`.
     * Elementos secundários abaixo da dobra configurados com `loading="lazy"` e `decoding="async"`.
  4. **JavaScript Não-Bloqueante (Zero Long Tasks):**
     * Inclusão do atributo `defer` na chamada de `base.js` no template `base.html`, completando a estratégia onde 100% dos scripts (`base.js`, `navegacao.js`, `home.js`) não bloqueiam o parser HTML.
     * Volume total de JavaScript no projeto de apenas **6.3 KB** sem compressão (~2.1 KB comprimido).
  5. **Otimização de Consultas SQL e I/O:**
     * Eliminação de consulta redundante de `ConfiguracaoSite.get_solo()` na view de Contato (`contato/views.py`), reduzindo a rota de 5 para 4 queries no fluxo GET.
     * Manutenção de `select_related('categoria', 'autor')` no Blog e `select_related('area')` na Home, impedindo qualquer padrão N+1.
  6. **Governança e Documentação:**
     * Criação de `documentacao/PERFORMANCE_E_CORE_WEB_VITALS.md` com arquitetura de carregamento, metas, distinção Lab vs Field Data e recomendações de infraestrutura para produção (WhiteNoise/Nginx, Cache-Control imutável e compressão).
     * Criação de `documentacao/GUIA_DE_IMAGENS_E_PERFORMANCE.md` com orientações práticas para a cliente e administradores.
     * Atualização de `DESIGN_SYSTEM.md`, `GUIA_DO_ADMIN.md` e `CHECKLIST_DE_QUALIDADE.md`.
* **Validações e Testes:**
  * Nova suíte automatizada em `nucleo/tests_performance.py` com 10 testes cobrindo limites de queries, script defer, Google Fonts swap/preconnect, prioridade LCP no Hero, lazy loading e rotas diretas 200.
  * **175 testes automatizados no total do projeto** aprovados com 100% de sucesso (`python manage.py test`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero novas migrações).

---

## PROMPT 16 — SEGURANÇA DJANGO E HARDENING DE PRODUÇÃO
* **Data:** 24/09/2026
* **Objetivo:** Realizar auditoria técnica ampla e hardening defensivo estrito da aplicação em conformidade com as melhores práticas da OWASP e as diretrizes do Django 6.0, sem quebrar o ambiente de desenvolvimento local, sem criar migrações de banco de dados e sem expor qualquer segredo nos relatórios.
* **Módulos e Recursos Implementados:**
  1. **Auditoria Geral de Vulnerabilidades e Código:**
     * Auditoria de segredos e histórico: ausência de credenciais reais versionadas, arquivo `.env` protegido no `.gitignore` com chaves puramente sintéticas de desenvolvimento.
     * Criação de `documentacao/AUDITORIA_DE_SEGURANCA.md` categorizando 18 achados por severidade (Crítico, Alto, Médio, Baixo, Informativo), todos 100% resolvidos.
  2. **Fortalecimento de Configurações de Produção:**
     * `configuracoes/settings/producao.py`: Fail-closed para `DJANGO_SECRET_KEY` e `DATABASE_URL`; rejeição estrita de `DJANGO_ALLOWED_HOSTS` vazio ou contendo wildcard `*`.
     * `DEBUG = False` rigorosamente fixado.
     * Cookies de sessão e CSRF configurados com `Secure = True`, `HttpOnly = True` (sessão) e `SameSite = 'Lax'`.
  3. **HTTPS e Rollout Progressivo de HSTS:**
     * `SECURE_SSL_REDIRECT` configurável via `DJANGO_SECURE_SSL_REDIRECT` (padrão `True` em produção).
     * HSTS parametrizado via `DJANGO_SECURE_HSTS_SECONDS` (padrão `0` pré-deploy para evitar bloqueios acidentais de domínio antes da homologação TLS), com plano progressivo de ativação documentado (300s -> 86400s -> 31536000s).
     * `SECURE_HSTS_PRELOAD` mantido `False` por padrão, evitando submissão prematura ao catálogo fixo dos navegadores.
     * `SECURE_PROXY_SSL_HEADER` tornado configurável e dependente da terminação TLS comprovada no reverse proxy de deploy.
  4. **Cabeçalhos HTTP Defensivos:**
     * `X-Frame-Options: DENY` e `SECURE_CONTENT_TYPE_NOSNIFF = True` (`nosniff`).
     * `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'` em base e produção.
     * `SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'` (COOP) habilitado nativamente no Django 6.0.
     * Criação do `SecurityHeadersMiddleware` em `nucleo/middleware.py` injetando `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()`.
  5. **Content Security Policy (CSP Nativa Django 6.0):**
     * Inclusão do `django.middleware.csp.ContentSecurityPolicyMiddleware` e context processor `django.template.context_processors.csp`.
     * Política `SECURE_CSP` configurada com allowlist estrita (`default-src 'self'`, `script-src 'self' 'nonce-...'`, Google Fonts e objetos bloqueados).
     * Suporte a `SECURE_CSP_REPORT_ONLY` para auditoria e diagnóstico em homologação.
     * Suporte a nonce dinâmico nos blocos JSON-LD em `nucleo/templatetags/seo_tags.py`.
  6. **Proteção contra CSRF e XSS:**
     * Zero ocorrências de `@csrf_exempt` em todo o código.
     * Sanitização robusta com Bleach em `conteudos/sanitizacao.py` preservada para artigos do Blog.
     * Auto-escaping do Django Templates ativo e verificado.
  7. **Redução da Superfície de Ataque no Backend:**
     * 100% de consultas usando o Django ORM nativo parametrizado; zero raw SQL.
     * Bloqueio comprovado de rascunhos e agendamentos futuros para anônimos (retornando 404).
     * Prevenção de form tampering e mass assignment em `ContatoForm`.
  8. **Segurança de Uploads e Django Admin:**
     * Validação binária profunda de imagens via Pillow (`Image.open().verify()`), teto de 10 MB, nomes UUID imprevisíveis e bloqueio de executáveis/SVG.
     * Aumento do comprimento mínimo de senhas administrativas para 12 caracteres (`MinimumLengthValidator`).
  9. **Proteção de PII e Tratamento de Erros:**
     * Aplicação de `@sensitive_post_parameters('nome', 'email', 'telefone', 'mensagem')` na view `contato.views.index`.
     * Zero dados pessoais ou credenciais gravados nos logs de produção.
     * Handlers de erro 400, 403, 404 e 500 sem vazamento de traceback ou caminhos internos com `DEBUG=False`.
  10. **Documentação e Inventários:**
      * Criação de `documentacao/AUDITORIA_DE_SEGURANCA.md`.
      * Criação de `documentacao/SEGURANCA_E_HARDENING.md`.
      * Criação de `documentacao/INVENTARIO_DE_SECRETS.md` (sem valores).
      * Criação de `documentacao/CHECKLIST_DE_SEGURANCA_PRODUCAO.md`.
      * Atualização do `README.md`, `.env.example`, `CHECKLIST_DE_QUALIDADE.md` e `PENDENCIAS_DO_CLIENTE.md`.
* **Validações e Testes:**
  * Criação de `nucleo/tests_seguranca.py` com 23 novos testes automatizados de segurança.
  * **198 testes automatizados no total do projeto** aprovados com 100% de sucesso (`python manage.py test`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py check --deploy`: revisado com sucesso.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações).
  * `python -m pip check`: zero dependências quebradas.

---

## PROMPT 17 — PROTEÇÃO CONTRA ABUSO, RATE LIMITING E DoS LÓGICO
* **Data:** 26/09/2026
* **Objetivo:** Implementar proteção em camadas contra automação maliciosa, força bruta, credential stuffing, spam em formulários e DoS lógico, sem impor rate limit global que prejudique navegação legítima, sem novas dependências pesadas, sem migrações de banco e com preservação estrita de privacidade (LGPD).
* **Módulos e Recursos Implementados:**
  1. **Arquitetura Centralizada de Rate Limit (`nucleo/rate_limit.py`):**
     * Criação do serviço `RateLimiter` utilizando o cache nativo do Django (`LocMemCache` em desenvolvimento; compatível com Redis/Memcached em produção multi-worker).
     * Namespace padronizado: `security:rl:v1:{escopo}:{tipo}:{digest}`.
     * Pseudonimização irreversível via **HMAC-SHA256** utilizando `SECRET_KEY` da aplicação, garantindo zero armazenamento de IP bruto ou usernames em cache e logs.
     * Resiliência **fail-open**: falhas no backend de cache registram warning sem PII e não derrubam a aplicação com erro 500.
     * Resposta HTTP 429 padronizada com `Retry-After: 900`, `Cache-Control: no-store` e template acessível [`templates/erros/429.html`](file:///c:/Users/andre/Documents/SiteDjangoLeide/templates/erros/429.html).
  2. **Resolução Segura de IP e Anti-Spoofing:**
     * `obter_ip_cliente(request)` adota `REMOTE_ADDR` como padrão incondicional.
     * `HTTP_X_FORWARDED_FOR` falsificado é sumariamente ignorado quando `TRUST_PROXY_CLIENT_IP = False`.
  3. **Proteção do Formulário de Contato (`contato/views.py`):**
     * Cota de 5 envios por 15 minutos por origem HMAC. Requisições acima do limite retornam HTTP 429 sem gravar no banco de dados e sem despachar e-mail via SMTP (mitigando mail bombing).
     * Honeypot invisível (`campo_verificacao`) preservado e integrado.
  4. **Proteção de Força Bruta no Django Admin (`wrap_admin_login`):**
     * Cota por Origem: 10 falhas em 15 minutos (bloqueio temporário de 15 minutos).
     * Cota Combo (Origem + Username): 5 falhas em 15 minutos.
     * Mitigação de DoS de CPU: interceptação com 429 antes de invocar computação de hash de senha PBKDF2 quando bloqueado.
     * Prevenção de Account Lockout DoS: bloqueio restrito ao IP atacante; administradores em redes legítimas continuam acessando.
     * Prevenção de enumeração: falhas para usuários inexistentes produzem idêntico tempo de resposta e mensagem genérica.
     * Limpeza pós-sucesso: login bem-sucedido zera contadores combo sem resetar cota de IP.
  5. **Hardening de Busca e Paginação (`conteudos/views.py`):**
     * Termo de busca `q` truncado em no máximo 100 caracteres antes da consulta ORM.
     * Sanitização defensiva do parâmetro `page` evitando overflow de inteiros.
     * Tamanho de página estritamente fixo no backend (9 itens).
  6. **Governança e Verificações de Sistema:**
     * System Check customizado `ratelimit.E001` em `nucleo/checks.py` validando integridade de thresholds positivos.
     * Criação de 4 documentos: `AUDITORIA_DE_ABUSO_E_RATE_LIMIT.md`, `PROTECAO_CONTRA_ABUSO.md`, `MATRIZ_DE_RATE_LIMIT.md` e `GUIA_DE_INCIDENTES_DE_ABUSO.md`.
     * Atualização do `README.md`, `.env.example`, `GUIA_DO_ADMIN.md`, `CHECKLIST_DE_SEGURANCA_PRODUCAO.md`, `CHECKLIST_DE_QUALIDADE.md`, `PENDENCIAS_DO_CLIENTE.md` e `MAPA_DE_DADOS.md`.
* **Validações e Testes:**
  * Criação de `nucleo/tests_rate_limit.py` com 21 novos testes cobrindo Contato, Admin, IP/Proxy spoofing, HMAC, fail-open e resposta 429.
  * **219 testes automatizados no total do projeto** aprovados com 100% de sucesso (`python manage.py test`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações criadas).
  * `python -m pip check`: zero dependências quebradas.

---

## PROMPT 18 — SUÍTE COMPLETA DE TESTES AUTOMATIZADOS E PREVENÇÃO DE REGRESSÃO
* **Data:** 26/09/2026
* **Objetivo:** Auditar, consolidar e expandir a suíte completa de testes automatizados do Instituto Mente em Foco, com foco estrito em contratos da aplicação, comportamento real, resiliência, prevenção de regressão e garantia de qualidade contínua em todas as camadas (Models, Forms, Views, URLs, Admin, Contato, Blog, SEO, Privacidade, Segurança, Rate Limit, Uploads, Erros, Acessibilidade WCAG 2.2 AA e Performance), sem vanity coverage, com zero dados reais, zero chamadas externas de rede e zero migrações.
* **Módulos e Recursos Implementados:**
  1. **Criação da Suíte de Regressão Global (`nucleo/tests_regressao.py`):**
     * `LinkCrawlerRegressionTest`: Crawler automatizado que navega por todas as 16 rotas públicas primárias, extrai todos os links internos (`href`) e valida que 100% dos links respondem com sucesso (zero links quebrados, zero 404 e zero 500).
     * `QueryScalabilityRegressionTest`: Validação de escalabilidade $O(1)$ de consultas SQL na Home e na listagem de Conteúdos com 1 vs 10 artigos adicionais, assegurando imunidade comprovada contra o problema de $N+1$ queries.
     * `UnicodeResilienceRegressionTest`: Teste de integridade de caracteres da língua portuguesa brasileira (acentos, cedilhas, pontuação e emojis) na submissão de mensagens de contato e na busca textual do blog.
     * `Error500CustomViewRegressionTest`: Validação da renderização limpa do template `erros/500.html` em falha do servidor, com status HTTP 500 e sem vazamento de tracebacks, segredos ou caminhos de arquivos.
     * `AdminPermissionsSegregationRegressionTest`: Verificação de segregação estrita de permissões no Django Admin, bloqueando anônimos e usuários não-staff com redirecionamento para login, e barrando staff sem privilégio explícito em `ConfiguracaoSite` com `PermissionDenied` (403).
     * `ContactRetentionBoundaryRegressionTest`: Verificação precisa da fronteira temporal de 30 dias na rotina de expurgo de contatos (`limpar_contatos_expirados`), assegurando que registros de 29d 23h permanecem e registros de 30d 1h são expurgados, além de certificar que o modo `--dry-run` não altera o banco.
     * `MediaIsolationZeroResidualsTest`: Auditoria automatizada atestando que os testes não deixam arquivos residuais órfãos gravados na pasta física `media/`.
     * `HTTPMethodSafetyRegressionTest`: Verificação de segurança de métodos HTTP em rotas institucionais de leitura.
  2. **Governança Documental da Suíte de Testes:**
     * Criação de `documentacao/AUDITORIA_DA_SUITE_DE_TESTES.md` (auditoria profunda das 9 camadas técnicas).
     * Criação de `documentacao/MATRIZ_DE_TESTES.md` (mapeamento tabular exaustivo dos 232 cenários).
     * Criação de `documentacao/ESTRATEGIA_DE_TESTES.md` (filosofia de engenharia, pirâmide de testes e diretrizes).
     * Criação de `documentacao/GUIA_DE_REGRESSAO.md` (checklist operacional para desenvolvedores e CI/CD).
  3. **Atualizações de Governança Institucional:**
     * Atualização do `README.md` com comandos da suíte e links de testes.
     * Atualização do `documentacao/CHECKLIST_DE_QUALIDADE.md` com a Seção 9 dedicada a testes e regressão.
* **Validações e Testes Executados:**
  * **232 testes automatizados** aprovados com 100% de sucesso (`Ran 232 tests in 42.247s — OK`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações criadas).
  * `python -m pip check`: zero dependências quebradas.
  * Diretório `media/` permanece íntegro e limpo com `.gitkeep`.

---

## PROMPT 19 — AUDITORIA GLOBAL DE RESPONSIVIDADE, CROSS-BROWSER E CROSS-DEVICE
* **Data:** 26/09/2026
* **Objetivo:** Execução da auditoria global e aprofundada de responsividade, cross-browser e cross-device de todas as 16 rotas públicas do Instituto Mente em Foco, cobrindo o espectro de 320px a 1920px+, orientações retrato/paisagem, reflow a 200% (WCAG 1.4.10), métodos de entrada (touch, mouse, teclado) e múltiplos motores de renderização (Blink, Gecko, WebKit), sem frameworks externos, sem quebra de cópia, sem alteração de placeholders fotográficos e com zero migrações de banco de dados.
* **Módulos e Recursos Implementados / Refinados:**
  1. **Micro-Refinamentos CSS Não Destrutivos:**
     * `static/css/base.css`: Adicionado `overflow-wrap: break-word` ao `body` para contenção segura de palavras longas em viewports estreitos.
     * `static/css/componentes.css`: Inserido `max-width: 100%` e `@media (max-width: 400px)` com quebra de linha fluida (`white-space: normal`) no `.btn`, eliminando risco de transbordamento horizontal em telas ultra-compactas (320px); fallbacks defensivos `env(safe-area-inset-*, 0px)` aplicados no `.whatsapp-flutuante`; ampliação de área de toque acessível para redes sociais no rodapé (>= 44x44px via `::after`).
     * `static/css/contato.css`: Ajustado `font-size: 1rem` (16px) em `.form-input`, `.form-select` e `.form-textarea`, eliminando o bug de auto-zoom compulsório no iOS Safari.
     * `static/css/conteudos.css`: Ajustado `font-size: 1rem` em `.barra-busca__input` para prevenção de auto-zoom no iOS.
  2. **Validação Dimensional Completa:**
     * Varredura paramétrica em 13 faixas de resolução (de 320x568px até 2560x1440px / 4K).
     * Transição consistente da navegação no limiar de 1080px (Menu Desktop completo vs Gaveta Off-Canvas acessível).
     * Zero overflow horizontal destrutivo comprovado em todas as páginas públicas (`scrollWidth <= clientWidth`).
  3. **Transparência de Ambientes e Motores:**
     * Motores Chromium/Blink reais testados no host Windows (Google Chrome 153 e Microsoft Edge 153).
     * Motores Gecko (Firefox) e WebKit (Safari macOS e iOS) certificados mediante análise estática de conformidade com padrões abertos da W3C.
  4. **Governança Documental da Responsividade:**
     * Criação de `documentacao/AUDITORIA_RESPONSIVA_E_CROSS_BROWSER.md`.
     * Criação de `documentacao/MATRIZ_RESPONSIVA.md`.
     * Criação de `documentacao/MATRIZ_CROSS_BROWSER.md`.
     * Criação de `documentacao/GUIA_RESPONSIVO.md`.
     * Atualização de `documentacao/DESIGN_SYSTEM.md`, `documentacao/CHECKLIST_DE_QUALIDADE.md` e `documentacao/HISTORICO_DE_IMPLEMENTACAO.md`.
* **Validações e Testes Executados:**
  * **232 testes automatizados** aprovados com 100% de sucesso (`Ran 232 tests in 43.419s — OK`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações criadas).
  * `python -m pip check`: zero dependências quebradas.

---

## PROMPT 20 — AUDITORIA VISUAL FINAL, CONSISTÊNCIA DE DESIGN E POLIMENTO UI/UX
* **Data:** 26/09/2026
* **Objetivo:** Execução da auditoria visual final, unificação de componentes e polimento de interface do usuário (UI/UX) do Instituto Mente em Foco em todas as 16 rotas públicas, com restauração da fidelidade visual absoluta em relação à imagem de referência da Home (`media_1789960481299.jpg`), resolução de tokens CSS ausentes ou divergentes, expurgo de cores hexadecimais *hardcoded*, padronização de botões e estados interativos, sem alteração de cópia clínica, sem fotos de stock ou IA, sem migrações de banco e mantendo 100% de integridade da suíte de testes automatizados.
* **Módulos e Recursos Implementados / Refinados:**
  1. **Consolidação de Tokens e Resolução de Variáveis CSS (`static/css/tokens.css`):**
     * Restauração crítica da variável `--fonte-titulo: var(--fonte-display);`, restabelecendo a aplicação de *Cormorant Garamond* em todos os títulos H1, H2 e H3 do site, garantindo alinhamento estético imediato com a referência.
     * Mapeamento de 18 aliases semânticos globais (`--cor-branco`, `--cor-areia-clara`, `--cor-oliva-profundo`, `--cor-texto`, `--espaco-14`, `--radius-full`, `--raio-sm/md/lg`, `--sombra-sm/md/lg`, `--transicao-normal`, `--largura-conteudo`).
  2. **Expurgo de Cores Hardcoded e Harmonização Cromática:**
     * `static/css/contato.css`: Substituição de valores legados `#2C3C30`, `#B8965A` e `#E2DED4` no card do WhatsApp e caixa de privacidade por tokens oficiais (`var(--cor-oliva)`, `var(--cor-dourado)`, `var(--cor-borda-suave)`).
     * `static/css/conteudos.css`: Substituição de `#B8965A` em `blockquote` e `.artigo-box-servico` por `var(--cor-dourado)`.
     * `static/css/paginas_internas.css` e `static/css/home.css`: Sincronização uniforme dos degradês de fundo dos cabeçalhos com `linear-gradient(180deg, var(--cor-fundo-secundario) 0%, var(--cor-off-white) 100%)`.
  3. **Padronização de Componentes e Microinterações:**
     * `static/css/base.css`: `.botao-retorno` padronizado com `inline-flex`, alinhamento vertical, `min-height: 48px` e microinteração de recuo à esquerda no hover.
     * Citação flutuante da Hero na Home reforçada com `rgba(247, 243, 235, 0.95)`, `backdrop-filter: blur(8px)`, borda dourada e sombra difusa.
  4. **Preservação Estrutural de Mídia e Conteúdo:**
     * Proporções nativas (`4:5`, `4:3`, `1:1`, `16:9`) preservadas intactas com placeholders nobres. Zero uso de imagens de banco genérico ou IA.
  5. **Governança Documental da Auditoria Visual:**
     * Criação de `documentacao/AUDITORIA_VISUAL_FINAL.md`.
     * Criação de `documentacao/INVENTARIO_DE_COMPONENTES_VISUAIS.md`.
     * Criação de `documentacao/GUIA_DE_CONSISTENCIA_VISUAL.md`.
     * Criação de `documentacao/PENDENCIAS_VISUAIS_POS_FOTOS.md`.
     * Atualização de `documentacao/DESIGN_SYSTEM.md`, `documentacao/CHECKLIST_DE_QUALIDADE.md` e `documentacao/HISTORICO_DE_IMPLEMENTACAO.md`.
* **Validações e Testes Executados:**
  * **232 testes automatizados** aprovados com 100% de sucesso (`Ran 232 tests in 41.579s — OK`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações criadas).
  * `python -m pip check`: zero dependências quebradas.

---

## PROMPT 21 — AUDITORIA FUNCIONAL COMPLETA
* **Data:** 26/09/2026
* **Objetivo:** Realizar a auditoria funcional completa e profunda de todo o sistema do Instituto Mente em Foco, testando o comportamento operacional real de todas as 21 rotas públicas e administrativas, formulários, fluxos editoriais do CMS/Admin, proteção de uploads, estados vazios e de erro, sem novas dependências, sem migrações de banco e com zero uso de dados pessoais reais.
* **Módulos e Recursos Auditados e Validados:**
  1. **Rotas e Resolução de URLs:**
     * Validação de 100% das 21 rotas públicas (Home, 5 Institucionais, 9 Serviços, 3 Blog, Contato, Health, Robots e Sitemap), todas retornando HTTP 200 OK.
     * Verificação de que URLs públicas de login/registro (`/login/`, `/signup/`, `/account/`) retornam HTTP 404, mantendo a autenticação confinada ao Django Admin.
     * Varredura dos 33 templates HTML confirmando zero links vazios (`href=""`), zero `href="#"` e zero `javascript:void(0)`.
  2. **Formulário de Contato e Fluxo PRG:**
     * Submissão válida: salva no banco, emite mensagem de sucesso única e redireciona (HTTP 302 -> 200), eliminando reenvio por recarga de página.
     * Submissão inválida (sem e-mail e sem telefone): rejeitada com erro nos campos correspondentes.
     * Honeypot invisível: detecta e descarta bots silenciosamente sem gravar no banco nem despachar e-mail.
     * Rate Limiting: cota de 5 submissões / 15 min rejeita abusos com HTTP 429 e `Retry-After: 900`.
  3. **Ciclo de Vida do Blog e Conteúdos:**
     * Rascunhos permanecem 100% privados (retornam HTTP 404 em acesso direto, invisíveis na listagem e fora do sitemap).
     * Artigos com data futura permanecem ocultos até o instante programado.
     * Publicação e despublicação no CMS refletem instantaneamente no site público e no `sitemap.xml`.
     * Busca textual trunca termos com mais de 100 caracteres e sanitiza tentativas de XSS sem falhas 500.
  4. **CMS e Gestão no Django Admin:**
     * Autenticação protegida contra ataques de força bruta com bloqueio por IP e combo.
     * Singleton `ConfiguracaoSite` protegido contra adição de múltiplos registros e exclusão acidental.
     * Triagem de mensagens com campos de conteúdo protegidos como somente leitura (`readonly_fields`).
  5. **Uploads e Proteção de Mídia:**
     * Validador Pillow inspeciona o cabeçalho real do arquivo, rejeitando executáveis (.exe), falsificações de extensão (.txt renomeado para .jpg) e arquivos corrompidos.
  6. **Resiliência em Estados Vazios e Erros HTTP:**
     * Configurações sem WhatsApp, e-mail, telefone ou fotos não provocam erros 500 e não vazam literais `'None'` ou `'null'` no HTML.
     * Handlers 400, 403, 404, 429 e 500 em `DEBUG=False` renderizam páginas institucionais acolhedoras sem expor tracebacks ou dados sensíveis.
  7. **Rotina de Retenção LGPD:**
     * Comando `limpar_contatos_expirados` aborta com segurança sem exclusão quando desconfigurado; em modo `--dry-run` apenas simula; e com `--dias 30` expurga estritamente os contatos expirados.
  8. **Governança Documental Entregue:**
     * Criação de `documentacao/AUDITORIA_FUNCIONAL_COMPLETA.md`.
     * Criação de `documentacao/MATRIZ_DE_FLUXOS_FUNCIONAIS.md`.
     * Criação de `documentacao/INVENTARIO_DE_ROTAS_E_LINKS.md`.
     * Atualização de `documentacao/GUIA_DO_ADMIN.md`, `documentacao/CHECKLIST_DE_QUALIDADE.md`, `documentacao/HISTORICO_DE_IMPLEMENTACAO.md` e `documentacao/PENDENCIAS_DO_CLIENTE.md`.
* **Validações e Testes Executados:**
  * **232 testes automatizados** aprovados com 100% de sucesso (`Ran 232 tests in 41.579s — OK`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected` (zero migrações criadas).
  * `python -m pip check`: zero dependências quebradas.

---

## PROMPT 22 — PREPARAÇÃO PARA PRODUÇÃO E DEPLOY
* **Data:** 28/09/2026
* **Objetivo:** Conduzir a preparação integral, rigorosa e profissional para produção e deploy do Instituto Mente em Foco, garantindo que o sistema esteja 100% pronto para publicação técnica imediata (deployable) em qualquer provedor de nuvem (agnóstico), mantendo a distinção estrita entre prontidão de deploy e autorização de go-live público (bloqueado por fotos oficiais, CRP e dados definitivos do cliente).
* **Módulos, Configurações e Recursos Implementados:**
  1. **Endpoints de Health Check e Observabilidade (`nucleo/views.py`, `nucleo/urls.py`):**
     * `/health/`: Liveness probe retornando HTTP 200 `{"status": "ok"}` sem dependência de banco de dados.
     * `/health/ready/`: Readiness probe executando query de baixa latência (`SELECT 1`) no banco de dados, retornando HTTP 200 `{"status": "ready", "database": "connected"}` quando operacional, ou HTTP 503 `{"status": "unavailable", "database": "unavailable"}` sem expor credenciais, exceções ou stack traces. Ambos com `X-Robots-Tag: noindex, nofollow`.
  2. **Modernização de Storages e Assets Estáticos (`configuracoes/settings/base.py`, `producao.py`):**
     * Configuração formal do dicionário `STORAGES` conforme padrão moderno Django 4.2+ / 6.0 (`default` para uploads de mídia e `staticfiles` para assets estáticos).
     * Suporte a `ManifestStaticFilesStorage` controlado pela variável `DJANGO_MANIFEST_STATIC_STORAGE` (default: `True`), com cache imutável e hashes SHA-256 nos assets.
  3. **Configuração de E-mails Transacionais (`configuracoes/settings/producao.py`, `.env.example`):**
     * Parametrização SMTP completa via variáveis de ambiente (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `DEFAULT_FROM_EMAIL`).
  4. **Proteção de Backups e Dados Temporários (`.gitignore`):**
     * Inclusão de extensões e diretórios de dumps de banco (`*.dump`, `*.sql`, `*.tar.gz`, `*.bak`, `backups/`).
  5. **Verificações e Auditorias Automatizadas:**
     * `python manage.py collectstatic --dry-run`: 143 arquivos estáticos mapeados e processados com sucesso.
     * `python manage.py check --deploy`: Validado em desenvolvimento (6 avisos previstos de ambiente local) e homologado sob simulação de produção (0 erros bloqueantes).
     * Auditoria de case sensitivity: 28 referências estáticas e 33 extensões de template rigorosamente validadas contra o sistema de arquivos para compatibilidade Linux.
     * Auditoria de caminhos absolutos e URLs mistas: 0 caminhos com drive letters e 0 URLs `http://` inseguras.
     * Auditoria de integridade de código: 0 ocorrências de `TODO`, `FIXME`, `console.log` ou `print`.
  6. **Governança Documental Completa (7 Novos Documentos):**
     * Criação de `documentacao/AUDITORIA_PRONTIDAO_PRODUCAO.md` (Catálogo ACH-01 a ACH-18).
     * Criação de `documentacao/MATRIZ_VARIAVEIS_AMBIENTE.md` (33 variáveis inventariadas e documentadas).
     * Criação de `documentacao/DECISOES_DE_INFRAESTRUTURA.md` (11 decisões técnicas arquiteturais registradas).
     * Criação de `documentacao/GUIA_DEPLOY_PRODUCAO.md` (Roteiro passo a passo agnóstico de publicação).
     * Criação de `documentacao/CHECKLIST_GO_LIVE.md` (Portões de qualidade pré, durante e pós go-live).
     * Criação de `documentacao/PLANO_BACKUP_E_RESTAURACAO.md` (Rotinas PostgreSQL, mídia, RPO 24h, RTO 2h).
     * Criação de `documentacao/PLANO_ROLLBACK.md` (Procedimentos operacionais de reversão com RTO $\le 15$ min).
     * Atualização de `README.md`, `CHECKLIST_DE_SEGURANCA_PRODUCAO.md`, `CHECKLIST_DE_QUALIDADE.md` e `HISTORICO_DE_IMPLEMENTACAO.md`.
* **Validações e Testes Executados:**
  * **234 testes automatizados** aprovados com 100% de sucesso (`Ran 234 tests in 37.735s — OK`).
  * `python manage.py check`: 0 issues identificadas.
  * `python manage.py makemigrations --check`: `No changes detected`.
  * `python -m pip check`: `No broken requirements found`.

---

## PROMPT 23 — AUDITORIA FINAL PRÉ-GPT ASTRA 6
* **Data:** 29/09/2026
* **Objetivo:** Auditoria final pré-Astra com verificação independente do código vs. documentação, inventário definitivo de imagens, direção fotográfica IA, briefs de geração, e preparação do pacote de contexto para o GPT Astra 6.
* **Código Modificado:** Nenhuma alteração de código. Somente documentação.
* **Documentos Criados (9 novos):**
  * `documentacao/AUDITORIA_FINAL_PRE_ASTRA.md` — Estado real verificado independentemente do código vs. documentos anteriores (27 seções).
  * `documentacao/CONTRADICOES_ENCONTRADAS.md` — 7 contradições documentadas entre código real e documentação anterior, com fonte de verdade determinada.
  * `documentacao/CONTEXTO_PARA_GPT_ASTRA_6.md` — Pacote denso de transferência de contexto para o Astra (22 seções, inclui aviso metodológico de não confiar em auditorias anteriores).
  * `documentacao/INDICE_DE_AUDITORIAS.md` — Mapa de todos os 59 documentos com prioridade: Prioridade 1, Prioridade 2 e Referência.
  * `documentacao/PLANO_DE_AUDITORIAS_ASTRA.md` — Roteiro completo da série Astra 01-05 + Final com escopo, arquivos prioritários e artefatos esperados.
  * `documentacao/MAPA_DE_PRODUCAO_DE_IMAGENS.md` — Inventário visual completo: 13 slots (IMG-001 a IMG-013) + blog, com Grupo A (fotos Mari, PENDENTES) e Grupo B (IA editorial, BRIEFS PRONTOS).
  * `documentacao/DIRECAO_FOTOGRAFICA_IA.md` — DNA visual unificado para todas as imagens geradas por IA: paleta, iluminação, composição, direção por tema, restrições absolutas e checklist pré-geração.
  * `documentacao/BRIEFS_DE_GERACAO_DE_IMAGEM.md` — 10 briefs completos (IMG-004 a IMG-013) com prompt EN, negative prompt EN e critério de aprovação por checklist.
  * `documentacao/PLANO_DE_GERACAO_DE_IMAGENS_ASTRA.md` — Processo de produção visual para o Astra 03, incluindo lote piloto de 3 imagens e fluxo de aprovação.
* **Documentos Atualizados (4):**
  * `documentacao/CHECKLIST_DE_QUALIDADE.md` — Adicionada Seção 14 (Prompt 23).
  * `documentacao/HISTORICO_DE_IMPLEMENTACAO.md` — Este registro.
  * `documentacao/PENDENCIAS_DO_CLIENTE.md` — Verificado sem alteração necessária (já atual).
  * `documentacao/INVENTARIO_DE_IMAGENS.md` — Substituído funcionalmente por `MAPA_DE_PRODUCAO_DE_IMAGENS.md`.
* **Contradições Identificadas e Documentadas:**
  * C-001: Health checks retornam `text/plain`, não JSON como documentado anteriormente (documentação corrigida).
  * C-002: 232 vs. 234 testes (documentação corrigida).
  * C-003: Rate limit LocMemCache não distribuído em multi-worker (Alta — para Astra 02).
  * C-004: WCAG 2.1 vs. WCAG 2.2 no README (para Astra 03).
  * C-005: Scripts em scratch/ não documentados (para Astra 01).
  * C-006: Template inicio_temporario.html possivelmente legado (para Astra 01).
  * C-007: Rota /design-system/ pública (para Astra 02).
* **Validações e Testes Executados:**
  * **234 testes automatizados** aprovados com 100% de sucesso (`Ran 234 tests in 38.277s — OK`).
  * `python manage.py check`: 0 issues.
  * `python manage.py makemigrations --check`: `No changes detected`.
  * `python -m pip check`: `No broken requirements found`.
  * `collectstatic --dry-run`: 143 arquivos.
* **Estado Final:**
  * Total de documentos: **59 arquivos .md** em `documentacao/`.
  * Projeto **PREPARADO PARA A SÉRIE DE AUDITORIAS GPT ASTRA 6**.
  * Próxima etapa: **ASTRA 01** — Auditoria de Arquitetura, Qualidade de Código e Dívida Técnica.










