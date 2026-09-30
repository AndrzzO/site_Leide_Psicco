# Checklist de Go-Live e Publicação Oficial
**Projeto:** Instituto Mente em Foco  
**Data:** 28/09/2026  
**Responsável:** Equipe Técnica / Coordenação do Projeto  
**Objetivo:** Roteiro de portões de decisão (Gates) para validação pré-deploy, lançamento oficial e monitoramento operacional inicial.

---

## 1. Fase 1 — Antes do Deploy (Pré-Requisitos e Gates)

> [!IMPORTANT]
> Todos os itens desta seção devem estar marcados como `[X]` antes de disparar o deploy em ambiente de produção.

### 1.1 Código e Qualidade
- [ ] Commit aprovado na branch principal (`main`).
- [ ] Working tree do Git completamente limpa, sem arquivos temporários ou modificações locais não rastreadas.
- [ ] Suíte de 232 testes automatizados executada e 100% aprovada (`Ran 232 tests in ... OK`).
- [ ] Verificação de migrações limpa: `python manage.py makemigrations --check` retornando *No changes detected*.
- [ ] Verificação de dependências do Python limpa: `python -m pip check` sem erros.
- [ ] Nenhuma rota Windows ou letra de unidade (`C:\`, `D:\`) hardcoded no código ou templates.
- [ ] Case-sensitivity de 100% dos arquivos estáticos e templates validada para ambiente Linux.

### 1.2 Infraestrutura e Segurança
- [ ] Provedor de hospedagem selecionado e provisionado (consulte `DECISOES_DE_INFRAESTRUTURA.md`).
- [ ] Cluster PostgreSQL de produção provisionado e acessível via string `DATABASE_URL`.
- [ ] Volume persistente para `/app/media/` ou Object Storage (S3/R2) configurado (proibido filesystem efêmero para mídia).
- [ ] Certificado SSL/TLS válido e ativo para o domínio oficial.
- [ ] Variáveis de ambiente configuradas no painel da infraestrutura (consulte `MATRIZ_VARIAVEIS_AMBIENTE.md`).
- [ ] `DJANGO_SECRET_KEY` aleatória e forte (>50 caracteres) injetada exclusivamente via environment.
- [ ] `DJANGO_DEBUG=False` rigorosamente configurado em produção.
- [ ] `DJANGO_ALLOWED_HOSTS` estrito com os domínios oficiais, sem asterisco wildcard `*`.
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` configurado com os esquemas `https://` correspondentes.
- [ ] `SEO_ALLOW_INDEXING=False` mantido para evitar indexação durante os testes de homologação.

### 1.3 Conteúdo e Conformidade do Cliente
- [ ] Fotografias oficiais e definitivas da psicóloga Mari Menezes fornecidas e validadas.
- [ ] Número de inscrição do CRP validado e inserido na configuração institucional.
- [ ] Telefone de WhatsApp e e-mail institucional oficial validados.
- [ ] Texto da Política de Privacidade revisado perante as práticas reais da clínica e LGPD.
- [ ] Nenhum texto de rascunho, "Lorem Ipsum" ou placeholder de desenvolvimento visível nas páginas públicas.

---

## 2. Fase 2 — Execução do Deploy

- [ ] Instalação limpa das dependências: `pip install -r requirements.txt` e `psycopg`.
- [ ] Backup preventivo de banco de dados executado (se houver dados preexistentes).
- [ ] Aplicação de migrações executada com sucesso: `python manage.py migrate --noinput`.
- [ ] Coleta de arquivos estáticos executada com sucesso: `python manage.py collectstatic --noinput`.
- [ ] Inicialização do servidor WSGI (Gunicorn) através do comando padrão de produção.
- [ ] Proxy reverso (Nginx/Edge) roteando requisições com `X-Forwarded-Proto: https`.

---

## 3. Fase 3 — Pós-Deploy e Homologação Fechada (Smoke Test)

- [ ] Sonda `/health/` responde HTTP 200 `OK`.
- [ ] Sonda `/health/ready/` responde HTTP 200 `OK` (confirmando conexão com PostgreSQL).
- [ ] Redirecionamento HTTP -> HTTPS funcionando sem loop de redirecionamento.
- [ ] Headers de segurança presentes: `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`.
- [ ] Carregamento sem falhas das páginas essenciais no navegador:
  - [ ] Home (`/`)
  - [ ] Sobre Mim (`/sobre-mim/`)
  - [ ] Áreas de Atuação (`/servicos/psicologia/`, `/servicos/neuropsicologia/`, `/servicos/traumas/`, etc.)
  - [ ] Blog / Conteúdos (`/conteudos/` e artigo de leitura)
  - [ ] Contato (`/contato/`)
  - [ ] Política de Privacidade (`/politica-de-privacidade/`)
- [ ] Console do navegador com zero erro de script e zero bloqueio de CSP.
- [ ] Aba Rede (Network) do navegador com zero erro 404 para CSS, JS, fontes e imagens.
- [ ] Criação interativa do superusuário do Django Admin: `python manage.py createsuperuser`.
- [ ] Login administrativo testado com sucesso no painel.
- [ ] Um único teste autorizado de envio de formulário de contato realizado e validado no Admin.

---

## 4. Fase 4 — Go-Live Oficial (Abertura ao Público e Indexação)

- [ ] Todos os itens das Fases 1, 2 e 3 aprovados sem exceção.
- [ ] Virada de chave de SEO: definir `SEO_ALLOW_INDEXING=True` no ambiente de produção.
- [ ] Reinicialização suave dos workers da aplicação.
- [ ] Validação do `robots.txt` em `https://dominio.com.br/robots.txt`:
  - Deve conter `User-agent: *` e `Allow: /`.
  - Deve apontar para o `Sitemap: https://dominio.com.br/sitemap.xml`.
- [ ] Validação do `sitemap.xml` no navegador (confirmar URLs canônicas em HTTPS e ausência de rotas privadas).
- [ ] Submissão do sitemap no Google Search Console e Bing Webmaster Tools.
- [ ] Ativação do monitoramento de uptime externo apontando para `/health/`.

---

## 5. Fase 5 — Primeiras 24 Horas de Operação

- [ ] Acompanhamento contínuo dos logs de erro do servidor (garantir ausência de erros 500).
- [ ] Verificação de erros 404 nos logs (identificar eventuais links quebrados ou requisições malformadas).
- [ ] Confirmação de recebimento de mensagens reais de contato pelo painel administrativo.
- [ ] Monitoramento de uso de CPU, memória RAM e limites de conexões no PostgreSQL.
- [ ] Verificação da integridade das imagens recém-carregadas pelo CMS na pasta persistente de mídia.

---

## 6. Fase 6 — Primeira Semana de Operação

- [ ] Validação do primeiro ciclo completo de backup automatizado diário.
- [ ] Teste de restauração simulada do backup em ambiente isolado (consulte `PLANO_BACKUP_E_RESTAURACAO.md`).
- [ ] Verificação do status de indexação e rastreamento no Google Search Console.
- [ ] Avaliação do rollout de HSTS: se o HTTPS permaneceu 100% estável, elevar `DJANGO_SECURE_HSTS_SECONDS` de `300` para `86400` (1 dia).
- [ ] Revisão dos relatórios de Core Web Vitals reais coletados de usuários (Chrome User Experience Report / PageSpeed).
