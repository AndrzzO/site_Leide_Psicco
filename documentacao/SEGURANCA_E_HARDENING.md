# SEGURANÇA E HARDENING DA APLICAÇÃO
## Instituto Mente em Foco
### Manual Técnico de Defesa em Profundidade, Governança de Configuração e Produção

---

## 1. Princípios Arquiteturais e Separação por Ambiente

O projeto adota a estratégia de **Defesa em Profundidade (*Defense in Depth*)**, estruturada em camadas complementares para garantir proteção sem sacrificar a produtividade em desenvolvimento:

1. **Camada de Ambientes Separados:**
   - **Desenvolvimento (`configuracoes.settings.desenvolvimento`):** Configurado para depuração local (`DEBUG=True`), SQLite rápido, cookies HTTP padrão e sem redirecionamento forçado para HTTPS (o que quebraria `localhost:8000`).
   - **Produção (`configuracoes.settings.producao`):** Configurado para falha fechada (*fail-closed*), `DEBUG=False` estrito, validação de variáveis de ambiente obrigatórias, cookies exclusivamente `Secure`, HSTS progressivo, cabeçalhos modernos e Content Security Policy ativa.
2. **Camada de Aplicação:** Validação rígida de entradas pelo Django ORM e Django Forms, sanitização estrita de Markdown via Bleach, controle de acesso a rascunhos editoriais e mascaramento de parâmetros sensíveis com `@sensitive_post_parameters`.
3. **Camada de Transporte e Rede:** Forçamento de HTTPS em produção, isolamento de frames (anti-clickjacking), proteção contra MIME-sniffing e controle de abertura de janelas (COOP).

---

## 2. Governança de Segredos (Secrets Management)

- **Princípio Fundamental:** Nenhuma credencial de produção é armazenada no código-fonte, em templates, scripts ou repositórios versionados.
- **Carregamento:** Todas as configurações sensíveis utilizam `python-decouple`, lendo exclusivamente de variáveis de ambiente do sistema operacional ou de arquivos `.env` locais devidamente ignorados no `.gitignore`.
- **Fail-Closed em Produção:** Se a variável `DJANGO_SECRET_KEY` ou `DATABASE_URL` não for fornecida no ambiente de produção, a aplicação levanta `ImproperlyConfigured` imediatamente na inicialização, impedindo a subida do servidor com valores inseguros ou padrões de fábrica.
- **Auditoria de Histórico:** O arquivo `.env` local contém unicamente chaves de desenvolvimento sintéticas e não há repositório Git com credenciais reais comprometidas.

---

## 3. HTTPS, Reverse Proxy e HSTS (Rollout Seguro)

### HTTPS e Redirecionamento
- Em produção, `DJANGO_SECURE_SSL_REDIRECT=True` força todas as requisições HTTP para HTTPS.
- Em desenvolvimento, essa configuração permanece desligada para permitir testes em `localhost`.

### Reverse Proxy e Terminação TLS
- A configuração `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` deve ser ativada **apenas** quando o provedor de hospedagem ou reverse proxy (ex: Nginx, AWS ALB, Render, Railway) terminar a conexão TLS de forma confiável e sobrescrever qualquer cabeçalho malicioso vindo do cliente.
- Por padrão, a configuração permanece desligada (`DJANGO_SECURE_PROXY_SSL_HEADER=False`), cabendo à equipe de deploy ativá-la quando a infraestrutura estiver homologada.

### Rollout Progressivo de HSTS (HTTP Strict Transport Security)
O HSTS instrui os navegadores a acessarem o site exclusivamente via HTTPS. Para evitar bloqueios acidentais e irreversíveis antes da validação do domínio oficial, o HSTS foi configurado com um plano progressivo:
1. **Fase Preliminar (Pré-Deploy):** `DJANGO_SECURE_HSTS_SECONDS=0` (desativado).
2. **Fase 1 (Validação de Domínio):** `DJANGO_SECURE_HSTS_SECONDS=300` (5 minutos). Permite reverter rapidamente caso haja problemas de certificado.
3. **Fase 2 (Estabilização):** `DJANGO_SECURE_HSTS_SECONDS=86400` (1 dia).
4. **Fase 3 (Produção Longa):** `DJANGO_SECURE_HSTS_SECONDS=31536000` (1 ano).
5. **HSTS Preload:** A inclusão no HSTS Preload (`DJANGO_SECURE_HSTS_PRELOAD=True`) é estritamente opcional e só deve ser solicitada após comprovação de que o domínio e todos os seus subdomínios permanecerão em HTTPS perpetuamente.

