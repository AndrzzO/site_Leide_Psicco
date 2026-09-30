# CHECKLIST DE QUALIDADE PERMANENTE — INSTITUTO MENTE EM FOCO
**CRITÉRIOS DE AUDITORIA, VALIDAÇÃO TÉCNICA E HOMOLOGAÇÃO CONTÍNUA**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

---

## 1. DESIGN E FIDELIDADE VISUAL

- [x] **Fidelidade à Imagem de Referência:** A composição geral, alinhamentos, divisões de coluna e proporções reproduzem fielmente a estética e wireframe aprovado nos componentes do Design System.
- [x] **Paleta de Cores e Tokens:** Todas as cores utilizadas derivam exclusivamente dos design tokens (`--cor-areia`, `--cor-off-white`, `--cor-salvia`, `--cor-oliva`, `--cor-dourado`, `--cor-taupe`). Nenhuma cor arbitrária solta no CSS.
- [x] **Tipografia Editorial:** Fontes carregadas e aplicadas corretamente (`Cormorant Garamond` para títulos editoriais e `Montserrat` para leitura e microcopy). Hierarquia visual nítida.
- [x] **Ritmo Vertical e Espaçamento:** Áreas de respiro confortáveis (seções fluidas com clamp), transmitindo calma e sofisticação.
- [x] **Integridade de Imagens:** Todas as fotos utilizam `object-fit: cover` e possuem proporção de aspecto (*aspect ratio*) preservada sem deformações.
- [x] **Placeholders de Desenvolvimento:** Blocos de imagens não fornecidas exibem claramente a marcação temporária sem alterar a geometria do layout.
- [x] **Adaptação Mobile-First:** Experiência mobile estruturada para 320px, 360px, 390px, 430px e 768px sem rolagem horizontal indesejada e com elementos fluidos.

---

## 2. FUNCIONALIDADES E UX

- [x] **Navegação e Links:** Todos os links do Header, Footer e botões internos direcionam para as URLs corretas sem quebras ou âncoras órfãs.
- [x] **Menu Mobile:** Menu responsivo abre e fecha com fluidez, conta com botão de fechar acessível e bloqueia rolagem do fundo quando aberto.
- [x] **Integração WhatsApp:** Botão flutuante e CTAs abrem o link seguro da API do WhatsApp com o texto pré-configurado: *"Olá, Mari. Conheci o Instituto Mente em Foco pelo site e gostaria de informações sobre o atendimento psicológico/neuropsicológico."*.
- [x] **Formulário de Contato Seguro:**
  - [x] Campos restritos a Nome, Telefone/WhatsApp, E-mail, Tipo de Atendimento e Mensagem.
  - [x] Ausência total de campos invasivos (sem coleta de prontuário, diagnóstico ou dados clínicos sensíveis).
  - [x] Checkbox explícito de consentimento de privacidade presente e obrigatório.
  - [x] Validação server-side contra campos em branco ou formatos inválidos.
  - [x] Feedback visual claro de sucesso ou erro (toasts/mensagens do Django Messages Framework).
- [x] **Blog e Conteúdos:** Listagem paginada funcional, rotas de artigos amigáveis (`/conteudos/<slug>/`), contagem estimada de leitura e compartilhamento social limpo.
- [x] **Django Admin / CMS:** Painel administrativo customizado e seguro, permitindo atualização de conteúdos, áreas, serviços e informações centrais da clínica.

---

## 3. SEO E INDEXAÇÃO

- [x] **Titles Personalizados:** Cada página possui um `<title>` exclusivo, conciso e com a assinatura institucional (validado na Home e nas 5 páginas do Eixo Psicologia).
- [x] **Meta Descriptions Únicas:** Resumos acolhedores e éticos com meta descriptions exclusivas configuradas para as páginas implementadas.
- [x] **Headings Hierárquicos:** Exatamente uma tag `<h1>` semântica por página, com `<h2>` e `<h3>` ordenados logicamente sem saltos arbitrários.
- [x] **URLs Amigáveis:** URLs limpas em português, sem parâmetros criptografados ou extensões aparentes.
- [x] **Canonical Tags:** Tags `<link rel="canonical">` presentes em todas as páginas para evitar conteúdo duplicado.
- [x] **Open Graph & Twitter Cards:** Meta tags de compartilhamento social (og:title, og:description, og:image, og:type) configuradas e testadas.
- [x] **Sitemap e Robots:** Arquivos `/sitemap.xml` dinâmico e `/robots.txt` devidamente configurados e servidos com governança de ambiente.
- [x] **Dados Estruturados (JSON-LD):** Schemas `Organization`, `Person`, `Service`, `BlogPosting` e `BreadcrumbList` implementados com escape seguro anti-XSS.

