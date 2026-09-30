# Matriz Completa de Variáveis de Ambiente
**Projeto:** Instituto Mente em Foco  
**Data:** 28/09/2026  
**Finalidade:** Inventário rigoroso de configuração e segredos por ambiente (Desenvolvimento, Testes, Homologação/Staging e Produção).  
**Regra Absoluta:** NENHUM valor secreto real está registrado neste documento. Apenas nomes, propósitos e exemplos sintéticos seguros.

---

## 1. Variáveis Essenciais do Núcleo Django

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `DJANGO_SETTINGS_MODULE` | Módulo de settings a ser carregado pelo runtime | `configuracoes.settings.desenvolvimento` | `configuracoes.settings.desenvolvimento` | `configuracoes.settings.producao` | **SIM** | Não | `configuracoes.settings.producao` | `configuracoes.settings.desenvolvimento` | `manage.py`, `wsgi.py` |
| `DJANGO_SECRET_KEY` | Chave criptográfica para hashes, sessões e tokens CSRF | Chave estática dev | Chave estática test | Chave randômica >50 chars | **SIM** | **SIM** | `c2VjdXJlX3JhbmRvbV9rZXlfZm9yX3Byb2RfdmFsaWRhdGlvbl8yMDI2` | Rejeita chave dev em prod | `base.py`, `producao.py` |
| `DJANGO_DEBUG` | Ativação do modo de depuração | `True` | `False` | `False` (forçado no código) | Não (código fixa False) | Não | `False` | `True` em dev, `False` em prod | `desenvolvimento.py`, `producao.py` |
| `DJANGO_ALLOWED_HOSTS` | Lista de nomes de domínio permitidos no cabeçalho Host | `localhost,127.0.0.1` | `testserver` | Domínios canônicos oficiais | **SIM** | Não | `menteemfoco.com.br,www.menteemfoco.com.br` | Rejeita vazio ou `*` em prod | `desenvolvimento.py`, `producao.py` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens confiáveis para requisições POST com validação CSRF | `http://localhost:8000` | Vazio | Origens HTTPS oficiais | **SIM** | Não | `https://menteemfoco.com.br,https://www.menteemfoco.com.br` | String vazia | `desenvolvimento.py`, `producao.py` |
| `DJANGO_ADMIN_URL` | Prefixo da URL do painel administrativo (obfuscação de rotas) | `admin/` | `admin/` | Rota customizada ou `admin/` | Não | Não | `gestao-clinica/` | `admin/` | `base.py` |

---

## 2. Banco de Dados Relacional

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `DATABASE_URL` | String de conexão com o banco relacional (dj-database-url) | Opcional (SQLite padrão) | SQLite em memória | PostgreSQL gerenciado | **SIM** | **SIM** | `postgres://app_user:senha_forte@db.cluster.internal:5432/mente_foco_prod` | SQLite local (`db.sqlite3`) em dev | `base.py`, `producao.py` |

---

## 3. Segurança HTTP, HTTPS, TLS e Proxy Reverso

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `DJANGO_SECURE_SSL_REDIRECT` | Redirecionamento forçado de conexões HTTP para HTTPS | `False` | `False` | `True` | **SIM** | Não | `True` | `True` em prod | `producao.py` |
| `DJANGO_SECURE_HSTS_SECONDS` | Tempo de cache da política HSTS no navegador | `0` | `0` | Rollout: `0` -> `300` -> `86400` -> `31536000` | Não | Não | `300` | `0` (seguro até validação TLS) | `producao.py` |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | Extensão da política HSTS para todos os subdomínios | `False` | `False` | `False` (ativar só com wildcard TLS) | Não | Não | `False` | `False` | `producao.py` |
| `DJANGO_SECURE_HSTS_PRELOAD` | Solicitação de inclusão na lista global de preload dos browsers | `False` | `False` | `False` (NUNCA ativar no dia 1) | Não | Não | `False` | `False` | `producao.py` |
| `DJANGO_SECURE_PROXY_SSL_HEADER` | Informa ao Django para confiar no header `X-Forwarded-Proto` | `False` | `False` | `True` se proxy terminar TLS | Depende do Proxy | Não | `True` | `False` | `producao.py` |
| `DJANGO_SECURE_CSP_REPORT_ONLY` | Alterna CSP entre modo de bloqueio e modo de relatório (diagnóstico) | `False` | `False` | `False` (ou `True` em staging) | Não | Não | `False` | `False` | `producao.py` |
| `TRUST_PROXY_CLIENT_IP` | Autoriza ler `X-Forwarded-For` para rate limiting | `False` | `False` | `True` SOMENTE se proxy sob controle sobrescrever o header | Depende do Proxy | Não | `True` | `False` | `base.py`, `rate_limit.py` |

---

