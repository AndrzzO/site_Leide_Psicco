# AUDITORIA DE ABUSO, RATE LIMIT E VETORES DE RISCO
**INSTITUTO MENTE EM FOCO — MAPEAMENTO ANALÍTICO DE SUPERFÍCIE DE ATAQUE**
**PROJETO:** INSTITUTO MENTE EM FOCO | **ESTADO:** AUDITADO E MITIGADO

---

## 1. VISÃO GERAL E DIRETRIZ FUNDAMENTAL

A proteção contra abuso e automação hostil no portal institucional do **Instituto Mente em Foco** foi concebida sob o princípio da **defesa em profundidade direcionada**.

> [!IMPORTANT]
> **REGRA FUNDAMENTAL — ZERO RATE LIMIT GLOBAL:**
> O portal não impõe barreiras de rate limiting a navegações legítimas, requisições de leitura de páginas institucionais (Home, Sobre Mim, Serviços, Artigos), assets estáticos (CSS, JS, imagens, fontes) ou indexadores autorizados de mecanismos de busca (`robots.txt`, `sitemap.xml`).
> O rate limiting atua exclusivamente sobre **operações de escrita e autenticação suscetíveis a abuso** (POST de Login Administrativo e POST do Formulário de Contato), associado à blindagem contra DoS lógico em busca e paginação.

---

## 2. INVENTÁRIO COMPLETO E CLASSIFICAÇÃO DE RISCO DOS ENDPOINTS

| Endpoint / Rota | Método | Autenticação | Tipo de Operação | Custo Computacional | Altera Estado? | Envia E-mail? | Grava BD? | Queries BD | Classificação de Risco | Rate Limit de Aplicação? | Proteção Implementada |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `/` (Início / Home) | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 6 | **Baixo Risco** | Não aplicável | Proteção por cache e orçamentos de queries (Prompt 15) |
| `/sobre-mim/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/psicologia/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/neuropsicologia/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/traumas/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/separacao-e-recomecos/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/novos-relacionamentos/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/avaliacao/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/avaliacao-psicologica/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/avaliacao-neuropsicologica/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/servicos/reabilitacao-neurocognitiva/` | GET | Anônimo | Leitura / Render | Baixo | Não | Não | Não | 5 | **Baixo Risco** | Não aplicável | Orçamentos estritos de I/O |
| `/conteudos/` | GET | Anônimo | Leitura / Listagem | Baixo | Não | Não | Não | ~6 | **Baixo Risco** | Não aplicável | Paginação fixa em 9 itens |
| `/conteudos/?q=...` | GET | Anônimo | Busca Textual | Médio | Não | Não | Não | 3-5 | **Médio Risco** | Hardening de Entrada | Truncamento estrito em 100 caracteres; sanitização anti-DoS; sem regex arbitrária |
| `/conteudos/categoria/<slug>/` | GET | Anônimo | Leitura / Filtro | Baixo | Não | Não | Não | ~6 | **Baixo Risco** | Não aplicável | Query parametrizada via slug |
| `/conteudos/<slug>/` | GET | Anônimo | Leitura / Artigo | Baixo | Não | Não | Não | 6 | **Baixo Risco** | Não aplicável | 404 estrito para rascunhos e datas futuras |
| `/contato/` | GET | Anônimo | Exibição de Form | Baixo | Não | Não | Não | 4 | **Baixo Risco** | Não aplicável | Zero consumo de cota de submissão |
| `/contato/` | POST | Anônimo | Escrita / Triagem | Médio/Alto | **Sim** | **Sim** | **Sim** | ~4-6 | **ALTO RISCO** | **SIM (Obrigatório)** | Rate limit de 5/15min por origem HMAC, Honeypot invisível, HTTP 429 com Retry-After e no-store, sem DB/e-mail no bloqueio |
| `/<admin_path>login/` | GET | Anônimo | Exibição de Login | Baixo | Não | Não | Não | ~2 | **Baixo Risco** | Não aplicável | Zero consumo de tentativas |
| `/<admin_path>login/` | POST | Anônimo | Autenticação | **Alto (PBKDF2)**| **Sim (Sessão)** | Não | Não | ~2-4 | **ALTO RISCO** | **SIM (Obrigatório)** | Rate limit por IP (10 falhas/15min) e Combo IP+User (5 falhas/15min), 429 antes de computar hash, sem enumeração, sem lockout DoS |
| `/<admin_path>...` (Painel) | GET/POST | Staff Autenticado | Gestão Interna | Médio | Sim | Não | Sim | Variável | **Baixo Risco** | Não aplicável | Acesso restrito a administradores; sem rate limit em operações normais |
| `/politica-de-privacidade/` | GET | Anônimo | Leitura | Baixo | Não | Não | Não | 3 | **Baixo Risco** | Não aplicável | Conteúdo estático/cache |
| `/politica-de-cookies/` | GET | Anônimo | Leitura | Baixo | Não | Não | Não | 3 | **Baixo Risco** | Não aplicável | Conteúdo estático/cache |
| `/robots.txt` | GET | Anônimo | Diretiva de Crawling| Mínimo | Não | Não | Não | 0 | **Baixo Risco** | Não aplicável | Geração procedural dinâmica |
| `/sitemap.xml` | GET | Anônimo | Mapeamento SEO | Baixo | Não | Não | Não | ~3 | **Baixo Risco** | Não aplicável | Sitemap nativo em cache |
| `/health/` | GET | Anônimo | Monitoramento | Mínimo | Não | Não | Não | 0 | **Baixo Risco** | Não aplicável | Resposta 'OK' instantânea sem I/O |

