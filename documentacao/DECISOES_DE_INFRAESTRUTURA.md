# Decisões de Infraestrutura e Pendências Arquiteturais
**Projeto:** Instituto Mente em Foco  
**Data:** 28/09/2026  
**Status:** Mapeamento de Opções e Recomendações — Nenhuma contratação ou presunção automática de provedor realizada.

---

## 1. Visão Geral

Este documento cataloga as decisões de infraestrutura pendentes para o lançamento do projeto em produção.  
O código e as configurações foram estruturados de forma **100% agnóstica a provedor**, permitindo que o cliente ou a equipe de operações escolha a opção mais econômica e confiável sem necessidade de refatorações de backend.

---

## 2. Inventário de Decisões

### Decisão 01: Nome de Domínio Oficial e DNS
- **Estado:** **PENDENTE**
- **Opções:** 
  1. Domínio `.com.br` registrado no Registro.br (ex: `institutomenteemfoco.com.br` ou `marimenezespsicologia.com.br`).
  2. Domínio internacional `.com`.
- **Origem Canônica:** Recomenda-se escolher **Apex** (`https://dominio.com.br`) ou **WWW** (`https://www.dominio.com.br`), com redirecionamento 301 automático na borda (DNS/Proxy).
- **Pendência:** Aguardando definição e aquisição do domínio pelo cliente.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 02: Plataforma de Hospedagem / Execução
- **Estado:** **PENDENTE**
- **Opções:**
  - **Opção A (PaaS Gerenciada - Recomendada para facilidade operacional):** Render, Railway, Fly.io ou DigitalOcean App Platform. Provisiona HTTPS automático, deploy via Git e reinicialização automática de processos.
  - **Opção B (VPS Linux Dedicada - Recomendada para custo fixo baixo em reais):** Hetzner Cloud, DigitalOcean Droplet ou Linode/Akamai com Ubuntu 24.04 LTS, Nginx e Systemd.
- **Recomendação Técnica:** PaaS moderna (como Render ou Railway) para dispensar manutenção manual de SO, patches de segurança e certificados TLS.
- **Pendência:** Definição orçamentária e preferência do cliente.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 03: Banco de Dados Relacional (PostgreSQL)
- **Estado:** **PENDENTE**
- **Opções:**
  1. PostgreSQL Gerenciado pela plataforma de nuvem (Render PostgreSQL, Neon, Supabase ou AWS RDS) com backups automáticos diários.
  2. PostgreSQL instalado localmente na VPS Linux (se a Opção B de hospedagem for adotada).
- **Versão Alvo:** PostgreSQL 15, 16 ou 17.
- **Driver:** `psycopg` (v3), 100% compatível com Django 6.0 e Python 3.14.
- **Conexão:** Fornecida estritamente via variável `DATABASE_URL`.
- **Pendência:** Provisionamento do cluster do banco de produção.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 04: Armazenamento Persistente de Mídia (Media Storage)
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Volume Persistente (Disk/Storage Mount):** Montagem de disco persistente no caminho `/app/media/`. Adequado para monólito ou VPS.
  2. **Object Storage Gerenciado (S3 / Cloudflare R2 / Backblaze B2):** Desacopla arquivos de mídia do servidor de aplicação. Custo irrisório para o volume do site.
- **Alerta Crítico:** Servidores PaaS (Render, Heroku, etc.) possuem **filesystem efêmero**. Subir arquivos na pasta local sem volume persistente causará a exclusão das imagens a cada reinício ou deploy.
- **Pendência:** Escolha entre montagem de volume persistente ou ativação de bucket S3/R2.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 05: Estratégia de Entrega de Arquivos Estáticos (Static Files)
- **Estado:** **PENDENTE**
- **Opções:**
  1. **WhiteNoise:** Pacote Python amplamente utilizado no ecossistema Django. Serve arquivos estáticos compactados diretamente pelo WSGI com headers de cache agressivos.
  2. **Nginx (Proxy Reverso):** Nginx mapeia `/static/` diretamente para o diretório `staticfiles/` no disco com `gzip`/`brotli` ativado.
  3. **CDN / Object Storage:** Upload dos arquivos coletados via `collectstatic` para CDN de borda.
- **Recomendação Técnica:** Se PaaS, `WhiteNoise` oferece a integração mais rápida e robusta. Se VPS, Nginx estático dedicado.
- **Pendência:** Alinhamento com a plataforma de hospedagem escolhida.
- **Bloqueia Go-Live?** Não bloqueia deploy técnico; deve ser testado com `collectstatic`.

