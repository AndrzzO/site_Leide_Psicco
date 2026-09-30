# AUDITORIA DE SEGURANÇA E HARDENING
## Instituto Mente em Foco
### Data: Setembro de 2026 | Versão do Django: 6.0.8 | Python: 3.14.5

---

## 1. Visão Geral da Auditoria

Esta auditoria de segurança foi realizada como parte do **PROMPT 16**, contemplando inspeção estática de código, auditoria de configurações, verificação de segredos, análise da superfície de ataque do backend e criação de testes automatizados.

### Classificação de Severidade Adotada:
- **CRÍTICO:** Vulnerabilidades que permitiriam comprometimento imediato do sistema, execução arbitrária de código, vazamento massivo de segredos ou bypass total de autenticação.
- **ALTO:** Falhas que expõem dados sensíveis (PII/LGPD), permitem ataques de CSRF/XSS, ou configurações de produção com falhas estruturais de isolamento.
- **MÉDIO:** Ausência de cabeçalhos defensivos modernos, configurações de cookies permissivas, ou políticas de HSTS ativadas sem planejamento gradual.
- **BAIXO:** Pequenas inconsistências de documentação, falta de tipagem de variáveis de ambiente secundárias ou mensagens informativas em logs de depuração.
- **INFORMATIVO:** Recomendações arquiteturais e itens vinculados estritamente à infraestrutura futura de deploy (provedor de nuvem, terminação TLS, DNS oficial).

---

## 2. Tabela Consolidada de Achados

