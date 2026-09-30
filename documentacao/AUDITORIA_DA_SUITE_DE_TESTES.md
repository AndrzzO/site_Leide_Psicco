# AUDITORIA DA SUÍTE DE TESTES AUTOMATIZADOS — INSTITUTO MENTE EM FOCO
**DOCUMENTO TÉCNICO DE COBERTURA, RESILIÊNCIA E CONTRATOS DO SISTEMA**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0+ | **DATA:** 26/09/2026

---

## 1. RESUMO EXECUTIVO DA AUDITORIA

A suíte de testes automatizados do projeto **Instituto Mente em Foco** foi concebida sob o princípio inegociável de **validação de contratos e comportamento real**, rejeitando formalmente o conceito de *coverage vanity* (testes triviais concebidos unicamente para inflar percentuais de cobertura sem valor de engenharia).

Todos os testes utilizam exclusivamente a infraestrutura nativa do Django (`django.test.TestCase`, `django.test.Client`, `RequestFactory`), isolamento estrito de banco de dados (`SQLite in-memory`), zero dependência de rede externa, zero envio de e-mails reais e dados rigorosamente sintéticos.

### Métricas Gerais Consolidadas:
- **Total de Testes Automatizados:** 232 testes
- **Taxa de Aprovação:** 100% OK (0 falhas, 0 erros, 0 testes silenciados)
- **Tempo de Execução:** ~44 segundos (incluindo testes de janela temporal e rate limiting)
- **Módulos de Teste Auditados:** 12 arquivos distribuídos pelos 5 apps da arquitetura
- **Dependências Externas:** 0 (testes rodam inteiramente offline e em sandbox)
- **Resíduos em Mídia / Disco:** 0 arquivos residuais (diretório `media/` permanece íntegro com `.gitkeep`)

---

## 2. AUDITORIA CAMADA POR CAMADA

### 2.1 Camada de Modelos (Models & ORM Contracts)
- **Módulos:** `nucleo/tests.py`, `servicos/tests.py`, `conteudos/tests.py`, `contato/tests.py`
- **Contratos Auditados:**
  - `ConfiguracaoSite`: Padrão Singleton garantido (apenas 1 registro com PK=1; rejeição de duplicatas no método `clean()`; resiliência do método auxiliar `get_solo()`).
  - `Profissional`: Geração determinística de slug seguro em lowercase, validação de campos ativos e destaque.
  - `RedeSocial`: Ordenação ascendente por campo `ordem`, ativação condicional e integridade do método `__str__`.
  - `AreaAtuacao` e `Servico`: Relacionamento 1:N com integridade referencial, geração automática de slugs únicos, ordenação determinística e flags de exibição na Home.
  - `CategoriaArtigo` e `Artigo`:
    - Geração de slug único anti-colisão (sufixo incremental `-1`, `-2` para categorias homônimas).
    - Status editorial estrito: `Artigo.STATUS_RASCUNHO` como padrão inicial.
    - Preenchimento automático de `data_publicacao` no momento da publicação (quando vazio).
    - Cálculo dinâmico de `tempo_leitura_minutos` com base na média de 200 palavras por minuto.
    - QuerySet customizado `Artigo.objects.publicados()`: aplica filtro triplo rigoroso (`status='publicado'`, `data_publicacao <= agora`, `categoria__ativo=True`).
  - `MensagemContato`: Ordenação descendente por mais recentes (`-criado_em`), status padrão de não-lida (`lida=False`) e representação textual formatada.

### 2.2 Camada de Formulários (Forms & Input Validation)
- **Módulo:** `contato/tests.py`
- **Contratos Auditados:**
  - `ContatoForm`:
    - Flexibilidade de retorno: aceita e-mail isolado OU telefone/WhatsApp isolado (atende visitantes que preferem mensagens de texto).
    - Rejeição estrita se nenhum canal de contato for informado (validação cruzada limpa com mensagens de erro correspondentes).
    - Validação de formato de e-mail contra strings sem domínio ou caracteres inválidos.
    - Limite máximo de comprimento da mensagem (rejeição de payloads superiores a 2.000 caracteres contra sobrecarga de memória).
    - Obrigatoriedade inegociável do checkbox de consentimento de privacidade (`aceite_privacidade`), em conformidade direta com a LGPD.
    - Seleção de serviço de interesse: rejeita chaves primárias de serviços marcados com `ativo=False`.
    - Honeypot defensivo: campo `campo_verificacao` mascarado e rejeitado se preenchido por robôs.

