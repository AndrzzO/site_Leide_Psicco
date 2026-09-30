# Plano de Backup, Retenção e Restauração de Dados
**Projeto:** Instituto Mente em Foco  
**Data:** 28/09/2026  
**Status:** Baseline Operacional Proposto — Pendente de Aprovação e Alinhamento com o Provedor Cloud Final  
**Conformidade:** LGPD (Lei Geral de Proteção de Dados) e Boas Práticas Operacionais

---

## 1. Princípios e Regras Fundamentais de Segurança

1. **O Git NÃO é Backup:** O repositório Git armazena exclusivamente código-fonte; dados dinâmicos do banco e uploads de mídia devem possuir rotinas próprias e isoladas.
2. **Backups NUNCA na Webroot:** É **estritamente proibido** salvar arquivos de backup dentro de pastas públicas como `static/`, `media/`, `public/` ou `staticfiles/`.
3. **Backups NUNCA no Repositório:** Arquivos `.sql`, `.dump`, `.tar.gz` ou snapshots com dados reais jamais devem ser commitados no Git (garantido pelas regras do `.gitignore`).
4. **Backup não testado não é backup:** A rotina deve prever testes periódicos de restauração em ambiente isolado (sandbox), nunca sobre a base produtiva em execução.
5. **Privacidade e LGPD:** Os backups do banco contêm mensagens de contato com dados pessoais (nome, e-mail, telefone). A retenção dos backups não pode ser indeterminada e os arquivos devem ser criptografados em repouso.

---

## 2. Escopo do que Deve Ser Protegido

| Ativo de Dados | Localização Primária | Conteúdo | Criticidade |
|:---|:---|:---|:---:|
| **Banco de Dados (PostgreSQL)** | Cluster Relacional de Produção | Artigos do Blog, Áreas Clínicas, Cadastros de Profissionais, Mensagens de Contato e Configurações Globais | **MÁXIMA** |
| **Arquivos de Mídia (`media/`)** | Volume Persistente ou Object Storage | Fotos oficiais da psicóloga Mari Menezes, fotos de atendimentos e imagens de capa de artigos | **ALTA** |
| **Segredos e Configuração** | Gerenciador de Segredos da Nuvem / `.env` seguro | `DJANGO_SECRET_KEY`, credenciais do banco e tokens de SMTP | **ALTA** |

---

## 3. Metas Operacionais de Resiliência (RPO e RTO)

> [!NOTE]
> Os valores abaixo representam a linha de base técnica recomendada para o Instituto Mente em Foco, pendentes de aprovação formal do cliente.

- **RPO (Recovery Point Objective):** **24 horas.**  
  Em caso de incidente grave ou falha de hardware, a perda máxima de dados tolerável é de 1 dia de operações.
- **RTO (Recovery Time Objective):** **2 horas.**  
  Tempo máximo estimado para restabelecer a infraestrutura, importar o dump do banco e restaurar os arquivos de mídia.

---

## 4. Política de Retenção e Armazenamento

- **Frequência de Execução:** Diária, durante a madrugada (horário de menor tráfego, ex: 03:00 UTC-3).
- **Janela de Retenção de Backups:**
  - Backups diários: mantidos por **14 dias**.
  - Backups semanais (domingos): mantidos por **4 semanas**.
  - Backups com mais de 30 dias: eliminados automaticamente para conformidade com a LGPD e minimização de dados.
- **Local de Armazenamento:** Storage secundário isolado (ex: bucket com bloqueio de acesso público e criptografia SSE-AES256 em região diferente do servidor principal).

---

## 5. Procedimento de Extração (Backup)

### 5.1 Backup do PostgreSQL (Formato Customizado Compactado)
Executado por rotina agendada (Cron / Task runner) ou snapshot automático do provedor gerenciado:
```bash
#!/bin/bash
set -e

DATA=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mente_foco"
BACKUP_FILE="${BACKUP_DIR}/mente_foco_${DATA}.dump"

mkdir -p "$BACKUP_DIR"

# Executa pg_dump com formato custom (-Fc) otimizado para pg_restore
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -Fc -Z 6 -f "$BACKUP_FILE"

# Encripta o backup antes do envio para o storage secundário (opcional / recomendado)
# gpg --symmetric --cipher-algo AES256 "$BACKUP_FILE"

echo "Backup do PostgreSQL concluído com sucesso: $BACKUP_FILE"
```

### 5.2 Backup dos Arquivos de Mídia
Se os arquivos estiverem em volume persistente local:
```bash
tar -czf "/var/backups/mente_foco/media_${DATA}.tar.gz" -C /app media/
```
Se estiver em Object Storage (S3/R2), deve-se ativar o recurso de **Bucket Versioning** e regras de ciclo de vida nativas do provedor.

---

## 6. Procedimento de Restauração (Restore)

> [!CAUTION]
> NUNCA execute testes de restauração diretamente sobre o banco de dados de produção ativo. Utilize sempre uma base de dados limpa ou contêiner de testes temporário.

### Passo 1 — Preparação do Banco Alvo Limpo
```bash
# Conecte-se ao PostgreSQL com privilégios administrativos
psql -h $DB_HOST -U $DB_ADMIN -c "DROP DATABASE IF EXISTS mente_foco_restore_teste;"
psql -h $DB_HOST -U $DB_ADMIN -c "CREATE DATABASE mente_foco_restore_teste OWNER $DB_USER;"
```

### Passo 2 — Execução do `pg_restore`
```bash
# Restaura o schema e dados a partir do arquivo .dump
pg_restore -h $DB_HOST -U $DB_USER -d mente_foco_restore_teste -v --no-owner --no-privileges "/caminho/do/backup/mente_foco_2026xxxx.dump"
```

### Passo 3 — Restauração dos Arquivos de Mídia
```bash
# Descompacta os arquivos na pasta de destino de mídia
tar -xzf "/caminho/do/backup/media_2026xxxx.tar.gz" -C /app/
```

### Passo 4 — Validação de Integridade Pós-Restauração
1. Conectar a aplicação temporária apontando para a base restaurada:
   ```bash
   DATABASE_URL="postgres://$DB_USER:$DB_PASS@$DB_HOST:5432/mente_foco_restore_teste" python manage.py check
   ```
2. Executar contagem de sanidade dos modelos no Django Shell:
   ```python
   python manage.py shell -c "from nucleo.models import Profissional, AreaAtuacao; from conteudos.models import Artigo; print('Profissionais:', Profissional.objects.count()); print('Áreas:', AreaAtuacao.objects.count()); print('Artigos:', Artigo.objects.count())"
   ```
3. Acessar o endpoint `/health/ready/` para confirmar resposta HTTP 200 `OK`.

---

## 7. Cronograma de Testes de Recuperação de Desastres

- **Teste Inicial de Restauração:** Deve ser executado imediatamente antes do lançamento público oficial (Go-Live).
- **Testes Recorrentes:** A cada **6 meses**, um exercício de recuperação simulada deve ser executado em ambiente de homologação para garantir que os arquivos de backup continuam íntegros e que o procedimento de restore permanece funcional.