---

## 4. Sessões e Cookies Seguros

As sessões e tokens utilizam cookies fortalecidos em produção:
- `SESSION_COOKIE_SECURE = True`: Trafega somente via canal criptografado HTTPS.
- `SESSION_COOKIE_HTTPONLY = True`: Impede acesso ao cookie de sessão via JavaScript, mitigando roubo de sessão via XSS.
- `SESSION_COOKIE_SAMESITE = 'Lax'`: Protege contra requisições cross-site indevidas enquanto permite navegação padrão a partir de links externos.
- `CSRF_COOKIE_SECURE = True`: Token CSRF transmitido exclusivamente via HTTPS.
- `CSRF_COOKIE_HTTPONLY = False`: Mantido False para garantir compatibilidade com formulários web padrão do Django.
- `CSRF_COOKIE_SAMESITE = 'Lax'`: Alinhado às melhores práticas modernas da OWASP.

---

## 5. Cabeçalhos HTTP Defensivos

| Cabeçalho | Valor Configurado | Objetivo de Segurança |
|:---|:---|:---|
| **X-Frame-Options** | `DENY` | Impede que o site seja incorporado em `<iframe>` por terceiros (anti-Clickjacking). |
| **X-Content-Type-Options** | `nosniff` | Impede que o navegador interprete arquivos com MIME types incorretos (anti-MIME sniffing). |
| **Referrer-Policy** | `strict-origin-when-cross-origin` | Envia a origem completa apenas em requisições de mesma origem; envia apenas o domínio para links externos HTTPS; oculta em HTTP. |
| **Cross-Origin-Opener-Policy (COOP)** | `same-origin` | Isola o contexto de navegação de janelas abertas via `window.open`, impedindo ataques de ataque cruzado de memória. |
| **Permissions-Policy** | `camera=(), microphone=(), geolocation=(), payment=(), usb=()` | Desativa nativamente no navegador o acesso a APIs de hardware não utilizadas pelo site institucional. |

---

## 6. Content Security Policy (CSP Nativa Django 6.0)

O site adota a implementação de CSP nativa do Django 6.0 (`django.middleware.csp.ContentSecurityPolicyMiddleware`), sem necessidade de pacotes externos.

### Política em Produção (`SECURE_CSP`):
```python
SECURE_CSP = {
    'default-src': [CSP.SELF],
    'script-src': [CSP.SELF, CSP.NONCE],
    'style-src': [CSP.SELF, CSP.UNSAFE_INLINE, 'https://fonts.googleapis.com'],
    'font-src': [CSP.SELF, 'https://fonts.gstatic.com', 'data:'],
    'img-src': [CSP.SELF, 'data:'],
    'connect-src': [CSP.SELF],
    'object-src': [CSP.NONE],
    'base-uri': [CSP.SELF],
    'form-action': [CSP.SELF],
    'frame-ancestors': [CSP.NONE],
    'frame-src': [CSP.NONE],
}
```

### Justificativas das Diretivas:
- **`default-src 'self'`:** Restringe todas as fontes de recursos não declaradas especificamente à própria origem do site.
- **`script-src 'self' 'nonce-...'`:** Permite carregar scripts externos locais (`base.js`, `navegacao.js`, `home.js`) e scripts inline que possuam o token criptográfico imprevisível de nonce (`{% if csp_nonce %}nonce="{{ csp_nonce }}"{% endif %}`). Bloqueia estritamente `'unsafe-eval'`.
- **`style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`:** Permite os estilos CSS locais modulares, as folhas de estilo do Google Fonts e o uso de propriedades customizadas inline (`--stack-gap`).
- **`font-src 'self' https://fonts.gstatic.com data:`:** Permite o download de fontes WOFF2 legítimas do Google Fonts.
- **`img-src 'self' data:`:** Permite imagens locais, avatares e placeholders SVG base64.
- **`object-src 'none'`:** Bloqueia completamente plugins legados (Flash, Java Applets, ActiveX).
- **`frame-ancestors 'none'`:** Reforço do `X-Frame-Options: DENY` na política moderna de CSP.
- **`form-action 'self'`:** Garante que submissões de formulários só possam ter como destino o próprio servidor do Instituto.