### 2.3 Camada de Visões e Roteamento (Views & URLs)
- **Módulos:** `paginas/tests.py`, `servicos/tests.py`, `conteudos/tests.py`, `contato/tests.py`, `nucleo/tests.py`, `nucleo/tests_regressao.py`
- **Contratos Auditados:**
  - Resposta HTTP 200 direta e canônica em todas as 16 rotas públicas institucionais (Home, Sobre Mim, 5 páginas do Eixo Psicologia, 5 páginas do Eixo Técnico/Neuro, Blog, Contato, Políticas de Privacidade e Cookies).
  - Padrão **Post/Redirect/Get (PRG)** no formulário de contato: submissão com sucesso redireciona para `contato:index` (HTTP 302) com toast de confirmação via Django Messages Framework, impedindo reenvio acidental por recarregamento da página (F5).
  - Rota de desenvolvimento `/design-system/`: responde HTTP 200 sob `DEBUG=True` e retorna estritamente HTTP 404 sob `DEBUG=False` (prevenção contra vazamento de laboratório em produção).
  - Tratamento resiliente de banco vazio: se não houver registros de configuração ou serviços, as views operam com fallbacks seguros em vez de retornar erro 500.

### 2.4 Camada do Painel Administrativo (Django Admin)
- **Módulos:** `nucleo/tests.py`, `servicos/tests.py`, `conteudos/tests.py`, `contato/tests.py`, `nucleo/tests_regressao.py`
- **Contratos Auditados:**
  - Acesso restrito a usuários com privilégios de staff: redirecionamento seguro para a tela de login.
  - Princípio do Menor Privilégio: membros da equipe sem permissões específicas em `ConfiguracaoSite` são bloqueados com `PermissionDenied` (HTTP 403).
  - Customização de cabeçalhos (`site_header`, `site_title`, `index_title`) mantendo o branding oficial do Instituto.
  - Acesso operacional validado às páginas de listagem (`changelist`) e edição de modelos institucionais.

### 2.5 Camada de Segurança e Hardening
- **Módulos:** `nucleo/tests_seguranca.py`, `nucleo/tests_rate_limit.py`
- **Contratos Auditados:**
  - **Host Header Validation:** Rejeição de cabeçalhos Host não listados em `ALLOWED_HOSTS` com HTTP 400 (mitigação de cache poisoning e password reset hijack).
  - **Proteção CSRF:** Verificação ativa em POSTs de contato (rejeição com 403 sem token; aprovação com token legítimo).
  - **Sanitização de Markdown:** Limpeza profunda de tags perigosas (`<script>`, `<iframe>`, `onerror`, `javascript:`) mantendo estrutura semântica limpa.
  - **Escape de JSON-LD:** Neutralização de injeções de quebra de script (`</script>`) em blocos Schema.org.
  - **Upload de Arquivos:** Bloqueio de arquivos executáveis disfarçados de imagem (.jpg falso com cabeçalho MZ), extensões não permitidas (.svg, .exe, .php, .pdf) e imagens acima de 10 MB.
  - **Cabeçalhos Defensivos:** Emissão de `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cross-Origin-Opener-Policy: same-origin`, `Permissions-Policy` e CSP.
  - **Fail-Closed em Produção:** `producao.py` rejeita inicialização se `DJANGO_SECRET_KEY` for insegura ou `DJANGO_ALLOWED_HOSTS` contiver wildcard `*`.