### Decisão 06: Servidor de Aplicação WSGI
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Gunicorn (`gunicorn configuracoes.wsgi:application`):** Servidor WSGI padrão para ambientes Linux.
  2. **uWSGI:** Servidor C de alta performance, mais complexo de configurar.
- **Recomendação Técnica:** Gunicorn com 2 a 3 workers síncronos (adequado para tráfego institucional com baixo consumo de memória).
- **Proibição Absoluta:** O utilitário `manage.py runserver` é **estritamente proibido** em produção.
- **Pendência:** Definição do comando de inicialização no Procfile / Dockerfile / Systemd.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 07: Proxy Reverso e Terminação TLS/HTTPS
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Proxy da Plataforma PaaS:** Cloudflare / Traefik gerenciado pelo provedor, encerrando TLS e encaminhando tráfego HTTP com `X-Forwarded-Proto: https`.
  2. **Nginx com Certbot / Let's Encrypt:** Na VPS, renovação automática a cada 90 dias via cron/systemd timer.
- **Configuração no Django:** Quando o proxy encerrar o TLS, ativar `DJANGO_SECURE_PROXY_SSL_HEADER=True` para que o Django identifique conexões seguras e evite loops de redirecionamento.
- **Pendência:** Definição da camada de rede.
- **Bloqueia Go-Live?** **SIM.**

### Decisão 08: Cache e Rate Limiting Distribuído
- **Estado:** **PENDENTE**
- **Opções:**
  1. **LocMemCache (Mono-processo / Multi-thread):** Suficiente se a aplicação rodar em um único processo worker. Em múltiplos workers independentes, cada processo mantém contadores isolados.
  2. **Redis Compartilhado:** Garante contadores atômicos de rate limiting para qualquer quantidade de workers.
  3. **Rate Limiting no Reverse Proxy / WAF:** Nginx (`limit_req_zone`) ou Cloudflare Rate Limiting Rules na borda antes de atingir a aplicação.
- **Recomendação Técnica:** Para a escala institucional da clínica (baixo volume de requisições concorrentes), proteção na borda (Cloudflare) ou Redis gerenciado básico.
- **Pendência:** Avaliação de custo/benefício da adição de um Redis gerenciado.
- **Bloqueia Go-Live?** Não. O sistema opera com fallback seguro no `LocMemCache`.

### Decisão 09: Serviço de E-mail Transacional (SMTP)
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Provedor Especializado (Recomendado):** Resend, Brevo (ex-Sendinblue), Amazon SES ou Mailgun. Garantem alta entregabilidade e conformidade com SPF/DKIM/DMARC.
  2. **SMTP do Provedor de E-mail Corporativo:** Google Workspace ou Microsoft 365 com senha de aplicativo (App Password).
- **Observação de Arquitetura:** O formulário de contato **sempre** salva a mensagem no banco de dados primeiro. O envio de e-mail é uma notificação secundária; falhas de SMTP não quebram a gravação da mensagem.
- **Pendência:** Contratação de serviço de SMTP ou fornecimento de credenciais de e-mail pela cliente.
- **Bloqueia Go-Live?** Não bloqueia go-live se o cliente aceitar acompanhar mensagens pelo painel administrativo.

### Decisão 10: Estratégia de Backup e RPO/RTO
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Snapshots Automáticos do Provedor:** Backup diário do banco gerenciado com retenção de 7 a 30 dias e point-in-time recovery (PITR).
  2. **Rotina com `pg_dump`:** Script diário criptografado enviado para storage externo secundário.
- **RPO Alvo (Recovery Point Objective):** Máximo de 24 horas.
- **RTO Alvo (Recovery Time Objective):** Máximo de 2 horas para restauração completa.
- **Pendência:** Aprovação formal do plano de backup pelo cliente.
- **Bloqueia Go-Live?** **SIM (Operacional).**

### Decisão 11: Monitoramento de Uptime e Erros
- **Estado:** **PENDENTE**
- **Opções:**
  1. **Monitoramento de Uptime Externo (Gratuito/Freemium):** Uptime Kuma, Better Stack, Freshping ou UptimeRobot sondando a rota `/health/` a cada 1 a 5 minutos.
  2. **Rastreamento de Erros de Aplicação (Opcional Futuro):** Sentry ou GlitchTip para notificação de exceções em tempo real.
- **Pendência:** Ativação do monitoramento após a publicação do domínio oficial.
- **Bloqueia Go-Live?** Não.