## 4. Proteção contra Abuso e Rate Limiting (Prompt 17)

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `CONTACT_RATE_LIMIT_COUNT` | Quantidade máxima de submissões no formulário de contato | `5` | `5` | `5` | Não | Não | `5` | `5` | `base.py`, `rate_limit.py` |
| `CONTACT_RATE_LIMIT_WINDOW` | Janela de tempo em segundos para limite de contato | `900` (15 min) | `900` | `900` | Não | Não | `900` | `900` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_IP_LIMIT` | Limite de falhas de login administrativo por IP | `10` | `10` | `10` | Não | Não | `10` | `10` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_IP_WINDOW` | Janela de monitoramento de tentativas de login por IP | `900` | `900` | `900` | Não | Não | `900` | `900` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_IP_BLOCK` | Duração do bloqueio em segundos após estourar tentativas por IP | `900` | `900` | `900` | Não | Não | `900` | `900` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_COMBO_LIMIT` | Limite de falhas de login por combinação IP + Usuário | `5` | `5` | `5` | Não | Não | `5` | `5` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_COMBO_WINDOW` | Janela de monitoramento para IP + Usuário | `900` | `900` | `900` | Não | Não | `900` | `900` | `base.py`, `rate_limit.py` |
| `ADMIN_LOGIN_COMBO_BLOCK` | Duração do bloqueio para IP + Usuário | `900` | `900` | `900` | Não | Não | `900` | `900` | `base.py`, `rate_limit.py` |

---

## 5. Arquivos Estáticos e de Mídia

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `DJANGO_MANIFEST_STATIC_STORAGE` | Ativa `ManifestStaticFilesStorage` (nomes com hash para cache longo) | `False` | `False` | Opcional (`True` se build pipeline rodar collectstatic) | Não | Não | `True` | `False` | `producao.py` |

---

## 6. Serviço de E-mail Transacional (SMTP)

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `EMAIL_BACKEND` | Classe do backend de e-mail | `console.EmailBackend` | `locmem.EmailBackend` | `smtp.EmailBackend` | Não | Não | `django.core.mail.backends.smtp.EmailBackend` | `smtp.EmailBackend` em prod | `producao.py` |
| `EMAIL_HOST` | Host do servidor SMTP transacional | Vazio | Vazio | Host do provedor SMTP | Se usar e-mail | Não | `smtp.provedor.com.br` | String vazia | `producao.py` |
| `EMAIL_PORT` | Porta do servidor SMTP | `587` | `587` | `587` ou `465` | Se usar e-mail | Não | `587` | `587` | `producao.py` |
| `EMAIL_USE_TLS` | Habilitação de criptografia STARTTLS | `True` | `True` | `True` | Se usar e-mail | Não | `True` | `True` | `producao.py` |
| `EMAIL_HOST_USER` | Usuário/login de autenticação no SMTP | Vazio | Vazio | Usuário SMTP seguro | Se usar e-mail | **SIM** | `notificacoes@menteemfoco.com.br` | String vazia | `producao.py` |
| `EMAIL_HOST_PASSWORD` | Senha ou API Key do SMTP | Vazio | Vazio | Senha / App Password / Token | Se usar e-mail | **SIM** | `token_smtp_secreto_2026` | String vazia | `producao.py` |
| `DEFAULT_FROM_EMAIL` | Remetente padrão das mensagens automáticas | `webmaster@localhost` | `webmaster@localhost` | E-mail institucional verificado | Se usar e-mail | Não | `Instituto Mente em Foco <contato@menteemfoco.com.br>` | `webmaster@localhost` | `producao.py` |

---

## 7. SEO, Domínio e Governança LGPD

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `SITE_URL` | URL pública canônica (usada em sitemaps, Open Graph e links absolutos) | `http://localhost:8000` | `http://testserver` | `https://menteemfoco.com.br` | **SIM** | Não | `https://menteemfoco.com.br` | `http://localhost:8000` | `base.py` |
| `SEO_ALLOW_INDEXING` | Chave mestra de indexação de buscadores (Google, Bing) | `False` | `False` | `False` (antes do go-live) -> `True` (após validação completa) | **SIM** | Não | `False` (pré-lançamento) | `False` | `base.py`, `SEOMiddleware` |
| `GOOGLE_SITE_VERIFICATION` | Código de verificação do Google Search Console | Vazio | Vazio | Token fornecido pelo Google | Não | Não | `google_token_exemplo_abc123` | String vazia | `base.py` |
| `BING_SITE_VERIFICATION` | Código de verificação do Bing Webmaster Tools | Vazio | Vazio | Token fornecido pela Microsoft | Não | Não | `bing_token_exemplo_xyz789` | String vazia | `base.py` |
| `CONTATO_RETENCAO_DIAS` | Prazo em dias para expiração de mensagens de contato (LGPD) | Vazio | Vazio | Número inteiro (ex: 90 ou 180) | Não | Não | `90` | `None` (sem deleção automática) | `base.py` |

---

## 8. Dados Institucionais do Cliente

| Nome da Variável | Finalidade | Dev | Test | Produção | Obrigatória em Prod? | É Segredo? | Exemplo Sintético Seguro | Default Seguro no Código | Origem / Arquivo |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| `WHATSAPP_NUMERO` | Número de WhatsApp oficial para link direto | `PENDENTE_DEFINICAO` | `PENDENTE_DEFINICAO` | Número oficial internacional | **SIM (para go-live)** | Não | `5561999999999` | `PENDENTE_DEFINICAO` | `base.py` |
| `EMAIL_CONTATO` | Endereço de e-mail institucional público | `PENDENTE_DEFINICAO` | `PENDENTE_DEFINICAO` | E-mail de atendimento da clínica | **SIM (para go-live)** | Não | `contato@menteemfoco.com.br` | `PENDENTE_DEFINICAO` | `base.py` |
| `INSTAGRAM_URL` | Link do perfil oficial do Instagram | `PENDENTE_DEFINICAO` | `PENDENTE_DEFINICAO` | URL do perfil profissional | Não | Não | `https://instagram.com/psimari.menezes` | `PENDENTE_DEFINICAO` | `base.py` |
| `CRP_PROFISSIONAL` | Registro profissional perante o CRP | `PENDENTE_DEFINICAO` | `PENDENTE_DEFINICAO` | Registro profissional oficial | **SIM (OBRIGATÓRIO CFP/CRP)** | Não | `CRP 01/12345` | `PENDENTE_DEFINICAO` | `base.py` |
