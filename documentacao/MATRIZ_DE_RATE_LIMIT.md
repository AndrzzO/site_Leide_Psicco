# MATRIZ DE RATE LIMIT E POLÍTICAS DE THROTTLING
**INSTITUTO MENTE EM FOCO — CONTROLE DE OPERAÇÕES SENSÍVEIS**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0

---

## 1. MATRIZ OPERACIONAL DE ENDPOINTS

| Endpoint / Operação | Método | Risco | Identificador de Origem | Limite | Janela | Duração do Bloqueio | Retorna HTTP 429? | Observações |
|---|---|---|---|---|---|---|---|---|
| **Formulário de Contato** (`/contato/`) | `POST` | **Alto** | `HMAC(SECRET_KEY, 'contato:' + IP)` | 5 submissões | 900s (15 min) | 900s (15 min) | **Sim** | Cabeçalho `Retry-After: 900` e `Cache-Control: no-store`. Submissões bloqueadas não gravam em banco nem disparam e-mail. |
| **Formulário de Contato** (`/contato/`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Visualização de página/formulário não consome cota. |
| **Admin Login (Origem IP)** (`/<admin>/login/`) | `POST` | **Alto** | `HMAC(SECRET_KEY, 'admin_ip:' + IP)` | 10 falhas | 900s (15 min) | 900s (15 min) | **Sim** | Bloqueia a origem antes de invocar PBKDF2 (mitigando DoS de CPU). Não afeta outras origens. |
| **Admin Login (Combo)** (`/<admin>/login/`) | `POST` | **Alto** | `HMAC(SECRET_KEY, 'admin_combo:' + IP + ':' + username)` | 5 falhas | 900s (15 min) | 900s (15 min) | **Sim** | Bloqueia a dupla específica sem criar lockout DoS global para o usuário. Login com sucesso limpa o contador da dupla. |
| **Admin Login** (`/<admin>/login/`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Exibição da tela de login não incrementa contadores. |
| **Admin Painel Interno** (`/<admin>/...`) | `GET`/`POST` | Baixo | Sessão de Staff | N/A | N/A | Nenhum | Não | Administradores autenticados operam sem qualquer rate limit. |
| **Busca no Blog** (`/conteudos/?q=...`) | `GET` | Médio | N/A | Sanitização de Entrada | N/A | Nenhum | Não | **Não limitado por rate limit de tempo** (não necessário no estado atual). Protegido por truncamento estrito de 100 caracteres e sanitização anti-DoS. |
| **Listagem do Blog** (`/conteudos/`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Paginação fixa em 9 itens por página no servidor. |
| **Artigos Individuais** (`/conteudos/<slug>/`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Apenas artigos publicados; rascunhos retornam 404 estrito. |
| **Páginas Institucionais** (`/`, `/sobre-mim/`, `/servicos/...`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | **Zero rate limit.** Navegação humana fluida e estável. |
| **Arquivos Estáticos & Mídia** (`/static/...`, `/media/...`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Entregues via WhiteNoise/Web Server com Cache-Control. |
| **Arquivos Técnicos SEO** (`/robots.txt`, `/sitemap.xml`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Crawlers legítimos navegam livremente. |
| **Health Check** (`/health/`) | `GET` | Baixo | N/A | Ilimitado | N/A | Nenhum | Não | Endpoint de monitoramento de infraestrutura. |

---

## 2. DIRETRIZES DE AUDITORIA E NÃO-SOBREPOSIÇÃO

1. **Sem Duplo Rate Limit:** A aplicação utiliza exclusivamente a camada `nucleo.rate_limit`, sem duplicar regras em middlewares adicionais ou bibliotecas externas não integradas.
2. **Identificadores Pseudonimizados:** Toda chave gravada no cache é composta pelo prefixo `security:rl:v1:`, pelo escopo (`contato`, `admin_ip`, `admin_combo`), pela finalidade (`attempts`, `block`) e por um digest HMAC de 32 caracteres.
3. **Resiliência:** Em caso de perda de conexão com o backend de cache, o rate limiter entra em modo *fail-open* com emissão de warning sem PII, garantindo continuidade do serviço.
