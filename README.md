# INSTITUTO MENTE EM FOCO — WEBSITE INSTITUCIONAL

Website institucional e profissional do **Instituto Mente em Foco**, sob responsabilidade técnica da **Psicóloga Mari Menezes**. O projeto é construído com arquitetura Django Server-Side Rendering (SSR), focada em alta sofisticação editorial, segurança, clareza, acessibilidade (WCAG 2.1 AA) e conformidade estrita com o Código de Ética Profissional do Psicólogo (CFP) e a LGPD.

---

## 1. CONCEITO E IDENTIDADE
* **Princípio Central:** `COMPREENDER • CUIDAR • RECONSTRUIR`
* **Assinatura Institucional:** *"Psicologia e Neuropsicologia para compreender a mente, cuidar das emoções e construir novos caminhos."*
* **Assinatura Emocional:** *"Sua história merece ser compreendida."*
* **Stack Principal:** Python 3.14+ / Django 6.0+ / HTML5 Semântico / CSS Moderno (Design Tokens) / Vanilla JavaScript.

---

## 2. REQUISITOS DO SISTEMA
* **Python:** 3.11 ou superior (desenvolvido e testado em Python 3.14.5).
* **Gerenciador de Pacotes:** `pip`.
* **Banco de Dados:**
  * Desenvolvimento: SQLite 3 (incluso nativamente no Python).
  * Produção: PostgreSQL 14+ (preparado via `dj-database-url`).
* **Git:** Para controle de versão (opcional em ambiente local).

---

## 3. INSTALAÇÃO E CONFIGURAÇÃO LOCAL

### 3.1 Clonar ou Acessar o Diretório
```bash
cd SiteDjangoLeide
```

### 3.2 Criar e Ativar o Ambiente Virtual

* **No Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

* **No Windows (Prompt de Comando CMD):**
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