### 3.1 SEO Editorial e On-Page (Prompt 13)
- [x] **H1 Canônico Único:** 100% das 16 URLs públicas renderizam estritamente 1 tag `<h1>`.
- [x] **Hierarquia de Headings Fluida:** `<h2>` para seções temáticas e `<h3>` para subdivisões/cartões, sem saltos arbitrários.
- [x] **Padronização de Titles:** Títulos uniformizados no padrão `[Nome da Página] | Instituto Mente em Foco`.
- [x] **Meta Descriptions Éticas:** Resumos factuais e acolhedores sem promessas sensacionalistas de cura ou diagnósticos precipitados.
- [x] **Zero Páginas Órfãs:** Todas as páginas possuem múltiplos links de entrada e saída.
- [x] **Interlinking Contextual:** Conexões naturais e bidirecionais entre serviços correlatos com textos-âncora explicativos.
- [x] **Prevenção de Canibalização:** Demarcação clara das intenções de cada URL (*Psicologia* vs *Traumas*, *Separação* vs *Novos Relacionamentos*, *Neuropsicologia* vs *Avaliação Neuropsicológica*).
- [x] **Controle de Rascunhos:** Artigos em rascunho ou agendados são excluídos das listagens públicas e do sitemap.
- [x] **Governança Documental:** 4 novos documentos de governança criados (`AUDITORIA_SEO_EDITORIAL.md`, `MAPA_DE_INTENCOES_SEO.md`, `MAPA_DE_LINKS_INTERNOS.md`, `PENDENCIAS_EDITORIAIS.md`).

---

## 4. ACESSIBILIDADE DIGITAL (WCAG 2.2 AA — PROMPT 14)

