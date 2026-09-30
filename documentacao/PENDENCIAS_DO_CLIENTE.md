# PENDÊNCIAS DO CLIENTE — INSTITUTO MENTE EM FOCO
**REGISTRO DE INFORMAÇÕES, ATIVOS E DADOS PENDENTES DE DEFINIÇÃO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

---

## 1. DIRETRIZ ABSOLUTA DE NÃO-BLOQUEIO

A ausência das informações e ativos listados abaixo **NÃO IRÁ BLOQUEAR O DESENVOLVIMENTO TÉCNICO** do site.

* Todas as informações pendentes serão representadas no código-fonte por constantes padronizadas no formato:
  $$\text{PENDENTE\_DEFINICAO}$$
* Todas as fotografias e marcas ausentes utilizarão **placeholders proporcionais elegantes**.
* **REGRA ÉTICA E CONTRATUAL INEGOCIÁVEL:** É estritamente proibido inventar dados cadastrais, números de telefone, endereços, registros de CRP ou depoimentos fictícios.

---

## 2. MATRIZ DE PENDÊNCIAS E STATUS

> [!NOTE]
> Todos os itens abaixo já possuem campos e validadores correspondentes implementados no Django Admin (`ConfiguracaoSite` e `Profissional`). Assim que forem fornecidos, poderão ser inseridos diretamente pelo painel administrativo sem necessidade de alteração de código.

| Item / Dado Pendente | Impacto no Projeto | Solução Temporária no Código / Template | Status Atual |
| :--- | :--- | :--- | :--- |
| **Logo Vetorial Oficial** | Identidade visual no Header e Footer | Placeholder SVG com tipografia institucional e símbolo minimalista | `PENDENTE_DEFINICAO` |
| **Favicon & Web Clip** | Aba do navegador e marcadores | Símbolo minimalista temporário em SVG/ICO | `PENDENTE_DEFINICAO` |
| **Foto Oficial de Mari Menezes (Hero)** | Bloco principal da Home (Hero) | Placeholder com aspecto `~4:5` (`IMG-001`) | `PENDENTE_DEFINICAO` |
| **Foto Oficial de Mari Menezes (Sobre)** | Página Sobre Mim | Placeholder com aspecto `~4:5` (`IMG-010`) | `PENDENTE_DEFINICAO` |
| **Fotografias das Áreas de Atuação** | 5 cards na Home e topos das páginas internas | Placeholders com aspecto `~4:3` e `~16:9` (`IMG-003` a `IMG-007`) | `PENDENTE_DEFINICAO` |
| **Fotografia Botânica da Home** | Seção "Alguns momentos..." | Placeholder com aspecto `~1:1` (`IMG-002`) | `PENDENTE_DEFINICAO` |
| **Número de WhatsApp Oficial** | Link de conversão nos CTAs e botão flutuante | Constante `WHATSAPP_NUMERO = ""` (link gerado dinamicamente via context processor com aviso condicional) | `PENDENTE_DEFINICAO` |
| **E-mail Institucional Oficial** | Rodapé e canal do formulário de contato | Constante `EMAIL_CONTATO = "PENDENTE_DEFINICAO"` | `PENDENTE_DEFINICAO` |
| **Perfil Oficial do Instagram** | Ícone e link no rodapé | Constante `INSTAGRAM_URL = "PENDENTE_DEFINICAO"` | `PENDENTE_DEFINICAO` |
| **Registro Profissional (CRP)** | Rodapé institucional e página Sobre Mim (obrigatório pelo CFP) | Tag condicional: exibe `CRP: PENDENTE_DEFINICAO` apenas em ambiente de testes ou suprime até fornecimento | `PENDENTE_DEFINICAO` |
| **Endereço Físico do Consultório** | Rodapé e página de Contato | Texto condicional informando atendimento online ou consultório físico | `PENDENTE_DEFINICAO` |
| **Modalidades de Atendimento** | Descrição clara se o atendimento é estritamente online, presencial ou híbrido | Texto neutro adaptado focado na disponibilidade de acolhimento | `PENDENTE_DEFINICAO` |
| **Formação Acadêmica e Títulos** | Página Sobre Mim (graduação, pós-graduação, instituições reais) | Manter apenas o posicionamento fornecido ("Psicóloga, palestrante e facilitadora de grupos") sem inventar faculdades | `PENDENTE_DEFINICAO` |
| **Revisão Jurídica da Política de Privacidade e Cookies** | Páginas `/privacidade/` e `/cookies/` | Minuta técnica factual com 14 seções e tabela de cookies essenciais implementadas; aguarda validação formal por assessoria jurídica | `PENDENTE_DEFINICAO` |
| **Prazo Institucional de Retenção de Mensagens** | Parâmetro `CONTATO_RETENCAO_DIAS` | Mecanismo técnico configurável e comando de expurgo implementados; aguarda definição de prazo formal (ex: 180 dias) | `PENDENTE_DEFINICAO` |
| **Canal Específico para Direitos do Titular (Privacidade/DPO)** | Atendimento a solicitações de titulares (LGPD) | Atualmente utilizando os canais institucionais gerais do Instituto até definição de e-mail dedicado | `PENDENTE_DEFINICAO` |
| **Dados Empresariais (CNPJ/Razão Social)**| Rodapé institucional e notas fiscais | Oculto no rodapé até fornecimento oficial | `PENDENTE_DEFINICAO` |
| **Configuração de Envio SMTP (E-mail)** | Disparo de mensagens recebidas pelo formulário | Modo console (`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`) durante o desenvolvimento | `PENDENTE_DEFINICAO` |
| **Google Search Console Verification** | Verificação de propriedade e monitoramento de busca | Código de verificação meta tag a ser configurado em `GOOGLE_SITE_VERIFICATION` | `PENDENTE_DEFINICAO` |
| **Bing Webmaster Tools Verification** | Verificação de propriedade no buscador Bing | Código de verificação meta tag a ser configurado em `BING_SITE_VERIFICATION` | `PENDENTE_DEFINICAO` |