### 2.6 Camada de Proteção contra Abuso e Rate Limiting
- **Módulo:** `nucleo/tests_rate_limit.py`
- **Contratos Auditados:**
  - Requisições GET normais e navegação legítima em Home, Artigos, Serviços, CSS e Imagens **NUNCA** são submetidas a rate limiting global.
  - Rate limit no Contato: cota de 5 submissões POST por 15 minutos por origem HMAC. Requisições excedentes retornam HTTP 429 com `Retry-After: 900`, `Cache-Control: no-store` e não disparam gravação no banco nem envio de e-mails.
  - Rate limit no Admin Login: defesa em duas camadas contra força bruta (10 falhas por IP; 5 falhas por IP + username) com limpeza após login bem-sucedido e mensagens anti-enumeração idênticas.
  - Resolução segura de IP: adoção prioritária de `REMOTE_ADDR` e rejeição de headers `X-Forwarded-For` falsificados quando não há proxy reverso confiável configurado.
  - Resiliência fail-open: falha ou indisponibilidade no backend de cache emite aviso no log e não derruba o fluxo de atendimento.

### 2.7 Camada de Acessibilidade Digital (WCAG 2.2 AA)
- **Módulo:** `nucleo/tests_acessibilidade.py`
- **Contratos Auditados:**
  - Declaração explícita de `lang="pt-BR"` na tag `<html>` de todas as páginas.
  - Skip link funcional apontando para `<main id="conteudo-principal" tabindex="-1">`.
  - Ausência de roles ARIA redundantes em elementos nativos HTML5 (`<header>`, `<main>`, `<footer>`, `<table>`).
  - Múltiplos blocos `<nav>` devidamente diferenciados por `aria-label` descritivos e exclusivos.
  - Formulário acessível: rótulos `<label for>` vinculados a todos os controles, legenda de campos obrigatórios, sumário de erros com `role="alert"` e atributos `aria-invalid` e `aria-describedby`.
  - Honeypot invisível para tecnologias assistivas (`aria-hidden="true"`, `tabindex="-1"`).
  - Imagens com atributo `alt` obrigatório em todo o template.

### 2.8 Camada de Performance Estrutural
- **Módulo:** `nucleo/tests_performance.py`
- **Contratos Auditados:**
  - Limite estrito de queries SQL: Home <= 6 queries, Sobre Mim <= 5 queries, Conteúdos <= 6 queries, Contato <= 4 queries.
  - Carregamento de scripts não-bloqueante: todos os scripts de cabeçalho possuem atributo `defer`.
  - Fontes externas do Google com duplo `preconnect` e diretiva `display=swap`.
  - Hero com estratégia LCP: `loading="eager"` e `fetchpriority="high"`.

### 2.9 Camada de Prevenção de Regressão Global
- **Módulo:** `nucleo/tests_regressao.py`
- **Contratos Auditados:**
  - **Link Crawler Completo:** Varre todas as 16 rotas públicas, descobre e requisita todos os links internos, garantindo 0 links quebrados (zero 404/500).
  - **Escalabilidade O(1) de Queries SQL:** Valida que o aumento de 1 para 10 artigos publicados não incrementa o número de queries SQL na Home ou na listagem de conteúdos (imunidade comprovada contra N+1).
  - **Resiliência UTF-8:** Garante gravação e exibição correta de acentuação em português brasileiro, caracteres especiais e emojis no Contato e na Busca do blog.
  - **Página de Erro 500 sem Vazamentos:** Renderiza template acolhedor com status 500 sem vazar dados confidenciais ou tracebacks.
  - **Precisão de Retenção LGPD:** Teste de fronteira temporal no comando `limpar_contatos_expirados` (mensagens de 29 dias e 23h mantidas; mensagens de 30 dias e 1h expurgadas; `--dry-run` não altera banco).
  - **Isolamento de Mídia:** Diretório `media/` permanece limpo sem resíduos gerados durante a execução dos testes.

---

## 3. CONCLUSÃO DA AUDITORIA

A suíte consolidada de **232 testes** atende integralmente a todos os requisitos do projeto e dos órgãos reguladores (CFP, WCAG e LGPD). O sistema encontra-se plenamente protegido contra regressões estruturais, funcionais e de segurança.
