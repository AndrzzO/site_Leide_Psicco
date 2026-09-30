# INVENTÁRIO DE ROTAS E LINKS — INSTITUTO MENTE EM FOCO
**CATÁLOGO EXAUSTIVO DE URLS, RESOLUÇÃO DE ROTAS, MÉTODOS HTTP E REGRAS DE INDEXAÇÃO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO + VANILLA JS

---

## 1. ESCOPO E ESTRUTURAÇÃO DO ROTEAMENTO

O projeto adota uma arquitetura SSR (*Server-Side Rendering*) estruturada em Django 6.0+, com separação modular de responsabilidades por aplicativo:
* `nucleo`: Rotas de governança de sistema, sitemaps, robots.txt e health check.
* `paginas`: Rotas institucionais fundamentais (Home, Sobre Mim, Políticas de Privacidade e Cookies).
* `servicos`: Rotas dedicadas aos eixos clínicos e avaliativos.
* `conteudos`: Rotas de publicação editorial do blog, listagens, categorias e artigos individuais.
* `contato`: Rota do canal de contato institucional com formulário seguro.
* `admin`: Painel de gestão do Django Admin configurável via variável de ambiente `DJANGO_ADMIN_URL`.

---

## 2. INVENTÁRIO EXAUSTIVO DE ROTAS PÚBLICAS E ADMINISTRATIVAS

| ROTA (PATH) | URL NAME (NAMESPACE:NAME) | VIEW FUNCTION / CLASS | MÉTODO HTTP | PÚBLICA? | INDEXÁVEL? (SEO) | FORM? | CMS? | AUTENTICAÇÃO? | STATUS ESPERADO |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `/` | `paginas:inicio` | `paginas.views.home` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/sobre-mim/` | `paginas:sobre_mim` | `paginas.views.sobre_mim` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/politica-de-privacidade/` | `paginas:politica_privacidade` | `paginas.views.politica_privacidade` | `GET` | **SIM** | SIM | NÃO | NÃO | NÃO | `200 OK` |
| `/privacidade/` | `paginas:privacidade` | `paginas.views.politica_privacidade` | `GET` | **SIM** | SIM (Canônica aponta p/ oficial) | NÃO | NÃO | NÃO | `200 OK` |
| `/politica-de-cookies/` | `paginas:politica_cookies` | `paginas.views.politica_cookies` | `GET` | **SIM** | SIM | NÃO | NÃO | NÃO | `200 OK` |
| `/cookies/` | `paginas:cookies` | `paginas.views.politica_cookies` | `GET` | **SIM** | SIM (Canônica aponta p/ oficial) | NÃO | NÃO | NÃO | `200 OK` |
| `/servicos/psicologia/` | `servicos:psicologia` | `servicos.views.psicologia` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/neuropsicologia/` | `servicos:neuropsicologia` | `servicos.views.neuropsicologia` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/traumas/` | `servicos:traumas` | `servicos.views.traumas` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/separacao-e-recomecos/` | `servicos:separacao_recomecos` | `servicos.views.separacao_recomecos` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/novos-relacionamentos/` | `servicos:novos_relacionamentos` | `servicos.views.novos_relacionamentos` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/avaliacao/` | `servicos:avaliacao` | `servicos.views.avaliacao` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/avaliacao-psicologica/` | `servicos:avaliacao_psicologica` | `servicos.views.avaliacao_psicologica` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/avaliacao-neuropsicologica/` | `servicos:avaliacao_neuropsicologica` | `servicos.views.avaliacao_neuropsicologica` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/servicos/reabilitacao-neurocognitiva/` | `servicos:reabilitacao_neurocognitiva` | `servicos.views.reabilitacao_neurocognitiva` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/conteudos/` | `conteudos:index` | `conteudos.views.index` | `GET` | **SIM** | SIM (sem query) / NÃO (com query `?q=`) | SIM (Busca) | SIM | NÃO | `200 OK` |
| `/conteudos/categoria/<slug>/` | `conteudos:categoria` | `conteudos.views.index` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` |
| `/conteudos/<slug>/` | `conteudos:detalhe` | `conteudos.views.detalhe` | `GET` | **SIM** | SIM (apenas publicados) | NÃO | SIM | NÃO | `200 OK` / `404 Not Found` (se rascunho) |
| `/contato/` | `contato:index` | `contato.views.index` | `GET`, `POST` | **SIM** | SIM | SIM (Contato) | SIM | NÃO | `200 OK` (GET/Erro) / `302 Found` (Sucesso) |
| `/health/` | `nucleo:health_check` | `nucleo.views.health_check` | `GET` | **SIM** | NÃO (`noindex`) | NÃO | NÃO | NÃO | `200 OK` ("OK") |
| `/robots.txt` | `robots_txt` | `nucleo.views.robots_txt` | `GET` | **SIM** | NÃO | NÃO | NÃO | NÃO | `200 OK` (`text/plain`) |
| `/sitemap.xml` | `django.contrib.sitemaps.views.sitemap` | `sitemap` | `GET` | **SIM** | SIM | NÃO | SIM | NÃO | `200 OK` (`application/xml`) |
| `/design-system/` | `paginas:laboratorio_design_system` | `paginas.views.laboratorio_design_system` | `GET` | Condicional (`DEBUG=True`) | NÃO (`noindex`) | NÃO | NÃO | NÃO | `200 OK` (em dev) / `404 Not Found` (em prod) |
| `/admin/` (configurável) | `admin:index` | `admin.site.index` | `GET` | NÃO | NÃO (`noindex`) | NÃO | SIM | **SIM (Staff)** | `302 Found` (p/ login se anônimo) / `200 OK` |
| `/admin/login/` | `admin:login` | `wrap_admin_login(admin.site.login)` | `GET`, `POST` | SIM (Privada) | NÃO (`noindex`) | SIM (Auth) | SIM | NÃO | `200 OK` (GET/Erro) / `302 Found` (Sucesso) / `429` (Rate limit) |
| `/admin/logout/` | `admin:logout` | `admin.site.logout` | `GET`, `POST` | NÃO | NÃO (`noindex`) | NÃO | SIM | **SIM** | `302 Found` / `200 OK` |

---

## 3. AUDITORIA DE LINKS INTERNOS E RESOLUÇÃO REVERSA

### 3.1 Integridade das Tags de URL no Sistema de Templates
Todas as referências a links internos na camada de apresentação utilizam estritamente a tag semântica `{% url 'namespace:name' %}`, eliminando caminhos estáticos *hardcoded* sujeitos a quebras durante futuras refatorações.

### 3.2 Ausência de Links Quebrados ou Vazios
A varredura completa dos 33 templates HTML e dos scripts Vanilla JS atesta:
* Zero referências a links vazios (`href=""`).
* Zero âncoras cegas para marcadores mortos (`href="#"`).
* Zero chamadas inline de pseudo-protocolo (`href="javascript:void(0)"`).
* Zero redirecionamentos em cadeia (*redirect chains*): todos os links internos apontam diretamente para as URLs canônicas com barra final (*trailing slash*).