---

## 3. CHECKLIST PARA VALIDAÇÃO COM O CLIENTE

Quando o cliente for questionado sobre o fornecimento destes ativos, este checklist servirá como roteiro direto de solicitação:

- [ ] **1. Identidade Visual:**
  - [ ] Arquivo vetorial do logo (formato SVG ou Illustrator / EPS) com versões clara e escura.
  - [ ] Manual de marca ou especificações de fontes corporativas (caso possua).
- [ ] **2. Fotografias em Alta Resolução (conforme [GUIA_DE_IMAGENS_E_PERFORMANCE.md](GUIA_DE_IMAGENS_E_PERFORMANCE.md)):**
  - [ ] Retrato da psicóloga Mari Menezes em ambiente de consultório (enquadramento vertical `~4:5`, 960 × 1200 px).
  - [ ] Retratos complementares ou fotos de atendimento/leitura para a página Sobre Mim.
  - [ ] Fotos do espaço físico de acolhimento (caso haja atendimento presencial, proporção `~4:3`, 720 × 540 px).
- [ ] **3. Dados Oficiais de Contato:**
  - [ ] Número de telefone / WhatsApp corporativo com DDD.
  - [ ] E-mail institucional desejado (ex.: contato@institutomenteemfoco.com.br).
  - [ ] Perfil oficial do Instagram (`@...`).
- [ ] **4. Informações Profissionais Formais:**
  - [ ] Número do registro no CRP (Conselho Regional de Psicologia) com indicação da região (ex: CRP 00/00000).
  - [ ] Resumo das formações e títulos acadêmicos reais que deseja destacar.
  - [ ] Endereço comercial completo ou indicação de atuação 100% online.
- [ ] **5. Infraestrutura, Hospedagem e Deploy:**
  - [ ] Definição do domínio final registrado (ex: `institutomenteemfoco.com.br`).
  - [ ] Definição do provedor de hospedagem de produção (ex: Render, Railway, AWS, DigitalOcean).
  - [ ] Homologação da terminação TLS/SSL no reverse proxy para validação de `DJANGO_SECURE_PROXY_SSL_HEADER`.
  - [ ] Validação da reescrita de cabeçalho `X-Forwarded-For` no proxy reverso para ativação segura de `TRUST_PROXY_CLIENT_IP`.
  - [ ] Definição da arquitetura de cache em produção (avaliação de backend compartilhado Redis/Memcached caso haja múltiplos workers Gunicorn).
  - [ ] Provisionamento da instância PostgreSQL de produção (`DATABASE_URL`).
  - [ ] Geração da chave segura exclusiva de produção (`DJANGO_SECRET_KEY`).
  - [ ] Credenciais para envio de e-mails transacionais (serviço SMTP como Resend, SendGrid ou servidor próprio).
  - [ ] Códigos de verificação do Google Search Console e Bing Webmaster Tools.
  - [ ] Autorização final para ativar `SEO_ALLOW_INDEXING=True` após validação completa em produção.
  - [ ] Aprovação do cronograma de rollout do HSTS (300s -> 86400s -> 31536000s) e decisão sobre HSTS Preload.
  - [ ] Ativação de proteção de borda (Cloudflare WAF) para mitigação de ataques volumétricos (DDoS).
  - [ ] Avaliação futura de autenticação em dois fatores (MFA) para superusuários do painel administrativo.

---
*Este registro garante a rastreabilidade das pendências do cliente sem comprometer a cadência de desenvolvimento do código.*

---
**Revisado em:** Prompt 23 (29/09/2026) — Verificado independentemente. Sem alterações necessárias. As fotografias da Mari Menezes (Hero e Sobre Mim) estão formalizadas em `MAPA_DE_PRODUCAO_DE_IMAGENS.md` como IMG-001 e IMG-002, com regra explícita: **NUNCA substituir por imagem gerada por IA**. Os IDs de imagem foram atualizados — os IDs originais (IMG-001 Hero, IMG-010 Sobre) foram redefinidos no novo MAPA como IMG-001 e IMG-002 com a mesma função.