---

## 7. Proteção contra CSRF e XSS

1. **CSRF:**
   - Todas as views POST exigem obrigatoriamente o token CSRF gerado pelo `CsrfViewMiddleware`.
   - Zero ocorrências de `@csrf_exempt` em todo o código-fonte.
   - Rejeição comprovada via testes automatizados com `enforce_csrf_checks=True`.
2. **XSS:**
   - Auto-escaping ativo em 100% dos templates do Django.
   - O único uso de `|safe` ocorre em `artigo.conteudo_formatado`, que passa rigorosamente pela biblioteca `Bleach` com allowlist estrita de tags e atributos seguros em `conteudos/sanitizacao.py`.
   - Dados de structured data JSON-LD utilizam substituição de segurança para sequências `</script>` (`\u003c\u002Fscript\u003e`), impedindo a injeção em tags `<script type="application/ld+json">`.

---

## 8. Superfície de Ataque de Backend

- **SQL Injection:** 100% das operações de banco de dados utilizam o Django ORM parametrizado nativo. Zero consultas brutas via `raw()`, `RawSQL` ou `cursor.execute()`. Ordenações utilizam listas estáticas (`'ordem'`, `'nome'`).
- **Open Redirect:** Não há captura ou redirecionamento baseado em parâmetros de requisição como `next=`. Todos os redirecionamentos são internos e fixos (ex: `redirect('contato:index')`).
- **SSRF (Server-Side Request Forgery):** A aplicação não realiza requisições HTTP ativas para URLs fornecidas por visitantes.
- **Path Traversal:** Uploads de arquivos utilizam nomes gerados aleatoriamente com `uuid4` e `slugify` em `nucleo.upload_paths`, sem aceitar nomes de arquivos fornecidos pelo cliente como caminho físico.
- **Controle de Acesso / IDOR:** Rascunhos de artigos e agendamentos futuros são bloqueados para o público geral no backend via `ArtigoQuerySet.publicados()`, retornando 404.

---

## 9. Uploads de Arquivos e Mídias

- **Acesso Restrito:** Apenas operadores autenticados no Django Admin podem enviar arquivos. O formulário público de contato **não** possui campo de upload.
- **Validação com Pillow:** A função `validar_imagem` em `nucleo/validators.py` inspeciona o cabeçalho binário real com `Image.open().verify()`. Arquivos renomeados com extensões falsas (ex: executáveis `.exe` renomeados para `.jpg`) são rejeitados imediatamente.
- **Formatos Permitidos:** Apenas `JPEG`, `PNG`, `WEBP` e `ICO`. Formatos perigosos como `SVG` arbitrário, scripts, executáveis e arquivos de sistema são rejeitados.
- **Limite de Tamanho:** Teto estrito de 10 MB centralizado em `TAMANHO_MAXIMO_IMAGEM_MB`.

---

## 10. Django Admin e Autenticação

- **URL do Admin:** Configurável via `DJANGO_ADMIN_URL` no `.env`, ausente de `robots.txt` e `sitemap.xml`.
- **Validação de Senhas:** `MinimumLengthValidator` fortalecido para exigir **no mínimo 12 caracteres**, além dos validadores nativos de similaridade com dados do usuário, senhas comuns e senhas puramente numéricas.
- **Proteção de Dados do Contato:** A mensagem completa dos contatos é exibida apenas na tela de detalhe (`fieldsets`), em bloco `readonly`, mantendo a listagem principal limpa para evitar vazamento visual acidental.

---

## 11. Logging e Tratamento de Erros

- **Minimização de PII:** A view `contato.views.index` é protegida com `@sensitive_post_parameters('nome', 'email', 'telefone', 'mensagem')`. Se uma exceção ocorrer durante o processamento, esses campos são mascarados como `********************` nos relatórios de erro do Django.
- **Logs Limpos:** Mensagens de log registram apenas eventos operacionais (ex: descarte por honeypot, contatos limpos por retenção), sem gravar dados pessoais completos, cookies ou credenciais.
- **Páginas de Erro Resilientes:** Handlers para 400, 403, 404 e 500 renderizam templates dedicados, amigáveis e acolhedores, sem exibir stack trace, versões de software ou caminhos de arquivos quando `DEBUG=False`.