* **No Linux / macOS (Bash / Zsh):**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3.3 Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3.4 Configurar Variáveis de Ambiente (.env)
Copie o arquivo de exemplo [.env.example](file:///c:/Users/andre/Documents/SiteDjangoLeide/.env.example) para `.env`:

* **No Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
* **No Linux / macOS:**
  ```bash
  cp .env.example .env
  ```

> [!WARNING]
> **AVISO DE SEGURANÇA:** O arquivo `.env` contém credenciais e segredos locais e já está configurado no `.gitignore`. **NUNCA** faça commit nem envie o arquivo `.env` com dados reais ou chaves de produção para o repositório Git.

### 3.5 Executar Migrações do Banco de Dados
```bash
python manage.py migrate
```

### 3.6 Executar a Suíte de Testes Automatizados
```bash
python manage.py test
```

### 3.7 Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```
Acesse a aplicação em seu navegador:
* Página Inicial (Fundação): `http://localhost:8000/`
* Verificação de Liveness: `http://localhost:8000/health/` (retorna HTTP 200 `{"status": "ok"}`)
* Verificação de Readiness (com probe de banco de dados): `http://localhost:8000/health/ready/` (retorna HTTP 200 `{"status": "ready", "database": "connected"}` ou HTTP 503)
* Painel Administrativo: `http://localhost:8000/admin/`

---

## 4. ESTRUTURA DE SETTINGS POR AMBIENTE

O projeto adota a separação explícita de configurações por ambiente:

```
configuracoes/settings/
├── __init__.py           # Exporta desenvolvimento por padrão
├── base.py               # Configurações compartilhadas, apps, i18n, tokens, templates
├── desenvolvimento.py    # DEBUG=True, SQLite local, console de e-mails
└── producao.py           # DEBUG=False, validação estrita de SECRET_KEY e ALLOWED_HOSTS, SSL/HSTS
```

Para alternar entre ambientes, ajuste a variável `DJANGO_SETTINGS_MODULE` no arquivo `.env`:
* Desenvolvimento: `DJANGO_SETTINGS_MODULE=configuracoes.settings.desenvolvimento`
* Produção: `DJANGO_SETTINGS_MODULE=configuracoes.settings.producao`

---

## 5. DOCUMENTAÇÃO TÉCNICA, SEGURANÇA E PRIVACIDADE (LGPD)
Todos os contratos, diretrizes, inventários e documentos de governança do projeto estão centralizados na pasta [documentacao](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao):
* [AUDITORIA_PRONTIDAO_PRODUCAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_PRONTIDAO_PRODUCAO.md)
* [MATRIZ_VARIAVEIS_AMBIENTE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MATRIZ_VARIAVEIS_AMBIENTE.md)
* [DECISOES_DE_INFRAESTRUTURA.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/DECISOES_DE_INFRAESTRUTURA.md)
* [GUIA_DEPLOY_PRODUCAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/GUIA_DEPLOY_PRODUCAO.md)
* [CHECKLIST_GO_LIVE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/CHECKLIST_GO_LIVE.md)
* [PLANO_BACKUP_E_RESTAURACAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PLANO_BACKUP_E_RESTAURACAO.md)
* [PLANO_ROLLBACK.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PLANO_ROLLBACK.md)
* [AUDITORIA_FUNCIONAL_COMPLETA.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_FUNCIONAL_COMPLETA.md)
* [MATRIZ_DE_FLUXOS_FUNCIONAIS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MATRIZ_DE_FLUXOS_FUNCIONAIS.md)
* [INVENTARIO_DE_ROTAS_E_LINKS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/INVENTARIO_DE_ROTAS_E_LINKS.md)
* [AUDITORIA_DA_SUITE_DE_TESTES.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_DA_SUITE_DE_TESTES.md)
* [MATRIZ_DE_TESTES.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MATRIZ_DE_TESTES.md)
* [ESTRATEGIA_DE_TESTES.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/ESTRATEGIA_DE_TESTES.md)
* [GUIA_DE_REGRESSAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/GUIA_DE_REGRESSAO.md)
* [CONTEXTO_MESTRE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/CONTEXTO_MESTRE.md)
* [ARQUITETURA_PLANEJADA.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/ARQUITETURA_PLANEJADA.md)
* [MAPA_DE_PAGINAS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MAPA_DE_PAGINAS.md)
* [PROTECAO_CONTRA_ABUSO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PROTECAO_CONTRA_ABUSO.md)
* [MATRIZ_DE_RATE_LIMIT.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MATRIZ_DE_RATE_LIMIT.md)
* [GUIA_DE_INCIDENTES_DE_ABUSO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/GUIA_DE_INCIDENTES_DE_ABUSO.md)
* [AUDITORIA_DE_ABUSO_E_RATE_LIMIT.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_DE_ABUSO_E_RATE_LIMIT.md)
* [SEGURANCA_E_HARDENING.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/SEGURANCA_E_HARDENING.md)
* [AUDITORIA_DE_SEGURANCA.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_DE_SEGURANCA.md)
* [INVENTARIO_DE_SECRETS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/INVENTARIO_DE_SECRETS.md)
* [CHECKLIST_DE_SEGURANCA_PRODUCAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/CHECKLIST_DE_SEGURANCA_PRODUCAO.md)
* [SEO_TECNICO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/SEO_TECNICO.md)
* [AUDITORIA_SEO_TECNICO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_SEO_TECNICO.md)
* [AUDITORIA_DE_ACESSIBILIDADE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/AUDITORIA_DE_ACESSIBILIDADE.md)
* [PERFORMANCE_E_CORE_WEB_VITALS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PERFORMANCE_E_CORE_WEB_VITALS.md)
* [MAPA_DE_DADOS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/MAPA_DE_DADOS.md)
* [TERCEIROS_E_COOKIES.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/TERCEIROS_E_COOKIES.md)
* [INVENTARIO_DE_IMAGENS.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/INVENTARIO_DE_IMAGENS.md)
* [CHECKLIST_DE_QUALIDADE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/CHECKLIST_DE_QUALIDADE.md)
* [PENDENCIAS_DO_CLIENTE.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/PENDENCIAS_DO_CLIENTE.md)
* [HISTORICO_DE_IMPLEMENTACAO.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/HISTORICO_DE_IMPLEMENTACAO.md)
* [GUIA_DO_ADMIN.md](file:///c:/Users/andre/Documents/SiteDjangoLeide/documentacao/GUIA_DO_ADMIN.md)

---

## 6. COMANDOS ÚTEIS DE GOVERNANÇA, TESTES E OPERAÇÃO

* **Executar suíte completa de testes automatizados (234 testes):**
  ```bash
  python manage.py test
  ```
* **Executar testes de regressão específicos:**
  ```bash
  python manage.py test nucleo.tests_regressao
  ```
* **Verificação preventiva de integridade e sistema:**
  ```bash
  python manage.py check
  ```
* **Verificação de modelos e ausência de migrações pendentes:**
  ```bash
  python manage.py makemigrations --check
  ```
* **Verificação de integridade das dependências pip:**
  ```bash
  python -m pip check
  ```
* **Auditoria de segurança pré-deploy do Django:**
  ```bash
  python manage.py check --deploy
  ```
* **Simulação de retenção de contatos (Dry-run):**
  ```bash
  python manage.py limpar_contatos_expirados --dias 180 --dry-run
  ```
* **Execução de limpeza de contatos expirados (conforme período configurado):**
  ```bash
  python manage.py limpar_contatos_expirados
  ```