- [x] **HTML5 Semântico First:** Uso prioritário de tags nativas (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<table>`). Remoção de roles ARIA redundantes (`role="banner"`, `role="main"`, `role="contentinfo"`).
- [x] **Skip Link Funcional:** Link `.skip-link` visível em foco no topo da tela, direcionando para `<main id="conteudo-principal" tabindex="-1">` com transferência programática de foco.
- [x] **Navegação Exclusiva por Teclado:** 100% dos controles acessíveis via `Tab`, `Shift+Tab`, `Enter`, `Space` e `Escape`.
- [x] **Indicador de Foco Visível Reforçado:** `:focus-visible` com espessura de 2px sólida em verde oliva, offset de 3px e curvatura suave, sem bloqueio de foco.
- [x] **Foco Não Obscurecido (Critério 2.4.11):** `scroll-margin-top: 96px;` em elementos com ID, inputs e âncoras para evitar que o header fixo cubra elementos focados.
- [x] **Menu Mobile com Focus Trap:** Drawer mobile aprisiona o foco em ciclo de tabulação enquanto aberto, fecha com `Escape` e devolve o foco imediatamente ao botão disparador (`toggleBtn`).
- [x] **Diferenciação de Múltiplos `<nav>`:** Todos os blocos de navegação (principal, móvel, breadcrumbs, chips de categoria, paginação, rodapé institucional e rodapé de especialidades) possuem atributos `aria-label` descritivos e exclusivos.
- [x] **Contraste de Cores Calibrado:** Ratio $\ge 4.5:1$ para textos normais e $\ge 3:1$ para botões e componentes de interface. Token `--cor-texto-suave` calibrado para `#6E675E` (5.01:1). Cor dourada restrita estritamente a elementos gráficos decorativos.
- [x] **Formulários Acessíveis e Prevenção de Erros:**
  - [x] 100% dos inputs com `<label for="...">` correspondente.
  - [x] Legenda textual explícita de campos obrigatórios (`.form-legenda-obrigatorio`).
  - [x] Injeção dinâmica de `aria-invalid="true"` e `aria-describedby` nos campos com erro.
  - [x] Sumário acessível de erros no topo com `role="alert"` e links para ancoragem.
  - [x] Blindagem absoluta do honeypot contra tecnologias assistivas (`aria-hidden="true"`, `tabindex="-1"`).
- [x] **Acessibilidade de Mídias e SVGs:** 100% das imagens possuem atributo `alt`; ícones e vetores decorativos possuem `aria-hidden="true"` e `focusable="false"`.
- [x] **Tabelas de Dados Acessíveis:** Tabela de cookies com `<caption>`, cabeçalhos `<th scope="col">` e sem roles redundantes.
- [x] **Paginação do Blog Acessível:** Link da página ativa marcado com `aria-current="page"` e páginas numéricas com rótulos `aria-label`.
- [x] **Movimento Reduzido (Sensibilidade Vestibular):** Suporte global a `@media (prefers-reduced-motion: reduce)` anulando durações de animações e transições.
- [x] **Reflow a 320px e Zoom a 200%:** Interface fluida sem rolagem horizontal ou sobreposição de texto em viewport de 320px e ampliação de 200%.

---

## 5. SEGURANÇA E HARDENING DE PRODUÇÃO (PROMPT 16)

- [x] **Variáveis de Ambiente:** Nenhuma chave (`SECRET_KEY`, senha de e-mail, senhas de banco) exposta no código-fonte ou versionada no Git.
- [x] **Modo Produção:** `DEBUG = False` rigorosamente garantido em `configuracoes/settings/producao.py`, com validação fail-closed.
- [x] **ALLOWED_HOSTS Estrito:** Configuração obrigatória sem wildcard `*` em produção, validando nomes de domínio oficiais.
- [x] **Proteção CSRF:** Tag `{% csrf_token %}` em 100% dos formulários POST; zero `@csrf_exempt` em todo o código; falhas tratadas sem vazamento.
- [x] **Headers de Segurança Modernos:**
  - `X-Frame-Options: DENY` (anti-clickjacking).
  - `X-Content-Type-Options: nosniff` (anti-MIME sniffing).
  - `Referrer-Policy: strict-origin-when-cross-origin`.
  - `Cross-Origin-Opener-Policy: same-origin` (COOP ativo nativamente).
  - `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()` via `SecurityHeadersMiddleware`.
- [x] **Content Security Policy (CSP Nativa Django 6.0):** Implementada via `ContentSecurityPolicyMiddleware`, restringindo scripts a `'self'` e nonces criptográficos, estilos controlados, fontes do Google Fonts e objetos bloqueados (`object-src 'none'`).
- [x] **HTTPS e Cookies Seguros:** `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'` em produção.
- [x] **HSTS Progressivo:** Rollout seguro parametrizado (`0` pré-deploy, plano de 300s -> 86400s -> 31536000s) sem ativação precipitada de preload.
- [x] **Segurança de Uploads:** Validação de cabeçalho binário real com Pillow (`Image.open().verify()`), teto estrito de 10 MB, nomes UUID imprevisíveis e proibição de executáveis/SVG arbitrário.
- [x] **Proteção de Dados Pessoais (LGPD / PII):** View de contato blindada com `@sensitive_post_parameters('nome', 'email', 'telefone', 'mensagem')` para mascarar dados em relatórios de erro.
- [x] **Django Admin Fortalecido:** Senhas com comprimento mínimo reforçado para 12 caracteres (`MinimumLengthValidator`), rota administrativa fora de sitemap/robots, mensagens em modo `readonly`.
- [x] **Páginas de Erro Resilientes:** 400, 403, 404 e 500 customizadas e sem vazamento de traceback ou caminhos do servidor.
- [x] **Testes Automatizados de Segurança:** 23 testes em `nucleo/tests_seguranca.py` (total de 198 testes na suíte geral).


---

## 6. PERFORMANCE E CORE WEB VITALS (PROMPT 15)

- [x] **Infraestrutura Preparada para Fotos:** Mapeamento completo dos 28 slots com aspect-ratio, dimensões ideais e orientações no inventário. Placeholders mantidos sem alteração de layout enquanto as fotos definitivas são aguardadas.
- [x] **Carregamento Priorizado (LCP):** Imagens do topo da dobra e Hero utilizam `loading="eager"`, `fetchpriority="high"` e `decoding="async"`.
- [x] **Carregamento Diferido (Lazy Loading):** Imagens abaixo da dobra utilizam `loading="lazy"` e `decoding="async"`.
- [x] **Estabilidade Dimensional (CLS = 0):** Containers CSS utilizam `aspect-ratio` nativo (`.ratio-4-5`, `.ratio-16-9`, `.ratio-4-3`), reservando o espaço dimensional prévio.
- [x] **CSS Modular e Enxuto:** Arquitetura CSS pura sem `@import`, sem frameworks pesados, sem `@keyframes` excessivos e com animações neutralizadas sob `prefers-reduced-motion`.
- [x] **JavaScript Não-Bloqueante:** 100% dos scripts (`base.js`, `navegacao.js`, `home.js`) utilizam `defer`. Apenas 6.3 KB de JS total no projeto.
- [x] **Otimização de Fontes:** Google Fonts com pré-conexão dupla (`fonts.googleapis.com` e `fonts.gstatic.com` com `crossorigin`) e `display=swap`.
- [x] **Otimização de Consultas SQL:** Prevenção de N+1 com `select_related('categoria', 'autor')` e eliminação de consulta duplicada em Contato (reduzido para 4 queries).
- [x] **Testes Automatizados de Performance:** 10 testes estruturais dedicados em `nucleo/tests_performance.py` garantindo tetos de queries e carregamento de assets.
- [ ] **Métricas de Campo (Field Data / CrUX):** Aguardando deploy em produção com tráfego real para coleta de telemetria RUM.

---

## 7. SEO TÉCNICO E INDEXAÇÃO CONTROLADA

- [x] **Governança de Ambientes:** `SEO_ALLOW_INDEXING=False` por padrão, com bloqueio absoluto de indexação em dev/staging e header `X-Robots-Tag: noindex, nofollow, noarchive`.
- [x] **Checks de Inicialização:** Django System Checks (`seo.E001`, `seo.E002`, `seo.W001`) impedindo ativação inadvertida de indexação com `DEBUG=True` ou com domínios locais.
- [x] **Robots.txt Dinâmico:** `/robots.txt` sem expor a rota administrativa secreta (`DJANGO_ADMIN_URL`), alternando entre `Disallow: /` e `Allow: /` + link para `sitemap.xml`.
- [x] **Sitemap.xml Dinâmico:** `/sitemap.xml` estruturado via `django.contrib.sitemaps` contendo páginas institucionais, serviços ativos, artigos publicados (sem rascunhos ou futuros) e categorias com artigos.
- [x] **Metadados Centralizados:** `<title>`, `<meta name="description">` e `<link rel="canonical">` absoluto em todas as páginas públicas.
- [x] **Redes Sociais:** Metadados Open Graph e Twitter Cards (`summary_large_image`) configurados no `base.html`.
- [x] **Busca Interna com Noindex:** Páginas de busca (`/conteudos/?q=...`) marcadas com `noindex, follow` e canônica limpa.
- [x] **JSON-LD Seguro:** Templatetag dedicada com escape contra encerramento indevido de scripts (`</script>` -> `\u003c/script\u003e`), contendo `WebSite`, `Organization`, `Person`, `Service`, `BlogPosting` e `BreadcrumbList`.
- [x] **Ética Médica e Psicológica:** Ausência total de dados fictícios, notas/estrelas fabricadas (`AggregateRating`) ou avaliações inventadas.

---

## 8. PROTEÇÃO CONTRA ABUSO, RATE LIMITING E DoS LÓGICO (PROMPT 17)

- [x] **Zero Rate Limit Global:** Navegação humana normal (Home, Sobre Mim, Serviços, Artigos), assets estáticos (CSS, JS, imagens) e rotas de SEO (`robots.txt`, `sitemap.xml`) nunca sofrem limitação.
- [x] **Rate Limit no Formulário de Contato:** Cota de 5 submissões a cada 15 minutos por origem pseudonimizada, retornando HTTP 429 com `Retry-After: 900` e `Cache-Control: no-store`. Submissões bloqueadas não gravam no banco nem disparam e-mails.
- [x] **Honeypot Ativo e Invisível:** Campo `campo_verificacao` intercepta bots sem poluir o banco de dados e sem despachar mensagens SMTP.
- [x] **Proteção contra Brute Force no Django Admin:** Rate limit em duas camadas: Origem (10 falhas/15 min) e Combo Origem+Username (5 falhas/15 min). Rejeição imediata com HTTP 429 antes da computação de hashing PBKDF2 (mitigação de DoS de CPU).
- [x] **Prevenção de Account Lockout DoS:** O bloqueio não é global por usuário; apenas o IP atacante é temporariamente bloqueado, permitindo que administradores legítimos acessem o painel normalmente de suas redes.
- [x] **Prevenção de Username Enumeration:** Mensagens genéricas e tempo de processamento idêntico tanto para usuários existentes quanto inexistentes.
- [x] **Anti-Spoofing de IP:** Resolução de cliente via `REMOTE_ADDR` por padrão estrito. Rejeição de `HTTP_X_FORWARDED_FOR` falsificado quando `TRUST_PROXY_CLIENT_IP=False`.
- [x] **Privacidade e LGPD:** Chaves de rate limit pseudonimizadas através de HMAC-SHA256 com a chave privada da aplicação (`SECRET_KEY`). Nenhum IP ou username em texto puro em cache, banco ou logs.
- [x] **Resiliência Fail-Open:** Falhas no backend de cache resultam em permissão da requisição acompanhada de log de warning sem PII, impedindo erros 500 indevidos.
- [x] **Hardening de Busca e Paginação:** Termo de busca `q` truncado em 100 caracteres; higienização estrita de inteiros no parâmetro `page`.
- [x] **Template 429 Acessível e Responsivo:** Template semântico [`templates/erros/429.html`](file:///c:/Users/andre/Documents/SiteDjangoLeide/templates/erros/429.html) testado em 320px, 390px e 1440px com preservação de cabeçalhos de segurança (CSP, nosniff, X-Frame-Options).
- [x] **Suíte de Testes Automatizados:** 21 novos testes em `nucleo/tests_rate_limit.py`, totalizando **219 testes** no projeto com 100% de aprovação.

---

## 9. SUÍTE COMPLETA DE TESTES AUTOMATIZADOS E PREVENÇÃO DE REGRESSÃO (PROMPT 18)

- [x] **Suíte Consolidada e 100% Aprovada:** Total de **232 testes automatizados** cobrindo todas as camadas da aplicação (Models, Forms, Views, URLs, Admin, Contato, Blog, SEO, Privacidade, Segurança, Rate Limit, Uploads, Erros, Acessibilidade e Performance).
- [x] **Zero Vanity Coverage:** Testes focados estritamente em contratos, comportamento real, resiliência e prevenção de regressão. Rejeição de testes superficiais ou inúteis.
- [x] **Zero Pessoas Reais / Zero Dados Reais:** Todos os dados de teste utilizam entidades sintéticas e fictícias (`exemplo.com.br`, telefones e nomes de amostra).
- [x] **Zero Chamadas Externas de Rede:** Nenhuma dependência externa ao vivo; integração com e-mail via `locmem` e cache isolado em memória.
- [x] **Link Crawler Global:** Varredura automatizada de todas as páginas públicas e seus links internos, confirmando **zero links quebrados (zero 404 e zero 500)**.
- [x] **Escalabilidade O(1) de Consultas SQL:** Garantia comprovada de imunidade contra regressão N+1 (queries na Home e na listagem de conteúdos mantêm-se constantes com 1 ou 10 artigos adicionais).
- [x] **Resiliência UTF-8 em Contato e Busca:** Submissões e pesquisas com acentuação da língua portuguesa e emojis são processadas e persistidas sem corrupção.
- [x] **Página de Erro 500 sem Vazamentos:** Template de erro 500 renderiza visual acolhedor e seguro sem expor tracebacks, caminhos físicos ou segredos de ambiente.
- [x] **Privilégio Mínimo e Segregação de Permissões no Admin:** Usuários anônimos e não-staff são barrados no painel administrativo; membros de staff sem permissão explícita não acessam configurações centrais.
- [x] **Fronteira Temporal LGPD (30 Dias):** Validação milimétrica do comando de retenção (29d 23h preservado; 30d 1h expurgado; modo `--dry-run` não altera dados).
- [x] **Isolamento de Mídia:** Diretório `media/` permanece íntegro com zero arquivos residuais deixados pela execução dos testes.
- [x] **Zero Migrações Pendentes:** `python manage.py makemigrations --check` atesta modelo de banco perfeitamente sincronizado.
- [x] **Governança Documental Completa:** Criação de `AUDITORIA_DA_SUITE_DE_TESTES.md`, `MATRIZ_DE_TESTES.md`, `ESTRATEGIA_DE_TESTES.md` e `GUIA_DE_REGRESSAO.md`.

---

## 10. AUDITORIA GLOBAL DE RESPONSIVIDADE, CROSS-BROWSER E CROSS-DEVICE (PROMPT 19)

- [x] **Auditoria Dimensional Plena (320px a 1920px+):** Todas as 16 rotas públicas testadas e estáveis em 13 faixas de resolução (desde o iPhone SE de 320px até telas 2K/4K).
- [x] **Zero Transbordamento Horizontal (Scroll Destrutivo):** Garantia estrita de `scrollWidth <= clientWidth` em 100% das páginas, sem máscaras artificiais no `body`.
- [x] **Navegação Desktop vs Gaveta Mobile:** Limiar perfeito em 1080px com fechamento automático no redimensionamento, foco controlado via Focus Trap, tecla Escape e bloqueio de rolagem do body.
- [x] **Touch Targets Conformes (WCAG 2.5.8):** Todos os elementos interativos possuem área de toque mínima cravada em 44x44px ou 48x48px.
- [x] **Prevenção de Auto-Zoom no iOS WebKit:** Todos os campos de formulário e barras de busca possuem `font-size: 1rem` (16px), eliminando o zoom compulsório no Safari móvel.
- [x] **Safe Area Insets Defensivos:** Fallbacks seguros `env(..., 0px)` aplicados em botões flutuantes para compatibilidade com telas com entalhes e gestos.
- [x] **Reflow a 200% (WCAG 1.4.10):** Layout reorganiza-se sem quebras ou colisões sob zoom de 200% do navegador.
- [x] **Transparência de Ambientes:** Testes executados em navegadores reais locais (Chrome 153 e Edge 153) e documentação transparente de conformidade W3C para Firefox (Gecko) e Safari (WebKit).
- [x] **Preservação de Conteúdo e Placeholders:** Nenhum texto reduzido arbitrariamente; proporções estruturais de imagem mantidas intactas.
- [x] **Suíte de Testes Íntegra:** 232 testes automatizados executando com 100% de sucesso (`OK`).
- [x] **Governança Documental Específica:** Publicação de `AUDITORIA_RESPONSIVA_E_CROSS_BROWSER.md`, `MATRIZ_RESPONSIVA.md`, `MATRIZ_CROSS_BROWSER.md` e `GUIA_RESPONSIVO.md`.

---

## 11. AUDITORIA VISUAL FINAL, CONSISTÊNCIA DE DESIGN E POLIMENTO UI/UX (PROMPT 20)

- [x] **Fidelidade à Imagem de Referência:** Home 100% alinhada com a referência visual do cliente (`media_1789960481299.jpg`), cobrindo Hero assimétrico, composição de colunas, 7 cards de acolhimento e 5 áreas em linha.
- [x] **Restauração da Variável `--fonte-titulo`:** Títulos H1, H2 e H3 exibindo a família nobre *Cormorant Garamond*, eliminando fallback indevido para sans-serif.
- [x] **Zero Cores Hardcoded:** Cores hexadecimais legadas (`#2C3C30`, `#B8965A`, `#E2DED4`) substituídas pelos tokens oficiais do Design System em todas as folhas de estilo.
- [x] **Harmonização de Gradientes:** Cabeçalhos das páginas internas e do blog sincronizados com o degradê suave de `--cor-fundo-secundario` para `--cor-off-white`.
- [x] **Padronização de Botões e Ações:** `.botao-retorno` padronizado com `min-height: 48px`, alinhamento `inline-flex` e microinteração suave de recuo.
- [x] **Preservação de Placeholders e Proporções:** Proporções de imagem nativas (`4:5`, `4:3`, `1:1`, `16:9`) rigorosamente mantidas com zero stock photos ou imagens de IA gerativa.
- [x] **Zero Alterações de Modelo ou Migrações:** Banco de dados mantido intacto (`makemigrations --check` com `No changes detected`).
- [x] **Zero Novas Dependências:** Nenhuma biblioteca externa de componentes ou animações adicionada (`pip check` limpo).
- [x] **Suíte de Testes 100% Preservada:** 232 testes automatizados executando com sucesso contínuo (`Ran 232 tests ... OK`).
- [x] **Governança Documental Entregue:** Publicação de `AUDITORIA_VISUAL_FINAL.md`, `INVENTARIO_DE_COMPONENTES_VISUAIS.md`, `GUIA_DE_CONSISTENCIA_VISUAL.md` e `PENDENCIAS_VISUAIS_POS_FOTOS.md`.

---

## 12. AUDITORIA FUNCIONAL COMPLETA (PROMPT 21)

- [x] **Integridade Plena de Rotas (21/21):** 100% das rotas públicas e utilitárias respondem com HTTP 200 OK sem 500, soft-404 ou loops de redirecionamento.
- [x] **Zero Autenticação Pública Inesperada:** URLs genéricas de login e registro (`/login/`, `/signup/`, `/account/`) retornam estritamente HTTP 404, mantendo a autenticação confinada ao Django Admin.
- [x] **Fluxo PRG no Formulário de Contato:** Submissões válidas salvam dados, geram mensagem de sucesso única e redirecionam (HTTP 302 -> 200), eliminando reenvio acidental por F5.
- [x] **Validação Defensiva e Honeypot:** Submissões sem telefone e sem e-mail são rejeitadas com erro explicativo; bots que preenchem o campo invisível são descartados com segurança.
- [x] **Ciclo de Vida Editorial do Blog:** Rascunhos permanecem 100% privados (HTTP 404 em acesso direto, invisíveis na listagem e ausentes no sitemap). Publicação e despublicação no CMS refletem instantaneamente no site público.
- [x] **Segurança de Uploads:** Validador binário Pillow inspeciona o cabeçalho real do arquivo e rejeita com ValidationError arquivos não-imagem renomeados para .jpg, executáveis .exe e binários corrompidos.
- [x] **Resiliência em Estados Vazios:** Remoção simulada de WhatsApp, e-mail, telefone e fotos comprova que as páginas não quebram (zero 500) e não vazam literais `'None'` ou `'null'` no HTML.
- [x] **Páginas de Erro Seguras (DEBUG=False):** Handlers 400, 403, 404, 429 e 500 renderizam layouts institucionais acolhedores, com links de retorno à Home e zero vazamento de tracebacks ou segredos.
- [x] **Rotina de Retenção LGPD:** Comando `limpar_contatos_expirados` aborta com segurança sem exclusão quando desconfigurado; em modo `--dry-run` apenas simula; e com `--dias 30` expurga estritamente os contatos expirados.
- [x] **Governança Documental Entregue:** Publicação de `AUDITORIA_FUNCIONAL_COMPLETA.md`, `MATRIZ_DE_FLUXOS_FUNCIONAIS.md`, `INVENTARIO_DE_ROTAS_E_LINKS.md` e atualização do `GUIA_DO_ADMIN.md`.

---

## 13. PREPARAÇÃO PARA PRODUÇÃO E DEPLOY (PROMPT 22)

- [x] **Arquitetura Provider-Agnostic:** Projeto configurado para qualquer nuvem moderna (PaaS ou IaaS), sem vendor lock-in e com pendências de infraestrutura formalmente mapeadas.
- [x] **Health Checks Resilientes:** `/health/` (liveness leve) e `/health/ready/` (readiness com probe no DB via `SELECT 1`, retornando 200 ou 503 com segurança anti-leaks e `X-Robots-Tag: noindex, nofollow`).
- [x] **Suíte de Testes Expandida:** 234 testes automatizados cobrindo liveness, readiness, simulação de falha de banco e bloqueio de SECRET_KEY insegura em produção (100% de sucesso).
- [x] **Storages Modernizados:** Dicionário `STORAGES` explícito conforme padrão Django 4.2+ / 6.0, com suporte a `ManifestStaticFilesStorage` e fallback.
- [x] **Configuração SMTP Blindada:** Variáveis para e-mails transacionais adicionadas e mapeadas em `producao.py` e `.env.example`.
- [x] **Coleta de Estáticos Verificada:** `collectstatic --dry-run` validado com 143 arquivos processados com sucesso.
- [x] **Check de Deploy Homologado:** `check --deploy` executado em desenvolvimento e sob simulação de produção com zero erros bloqueantes.
- [x] **Governança Documental Completa (7 Novos Documentos):**
  - `AUDITORIA_PRONTIDAO_PRODUCAO.md` (Catálogo ACH-01 a ACH-18).
  - `MATRIZ_VARIAVEIS_AMBIENTE.md` (33 variáveis mapeadas com defaults e tipagem).
  - `DECISOES_DE_INFRAESTRUTURA.md` (11 decisões técnicas registradas).
  - `GUIA_DEPLOY_PRODUCAO.md` (Manual passo a passo agnóstico de deploy).
  - `CHECKLIST_GO_LIVE.md` (Portões de homologação e smoke tests).
  - `PLANO_BACKUP_E_RESTAURACAO.md` (Rotinas PostgreSQL, mídia, RPO 24h, RTO 2h).
  - `PLANO_ROLLBACK.md` (Procedimentos operacionais de reversão com RTO $\le 15$ min).

---

## 14. AUDITORIA FINAL PRÉ-ASTRA (PROMPT 23)

- [x] **Verificação Independente do Código:** Auditorias anteriores confrontadas com código real. Contradições registradas em `CONTRADICOES_ENCONTRADAS.md`.
- [x] **Suíte de Testes Reexecutada:** 234 testes, 100% OK (Ran 234 tests in 38.277s).
- [x] **Sistema Check Confirmado:** `python manage.py check` → 0 issues.
- [x] **Migrations Verificadas:** `makemigrations --check` → No changes detected.
- [x] **Pip Check Confirmado:** No broken requirements found.
- [x] **Collectstatic Confirmado:** 143 arquivos verificados via dry-run.
- [x] **9 Novos Documentos Criados:**
  - `AUDITORIA_FINAL_PRE_ASTRA.md` (Estado real verificado independentemente)
  - `CONTRADICOES_ENCONTRADAS.md` (7 contradições documentadas)
  - `CONTEXTO_PARA_GPT_ASTRA_6.md` (Pacote denso de transferência de contexto)
  - `INDICE_DE_AUDITORIAS.md` (Mapa de todos os 59 documentos com prioridade Astra)
  - `PLANO_DE_AUDITORIAS_ASTRA.md` (Série Astra 01-05 + Final)
  - `MAPA_DE_PRODUCAO_DE_IMAGENS.md` (Inventário visual completo: 13 slots + blog)
  - `DIRECAO_FOTOGRAFICA_IA.md` (DNA visual unificado para imagens IA)
  - `BRIEFS_DE_GERACAO_DE_IMAGEM.md` (10 briefs com prompts EN completos)
  - `PLANO_DE_GERACAO_DE_IMAGENS_ASTRA.md` (Processo de produção visual Astra 03)
- [x] **Contradição Principal Documentada:** Health checks retornam `text/plain`, não JSON como documentado anteriormente.
- [x] **Rate Limit Multi-Worker Flaggeado:** LocMemCache não distribuído — aviso para Astra 02.
- [x] **Grupo A (Fotos Mari) Formalmente Documentado:** 2 slots PENDENTES — NUNCA gerar por IA.
- [x] **Grupo B (Imagens Temáticas IA) Documentado:** Briefs prontos para 10 imagens, aguardando Astra 03.
- [x] **Total de Documentação:** 59 arquivos .md em `documentacao/`.

---
*Este checklist deve ser consultado e validado formalmente a cada entrega incremental do projeto.*


