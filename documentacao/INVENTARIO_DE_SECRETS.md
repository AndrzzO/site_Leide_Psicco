# INVENTÁRIO DE SEGREDOS E VARIÁVEIS DE AMBIENTE
## Instituto Mente em Foco
### Diretriz Absoluta: ESTE DOCUMENTO NÃO CONTÉM E NUNCA DEVE CONTER VALORES REAIS DE SENHAS OU CHAVES.

---

## 1. Tabela de Governança de Segredos

| Variável | Finalidade | Ambiente | Obrigatória? | Origem Esperada | Status Atual |
|:---|:---|:---:|:---:|:---|:---:|
| `DJANGO_SETTINGS_MODULE` | Define qual arquivo de configuração carrega (`desenvolvimento` ou `producao`) | Todos | Sim | Variável de sistema / `.env` / Process Manager | Configurado |
| `DJANGO_SECRET_KEY` | Chave criptográfica para assinatura de cookies, sessões, tokens CSRF e hashes | Produção | Sim (Estrito) | Cofre de segredos (Vault, AWS Secrets, Render Env) | Sintética em dev; obrigatória em prod |
| `DJANGO_DEBUG` | Controla modo de depuração (`True` em dev, `False` em produção) | Todos | Sim | `.env` / Variável de ambiente | Configurado (`True` dev / `False` prod) |
| `DJANGO_ALLOWED_HOSTS` | Lista de nomes de domínio autorizados a servir requisições HTTP | Produção | Sim (Estrito) | Variável de ambiente | Restrito e validado (sem wildcard `*`) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens HTTPS autorizadas para submissões seguras de formulários | Produção | Sim | Variável de ambiente | Tipado via `Csv()`; pendente de domínio final |
| `DATABASE_URL` | String de conexão com o banco relacional PostgreSQL de produção | Produção | Sim | Painel de banco gerenciado (Postgres PaaS) | Opcional em dev (SQLite); obrigatório em prod |
| `DJANGO_ADMIN_URL` | Rota customizável para acesso ao painel administrativo Django Admin | Todos | Opcional | Variável de ambiente (default: `admin/`) | Configurado |
| `DJANGO_SECURE_SSL_REDIRECT` | Força redirecionamento de conexões HTTP inseguras para HTTPS | Produção | Sim | Variável de ambiente (default: `True` em prod) | Configurado |
| `DJANGO_SECURE_HSTS_SECONDS` | Tempo de vida em segundos da política HSTS no navegador | Produção | Sim (Rollout) | Variável de ambiente (default: `0` pré-deploy) | Rollout gradual planejado |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | Aplica política HSTS a todos os subdomínios da zona DNS | Produção | Não | Variável de ambiente (default: `False`) | Desativado até validação do domínio |
| `DJANGO_SECURE_HSTS_PRELOAD` | Solicita inclusão do domínio na lista HSTS fixa dos navegadores | Produção | Não | Variável de ambiente (default: `False`) | Desativado (exige decisão estratégica) |
| `DJANGO_SECURE_PROXY_SSL_HEADER` | Informa ao Django se a terminação TLS é realizada por reverse proxy | Produção | Não | Variável de ambiente (default: `False`) | Configurado dependente do provedor |
| `DJANGO_SECURE_CSP_REPORT_ONLY` | Alterna a política CSP entre bloqueio ativo ou modo diagnóstico | Homologação | Não | Variável de ambiente (default: `False`) | Suportado |
| `SITE_URL` | URL pública oficial canônica da aplicação institucional | Todos | Sim | Variável de ambiente | `http://localhost:8000` em dev |
| `WHATSAPP_NUMERO` | Número oficial de atendimento via WhatsApp | Todos | Opcional | Configurações institucionais | Pendente definição formal |
| `EMAIL_CONTATO` | Endereço oficial de e-mail institucional e destinatário de notificações | Todos | Opcional | Configurações institucionais | Pendente definição formal |
| `INSTAGRAM_URL` | Perfil oficial da profissional no Instagram | Todos | Opcional | Configurações institucionais | Pendente definição formal |
| `CRP_PROFISSIONAL` | Registro profissional junto ao Conselho Regional de Psicologia | Todos | Opcional | Configurações institucionais | Pendente definição formal |
| `CONTATO_RETENCAO_DIAS` | Prazo em dias para expiração e limpeza automática de contatos (LGPD) | Produção | Opcional | Política de retenção de dados | Configurável (default: `None`) |
| `SEO_ALLOW_INDEXING` | Governança de indexação por motores de busca (robots / sitemap) | Produção | Sim | Variável de ambiente (default: `False`) | Protegido contra indexação prematura |
| `GOOGLE_SITE_VERIFICATION` | Token público de verificação de propriedade no Google Search Console | Produção | Opcional | Painel Google Search Console | Pendente registro de domínio |
| `BING_SITE_VERIFICATION` | Token público de verificação de propriedade no Bing Webmaster | Produção | Opcional | Painel Bing Webmaster | Pendente registro de domínio |

---

## 2. Diretrizes de Rotação de Segredos

1. **SECRET_KEY:**
   - Em caso de comprometimento, deve ser gerada uma nova chave aleatória de pelo menos 50 caracteres via `secrets.token_urlsafe(50)`.
   - A rotação invalida todas as sessões administrativas ativas e assinaturas anteriores.
2. **DATABASE_URL:**
   - As credenciais de acesso ao PostgreSQL devem ser provisionadas exclusivamente pelo serviço gerenciado do provedor de nuvem, com tráfego TLS obrigatório.
3. **Credenciais Administrativas:**
   - Senhas de operadores do Django Admin devem respeitar o validador com mínimo de 12 caracteres, sem repetição de atributos ou sequências óbvias.