---

## 3. AUDITORIA DE VETORES ESPECÍFICOS DE RISCO

### 3.1 Força Bruta e Credential Stuffing (Admin Login)
- **Vulnerabilidade Teórica:** Tentativas contínuas de adivinhar credenciais de superusuário ou explorar senhas vazadas em outros serviços.
- **Risco de DoS de CPU:** O algoritmo PBKDF2 com milhares de iterações consome processamento propositalmente para desacelerar invasores. Múltiplas requisições paralelas poderiam sobrecarregar o worker WSGI.
- **Mitigação Implementada:** 
  1. O wrapper `wrap_admin_login` verifica a cota de IP e a cota combo antes de chamar o backend de autenticação. Se a origem estiver bloqueada, o Django responde imediatamente com HTTP 429 sem acionar o PBKDF2.
  2. A cota combo `(origem, username)` bloqueia tentativas repetidas para o mesmo usuário (5 falhas / 15 min).
  3. A cota por origem (10 falhas / 15 min) impede que um mesmo atacante tente senhas para múltiplos nomes de usuário diferentes (*credential stuffing*).

### 3.2 Enumeração de Usuários (Username Enumeration)
- **Vulnerabilidade Teórica:** Identificar se uma conta existe no sistema com base em diferenças de tempo de resposta ou mensagens de erro divergentes ("Usuário não existe" vs "Senha incorreta").
- **Mitigação Implementada:**
  1. A view de login do Django Admin renderiza uma mensagem idêntica para qualquer falha de autenticação.
  2. O `RateLimiter` normaliza e contabiliza tentativas mesmo quando o usuário não existe no banco de dados.
  3. As respostas 429 não revelam se a conta existe ou não.

### 3.3 Negação de Serviço por Bloqueio de Conta (Account Lockout DoS)
- **Vulnerabilidade Teórica:** Se qualquer usuário não autenticado puder bloquear uma conta legítima errando a senha 5 vezes de qualquer lugar da internet, o sistema de proteção vira vetor de ataque para impedir o trabalho da clínica.
- **Mitigação Implementada:** O bloqueio combo é atrelado estritamente à tupla `(origem_ip, username)`. Se um atacante a partir do IP `198.51.100.1` errar 5 vezes a senha do usuário `admin`, apenas aquele IP específico é impedido de tentar novamente aquele usuário. O administrador legítimo em seu IP habitual não sofre qualquer restrição.

### 3.4 Flooding de Formulário e Mail Bombing (Contato)
- **Vulnerabilidade Teórica:** Bots submetendo milhares de mensagens para lotar o banco de dados e sobrecarregar o serviço de e-mail institucional (SMTP).
- **Mitigação Implementada:**
  1. **Honeypot:** Campo invisível `campo_verificacao` que descarta envios automatizados sem salvar no banco e sem disparar e-mail.
  2. **Rate Limit:** Máximo de 5 submissões a cada 15 minutos por origem pseudonimizada. Requisições 429 são sumariamente rejeitadas sem processar persistência nem despacho SMTP.

### 3.5 DoS Lógico em Busca Textual e Paginação
- **Vulnerabilidade Teórica:** Envio de termos de busca com 50.000 caracteres ou paginação absurda (`?page=999999999999`) causando estouro de memória ou lentidão em consultas ORM.
- **Mitigação Implementada:**
  1. Limite estrito de 100 caracteres para `q` em `conteudos/views.py`.
  2. Truncamento automático e sanitização de strings.
  3. Tratamento defensivo de parâmetros de página com limites superiores seguros.

---

## 4. AUDITORIA DE RESOLUÇÃO DE IP E CABEÇALHOS DE PROXY

- **Diagnóstico:** A inspeção cega de `HTTP_X_FORWARDED_FOR` permitia bypass trivial do rate limit caso o cliente injetasse um cabeçalho arbitrário.
- **Remediação:** O helper `obter_ip_cliente` utiliza `REMOTE_ADDR` como default seguro incondicional. O cabeçalho de proxy somente é considerado quando `TRUST_PROXY_CLIENT_IP = True` for expressamente habilitado em ambiente de produção atrás de proxy reverso homologado.

---

## 5. AUDITORIA DE PRIVACIDADE E CONFORMIDADE LGPD

- **IPs e Usernames:** Nenhum IP de visitante e nenhum nome de usuário é gravado em texto puro nas chaves de cache ou em tabelas de auditoria.
- **HMAC:** As chaves utilizam HMAC-SHA256 com chave privada derivada da `SECRET_KEY`, tornando impossível a reconstituição dos endereços de rede a partir de vazamento de cache.
- **Logs:** Registros de advertência para respostas 429 contêm apenas o escopo funcional afetado, com zero dados pessoais (PII).