| ID | Categoria | Arquivo / Módulo | Severidade | Problema | Evidência | Impacto | Correção Implementada | Status |
|:---|:---|:---|:---:|:---|:---|:---|:---|:---:|
| **SEC-01** | Secrets | `.env` / Git | **INFORMATIVO** | Risco de versionamento acidental de chaves locais | Arquivo `.env` local contém credenciais sintéticas de dev e está listado no `.gitignore` | Nenhum risco de vazamento; repositório não possui histórico com segredos reais de produção | `.gitignore` revisado; `.env.example` padronizado sem valores | **RESOLVIDO** |
| **SEC-02** | Settings | `configuracoes/settings/producao.py` | **ALTO** | `DEBUG = True` acidental em produção | `DEBUG = False` rigorosamente fixado e validado | Vazamento de stack traces e variáveis de ambiente para visitantes | `DEBUG = False` forçado em `producao.py`; system check `--deploy` valida | **RESOLVIDO** |
| **SEC-03** | Settings | `configuracoes/settings/producao.py` | **CRÍTICO** | Risco de inicialização com `ALLOWED_HOSTS = ['*']` | Checagem de inicialização em `producao.py` | Host Poisoning, spoofing de URLs canônicas e envenenamento de cache | Validação estrita que levanta `ImproperlyConfigured` se vazio ou contendo `*` | **RESOLVIDO** |
| **SEC-04** | HTTPS / HSTS | `configuracoes/settings/producao.py` | **ALTO** | Ativação cega de `SECURE_HSTS_PRELOAD` sem domínio final | `producao.py` continha `SECURE_HSTS_PRELOAD = True` e 1 ano hardcoded | Bloqueio irrevogável de navegadores se o domínio ou subdomínios tiverem falha de TLS | `SECURE_HSTS_SECONDS` configurável via env (default 0 pré-deploy); `PRELOAD = False` | **RESOLVIDO** |
| **SEC-05** | Reverse Proxy | `configuracoes/settings/producao.py` | **MÉDIO** | `SECURE_PROXY_SSL_HEADER` hardcoded sem infraestrutura real | Header `HTTP_X_FORWARDED_PROTO` assumido cegamente | Risco de spoofing do estado HTTPS em servidores sem reverse proxy confiável | Tornada configurável via `DJANGO_SECURE_PROXY_SSL_HEADER` (padrão desligado) | **RESOLVIDO** |
| **SEC-06** | Cookies | `configuracoes/settings/producao.py` | **ALTO** | Cookies de sessão sem flags `HttpOnly` e `SameSite` explícitas | Flags padrão do framework sem explicitação em produção | Risco de interceptação via scripts de terceiros ou requisições cross-site | `SESSION_COOKIE_SECURE=True`, `HTTPONLY=True`, `SAMESITE='Lax'` aplicados | **RESOLVIDO** |
| **SEC-07** | Headers | `configuracoes/settings/base.py` | **MÉDIO** | Ausência de `Cross-Origin-Opener-Policy` (COOP) | Cabeçalho não emitido nas respostas HTTP | Janelas abertas via `window.open` poderiam manter referência ao contexto da página | `SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'` ativado nativamente | **RESOLVIDO** |
| **SEC-08** | Headers | `nucleo/middleware.py` | **MÉDIO** | Ausência de `Permissions-Policy` | Cabeçalho ausente nas respostas HTTP | Acesso desnecessário de APIs do navegador (câmera, microfone, geolocalização) | `SecurityHeadersMiddleware` criado restringindo APIs não utilizadas | **RESOLVIDO** |
| **SEC-09** | CSP | `configuracoes/settings/base.py` e `producao.py` | **ALTO** | Ausência de Content Security Policy (CSP) nativa | Cabeçalho `Content-Security-Policy` não estava configurado | Superfície vulnerável a injeção inline de scripts e terceiros não homologados | `ContentSecurityPolicyMiddleware` e `SECURE_CSP` nativos do Django 6.0 configurados | **RESOLVIDO** |
| **SEC-10** | CSRF | Projeto Completo | **INFORMATIVO** | Verificação de `@csrf_exempt` em rotas públicas | Busca textual por `csrf_exempt` retornou zero ocorrências | O projeto mantém proteção CSRF íntegra em todos os formulários | Mantida obrigatoriedade de token CSRF; teste automatizado criado | **RESOLVIDO** |
| **SEC-11** | XSS | `conteudos/sanitizacao.py` e templates | **INFORMATIVO** | Auditoria de filtros `\|safe` e `mark_safe` | Apenas 1 uso de `\|safe` em `artigo.conteudo_formatado` (Bleach) e JSON-LD | Injeção de código HTML/JS em conteúdo editorial | Allowlist Bleach mantida; escape de JSON-LD com suporte a nonce CSP | **RESOLVIDO** |
| **SEC-12** | Backend / SQL | Apps `nucleo`, `paginas`, `servicos`, `conteudos`, `contato` | **INFORMATIVO** | Verificação de Raw SQL ou ordenação dinâmica com inputs | Zero ocorrências de `.raw()`, `cursor.execute()` ou `order_by(request.GET)` | Risco de SQL Injection | 100% das operações utilizam Django ORM parametrizado nativo | **RESOLVIDO** |
| **SEC-13** | Backend / SSRF | Projeto Completo | **INFORMATIVO** | Requisições HTTP externas originadas pelo servidor | Zero uso de `requests`, `httpx` ou `urllib.request` disparados por inputs | Risco de Server-Side Request Forgery | Não aplicável no estado atual da aplicação | **RESOLVIDO** |
| **SEC-14** | Uploads | `nucleo/validators.py` | **ALTO** | Validação profunda de imagens contra executáveis disfarçados | `validar_imagem` utiliza `Pillow` com `Image.open().verify()` | Upload de scripts ou executáveis via extensão falsa `.jpg` | Validação de cabeçalho real, limite de 10 MB e nomes UUID aplicados | **RESOLVIDO** |
| **SEC-15** | Admin | `configuracoes/settings/base.py` | **MÉDIO** | Comprimento mínimo de senha administrativa era o default (8 caracteres) | `MinimumLengthValidator` sem opções explícitas | Senhas fracas no painel de administração vulneráveis a ataques de dicionário | `MinimumLengthValidator` configurado com `min_length=12` | **RESOLVIDO** |
| **SEC-16** | Logging / PII | `contato/views.py` | **ALTO** | Risco de PII em traces de exceções em caso de falha | View `index` não possuía `@sensitive_post_parameters` | Dados pessoais (nome, e-mail, telefone, mensagem) expostos em relatórios de erro | `@sensitive_post_parameters('nome', 'email', 'telefone', 'mensagem')` aplicado | **RESOLVIDO** |
| **SEC-17** | Error Pages | `nucleo/views.py` / `templates/erros/` | **INFORMATIVO** | Páginas customizadas de erro HTTP (400, 403, 404, 500) | Handlers `tratar_erro_*` renderizam templates limpos | Vazamento de paths do servidor, versões ou variáveis de ambiente para visitantes | Templates acolhedores validados sob `DEBUG=False` sem vazamento técnico | **RESOLVIDO** |
| **SEC-18** | Dependências | `requirements.txt` | **INFORMATIVO** | Auditoria de dependências quebradas ou vulneráveis | Execução de `python -m pip check` retornou zero problemas | Incompatibilidades de pacotes ou versões vulneráveis | Pip check íntegro; ecossistema minimalista sem bibliotecas supérfluas | **RESOLVIDO** |

---

## 3. Conclusão da Auditoria

A aplicação demonstrou excelente maturidade inicial, sem vulnerabilidades arquiteturais graves (zero raw SQL, zero open redirects, zero CSRF bypass). Todos os achados identificados foram devidamente mitigados através de configurações defensivas nativas do Django 6.0, sem necessidade de adicionar dependências de terceiros nem alterar o modelo de dados.
