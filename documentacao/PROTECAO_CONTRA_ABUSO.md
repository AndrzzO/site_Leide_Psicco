# MANUAL DE PROTEÇÃO CONTRA ABUSO, RATE LIMITING E RESILIÊNCIA
**INSTITUTO MENTE EM FOCO — ENGENHARIA DE SEGURANÇA NA CAMADA DE APLICAÇÃO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0

---

## 1. INTRODUÇÃO E PRINCÍPIOS ARQUITETURAIS

A proteção da integridade operacional do website institucional do **Instituto Mente em Foco** é orientada por quatro pilares:
1. **Proteção Focada em Vetores Reais:** O rate limiting aplica-se estritamente a fluxos que sofrem risco real de automação abusiva (envio de formulários de contato e tentativas de autenticação administrativa).
2. **Preservação Irrestrita da Experiência do Usuário e de SEO:** Páginas de leitura institucional, artigos de blog e arquivos de suporte (CSS, JS, imagens, fonts, `robots.txt`, `sitemap.xml`) nunca sofrem rate limit na camada de aplicação.
3. **Privacidade Rigorosa por Design (LGPD):** A aplicação não persiste endereços de IP em banco de dados ou logs; as chaves de identificação transitória são pseudonimizadas através de **HMAC-SHA256**.
4. **Resiliência Fail-Open:** Falhas no subsistema de cache não geram indisponibilidade ou erros 500 no portal; o tráfego legítimo é preservado enquanto avisos técnicos sem PII são registrados.

---

## 2. ARQUITETURA DO RATE LIMITER (`nucleo/rate_limit.py`)

A lógica foi concentrada em módulo único e enxuto para evitar dispersão de chamadas de cache:
- **Resolução de IP (`obter_ip_cliente`):**
  - Utiliza `REMOTE_ADDR` como default seguro contra *IP spoofing*.
  - Desativa a confiança cega em `HTTP_X_FORWARDED_FOR` a menos que `TRUST_PROXY_CLIENT_IP = True` esteja explicitamente habilitado.
- **HMAC de Origem (`gerar_digest_origem`):**
  - Transforma `(escopo, identificador)` em um digest hexadecimal de 32 caracteres utilizando a chave criptográfica da aplicação (`SECRET_KEY`).
  - Impede ataques de dicionário ou tabelas pré-computadas (*rainbow tables*) contra o espaço de endereçamento IPv4.
- **Namespace Padronizado:**
  - `security:rl:v1:{escopo}:{tipo}:{digest}`
  - Permite invalidação e versionamento futuro sem impactar outros caches da aplicação.
- **Resposta HTTP 429 (`criar_resposta_429`):**
  - Renderiza o template acessível [`templates/erros/429.html`](file:///c:/Users/andre/Documents/SiteDjangoLeide/templates/erros/429.html).
  - Define o cabeçalho `Retry-After` com o tempo aproximado de desbloqueio em segundos.
  - Define `Cache-Control: no-store` para impedir que intermediários façam cache da resposta transitória.
  - Mantém 100% dos cabeçalhos defensivos injetados pela pilha de segurança (`Permissions-Policy`, `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`).

---

## 3. ESCOPOS DE APLICAÇÃO

### 3.1 Formulário de Contato (`contato`)
- **Regra:** Limita o número de submissões `POST` bem-sucedidas ou malformadas por origem.
- **Threshold Padrão:** 5 submissões a cada 15 minutos (900 segundos).
- **Tratamento:** Se o limite for ultrapassado, retorna HTTP 429 imediatamente. Nenhuma mensagem é gravada no banco de dados e nenhuma notificação por e-mail é despachada.
- **Honeypot Integrado:** O campo armadilha invisível (`campo_verificacao`) descarta o envio antes de qualquer consumo de recursos, simulando sucesso para o bot sem alertá-lo da detecção.

### 3.2 Login Administrativo (`admin_login`)
- **Proteção em Duas Camadas:**
  1. **Origem (IP):** Máximo de 10 tentativas falhas a cada 15 minutos. Caso excedido, a origem é bloqueada por 15 minutos.
  2. **Combo (Origem + Username):** Máximo de 5 tentativas falhas a cada 15 minutos para a combinação específica. Caso excedido, a combinação é bloqueada por 15 minutos.
- **Prevenção de DoS de CPU (Password Hashing):** Se a origem ou a combinação já estiver sob bloqueio, a requisição é interceptada antes da verificação PBKDF2/Argon2.
- **Prevenção de Account Lockout DoS:** O bloqueio não é global por usuário; apenas a origem abusadora é contida, garantindo que o administrador legítimo continue acessando o painel de seu IP.
- **Prevenção de Enumeração de Contas:** Tentativas com usuários existentes e inexistentes produzem o mesmo tempo de resposta e mensagens padronizadas.
- **Autenticação Bem-Sucedida:** Reseta a cota da combinação `(origem, username)`, preservando a cota geral do IP.

### 3.3 Busca Textual e Paginação no Blog (`conteudos`)
- **Limite de Comprimento:** Consultas `?q=` são truncadas no limite de 100 caracteres antes de atingir o ORM.
- **Proteção de Paginação:** O parâmetro `?page=` é higienizado para valores válidos entre 1 e 10.000, com fallback seguro para a primeira página em caso de strings ou caracteres inválidos.

---

## 4. LIMITAÇÕES REAIS E GARANTIAS DE CACHE

- **Desenvolvimento e Ambiente Mono-Processo:** O cache padrão `LocMemCache` opera por processo com travas de thread (`threading.Lock`), sendo atômico localmente.
- **Ambiente de Produção Multi-Worker:** Em servidores com múltiplos workers independentes (ex.: Gunicorn com 4 workers), cada worker possui seu próprio `LocMemCache`. Nessa configuração, o rate limiting opera como proteção em regime *best-effort* (a cota efetiva multiplica-se pelo número de workers).
- **Recomendação para Produção Escalada:** Caso o tráfego justifique escala horizontal com múltiplos servidores, a equipe de DevOps deve adotar um backend centralizado (Redis/Memcached) ou configurar rate limiting na camada de proxy reverso (Nginx `limit_req_zone` / Cloudflare WAF).

---

## 5. VARIÁVEIS DE CONFIGURAÇÃO

As variáveis a seguir podem ser ajustadas no arquivo `.env` sem alteração de código-fonte:

| Variável | Padrão | Descrição |
|---|---|---|
| `CONTACT_RATE_LIMIT_COUNT` | `5` | Número máximo de envios de formulário de contato permitidos por janela |
| `CONTACT_RATE_LIMIT_WINDOW` | `900` | Duração da janela do formulário de contato (segundos) |
| `ADMIN_LOGIN_IP_LIMIT` | `10` | Tentativas falhas permitidas por IP de origem no login administrativo |
| `ADMIN_LOGIN_IP_WINDOW` | `900` | Janela de contagem de falhas por IP (segundos) |
| `ADMIN_LOGIN_IP_BLOCK` | `900` | Tempo de bloqueio temporário do IP após esgotar o limite (segundos) |
| `ADMIN_LOGIN_COMBO_LIMIT` | `5` | Tentativas falhas permitidas para a dupla (IP, username) |
| `ADMIN_LOGIN_COMBO_WINDOW` | `900` | Janela de contagem da dupla (IP, username) (segundos) |
| `ADMIN_LOGIN_COMBO_BLOCK` | `900` | Tempo de bloqueio temporário da dupla (segundos) |
| `TRUST_PROXY_CLIENT_IP` | `False` | Habilita leitura de `X-Forwarded-For` exclusivamente atrás de proxy reverso confiável |
