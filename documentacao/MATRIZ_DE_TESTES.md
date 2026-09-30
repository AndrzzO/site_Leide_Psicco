# MATRIZ DE TESTES AUTOMATIZADOS — INSTITUTO MENTE EM FOCO
**MAPEAMENTO EXAUSTIVO DE CAMADAS, ROTAS, CENÁRIOS E GARANTIAS DE CONTRATO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **TOTAL DE TESTES:** 232 | **STATUS:** 100% OK

---

## 1. TABELA CONSOLIDADA POR MÓDULOS DE TESTE

| Módulo de Teste | Qtd | Escopo Principal | Tipos de Teste | Status |
| :--- | :---: | :--- | :--- | :---: |
| `contato/tests.py` | 30 | Modelo de mensagens, ContatoForm, visualização, CSRF, honeypot, PRG, comando de expurgo LGPD | Unitário, Integração, Segurança | Aprovado |
| `conteudos/tests.py` | 28 | Modelos de Artigo/Categoria, sanitize anti-XSS, QuerySet publicados, rascunhos 404, busca, detalhe, admin | Unitário, Integração, Editorial | Aprovado |
| `paginas/tests.py` | 28 | Home definitiva, H1 único, Design System debug/prod, Header/Footer, WhatsApp dinâmico, Sobre Mim | Integração, Funcional, UI | Aprovado |
| `servicos/tests.py` | 30 | Eixo Psicologia, Eixo Técnico, Hub de Avaliação, 6 etapas, resiliência a dados vazios, menu ativo | Integração, Funcional, Ético | Aprovado |
| `nucleo/tests.py` | 12 | Health check /health/, handler 404 customizado, Singleton ConfiguracaoSite, validadores de upload | Unitário, Infraestrutura | Aprovado |
| `nucleo/tests_acessibilidade.py` | 13 | WCAG 2.2 AA: lang pt-BR, skip link, ausência de roles redundantes, aria-labels em navs, formulário acessível | Acessibilidade Estrutural | Aprovado |
| `nucleo/tests_performance.py` | 10 | Limite de queries SQL, scripts com defer, preconnect em fontes, estratégia LCP eager | Performance, Web Vitals | Aprovado |
| `nucleo/tests_rate_limit.py` | 21 | Rate limiting em Contato e Admin, anti-spoofing de IP, pseudonimização HMAC, fail-open, HTTP 429 | Segurança, Abuso, DoS | Aprovado |
| `nucleo/tests_seguranca.py` | 18 | Host header poisoning, CSRF, XSS em Markdown e JSON-LD, uploads executáveis, headers defensivos | Segurança e Hardening | Aprovado |
| `nucleo/tests_seo.py` | 17 | Robots.txt dinâmico, Sitemap.xml, Open Graph, Twitter Cards, System Checks seo.E001/E002 | SEO Técnico, Governança | Aprovado |
| `nucleo/tests_seo_editorial.py` | 12 | H1 canônico único nas 16 rotas, hierarquia de headings, padronização de titles, meta descriptions | SEO Editorial e On-Page | Aprovado |
| `nucleo/tests_regressao.py` | 13 | Link crawler global (zero 404/500), escalabilidade O(1) sem N+1, resiliência UTF-8/LGPD, erro 500 sem vazamento | Regressão Global, Contratos | Aprovado |
| **TOTAL GERAL** | **232** | **Cobertura integral de todas as camadas e fluxos do projeto** | **Completo** | **100% OK** |

---

## 2. MATRIZ DETALHADA POR CAMADA E CENÁRIO

### 2.1 Camada de Modelos e Banco de Dados (ORM)
| Módulo | Modelo | Cenário Auditado | Comportamento Esperado |
| :--- | :--- | :--- | :--- |
| `nucleo` | `ConfiguracaoSite` | Criação do primeiro registro e tentativa de criar segundo | Singleton preservado (PK=1); `clean()` levanta `ValidationError` em duplicata |
| `nucleo` | `ConfiguracaoSite` | Consulta via `get_solo()` | Retorna o registro ativo sem falhas |
| `nucleo` | `Profissional` | Criação com nome "Mari Menezes" | Gera slug `mari-menezes` automaticamente |
| `nucleo` | `RedeSocial` | Cadastro com ordem 1 e 2 | Ordenação determinística ascendente |
| `servicos` | `AreaAtuacao` | Criação com nome "Psicologia" | Slug `psicologia`, ativo=True, mostrar_na_home=True |
| `servicos` | `Servico` | Vinculação com `AreaAtuacao` | Relacionamento 1:N preservado e cascade consistente |
| `conteudos` | `CategoriaArtigo` | Criação de categorias homônimas | Geração de slugs anti-colisão (`categoria` e `categoria-1`) |
| `conteudos` | `Artigo` | Criação sem status | Define `status=STATUS_RASCUNHO` por padrão |
| `conteudos` | `Artigo` | Publicação imediata | Preenche `data_publicacao` automaticamente |
| `conteudos` | `Artigo` | Artigo com 450 palavras | Calcula `tempo_leitura_minutos = 3` |
| `conteudos` | `Artigo` | Consulta via `Artigo.objects.publicados()` | Filtra rascunhos, agendamentos futuros e categorias inativas |
| `contato` | `MensagemContato` | Criação de mensagens sucessivas | Ordenação descendente `-criado_em` e `lida=False` |

---

### 2.2 Camada de Formulários e Validação de Dados
| Módulo | Formulário | Cenário Auditado | Comportamento Esperado |
| :--- | :--- | :--- | :--- |
| `contato` | `ContatoForm` | Preenchimento apenas com e-mail válido | Válido (`form.is_valid() == True`) |
| `contato` | `ContatoForm` | Preenchimento apenas com telefone válido | Válido (`form.is_valid() == True`) |
| `contato` | `ContatoForm` | Omissão de e-mail e telefone simultaneamente | Inválido; erros em `email` e `telefone` |
| `contato` | `ContatoForm` | Omissão do campo `nome` ou nome < 2 caracteres | Inválido; erro em `nome` |
| `contato` | `ContatoForm` | Checkbox `aceite_privacidade` desmarcado | Inválido; erro obrigatório LGPD |
| `contato` | `ContatoForm` | Mensagem acima de 2.000 caracteres | Inválido; rejeição por excesso de tamanho |
| `contato` | `ContatoForm` | Seleção de serviço inativo (`ativo=False`) | Inválido; erro no campo `servico_interesse` |
| `contato` | `ContatoForm` | Campo honeypot `campo_verificacao` preenchido | Identificação silenciosa de bot e descarte |

---

### 2.3 Camada de Roteamento, Visões e HTTP
| Rota | Método | Cenário Auditado | Status Esperado |
| :--- | :---: | :--- | :---: |
| `/` | GET | Carregamento da Home institucional | 200 OK |
| `/sobre-mim/` | GET | Carregamento da página biográfica e clínica | 200 OK |
| `/servicos/psicologia/` | GET | Página de escuta clínica e temas acolhidos | 200 OK |
| `/servicos/neuropsicologia/` | GET | Página técnica de funcionamento cognitivo | 200 OK |
| `/servicos/traumas/` | GET | Página de acolhimento em experiências difíceis | 200 OK |
| `/servicos/separacao-e-recomecos/` | GET | Página de reorganização de rotina e identidade | 200 OK |
| `/servicos/novos-relacionamentos/` | GET | Página de reflexão sobre vínculos e limites | 200 OK |
| `/servicos/avaliacao/` | GET | Hub de diferenciação diagnóstica | 200 OK |
| `/servicos/avaliacao-psicologica/` | GET | Página de fluxo de 6 etapas | 200 OK |
| `/servicos/avaliacao-neuropsicologica/` | GET | Página técnica com procedimentos e devolutiva | 200 OK |
| `/servicos/reabilitacao-neurocognitiva/` | GET | Página de estratégias individualizadas | 200 OK |
| `/conteudos/` | GET | Listagem de artigos educativos paginada | 200 OK |
| `/conteudos/<slug>/` | GET | Detalhe de artigo publicado | 200 OK |
| `/conteudos/<slug-rascunho>/` | GET | Tentativa de acesso a artigo em rascunho | 404 Not Found |
| `/conteudos/<slug-futuro>/` | GET | Tentativa de acesso a artigo com data futura | 404 Not Found |
| `/contato/` | GET | Formulário de contato acessível | 200 OK |
| `/contato/` | POST | Envio legítimo com dados e token CSRF | 302 Found (PRG) |
| `/contato/` | POST | Submissão sem token CSRF | 403 Forbidden |
| `/design-system/` | GET | Acesso sob `DEBUG=True` | 200 OK |
| `/design-system/` | GET | Acesso sob `DEBUG=False` | 404 Not Found |
| `/health/` | GET | Verificação de integridade operacional | 200 OK ("OK") |
| `/robots.txt` | GET | Arquivo de governança de indexação | 200 OK (text/plain) |
| `/sitemap.xml` | GET | Mapa de URLs canônicas | 200 OK (application/xml) |
| `/politica-de-privacidade/` | GET | 14 seções factuais de privacidade LGPD | 200 OK |
| `/politica-de-cookies/` | GET | Tabela técnica de cookies estritamente necessários | 200 OK |

---

### 2.4 Camada de Segurança, Proteção contra Abuso e Rate Limiting
| Vetor Auditado | Módulo de Teste | Condição de Teste | Resultado Garantido |
| :--- | :--- | :--- | :--- |
| **Host Header Poisoning** | `tests_seguranca` | Host arbitrário `atacante-malicioso.com` | Rejeição imediata com HTTP 400 |
| **Cross-Site Scripting (XSS)** | `tests_seguranca` | Markdown com `<script>` e `onerror` | Sanitização total sem execução |
| **JSON-LD Script Breakout** | `tests_seguranca` | Injeção de `</script>` em strings Schema.org | Codificação segura `\u003c\u002Fscript\u003e` |
| **Upload de Executáveis** | `tests_seguranca` | Arquivo `.jpg` com cabeçalho de executável MZ | Rejeição por `validar_imagem` (ValidationError) |
| **Extensões Perigosas** | `tests_seguranca` | Arquivos `.svg`, `.exe`, `.php`, `.pdf` | Rejeição imediata |
| **Tamanho Excessivo de Imagem** | `tests_seguranca` | Imagem simulada com 11 MB | Rejeição por ultrapassar 10 MB |
| **Headers Defensivos** | `tests_seguranca` | Inspeção de cabeçalhos HTTP na resposta | DENY, nosniff, strict-origin, COOP, Permissions-Policy |
| **Rate Limit Contato (GET)** | `tests_rate_limit` | 10 requisições GET sucessivas à rota `/contato/` | Nenhuma consome cota de limite (todas 200 OK) |
| **Rate Limit Contato (POST)** | `tests_rate_limit` | 6 submissões POST dentro de 15 minutos | 5 aceitas; 6ª retorna HTTP 429 com `Retry-After: 900` |
| **Admin Brute Force (IP)** | `tests_rate_limit` | 10 falhas de autenticação no login administrativo | Bloqueio do IP por 15 minutos com HTTP 429 |
| **Admin Combo (IP + User)** | `tests_rate_limit` | 5 falhas no mesmo par (IP + username) | Bloqueio combo sem afetar outros usuários |
| **Anti-Enumeração Admin** | `tests_rate_limit` | Tentativa com username inexistente vs existente | Mensagem de erro e tempo de resposta idênticos |
| **IP Spoofing via Proxy** | `tests_rate_limit` | Envio de cabeçalho forjado `X-Forwarded-For` | Ignorado sumariamente; adota `REMOTE_ADDR` |
| **Pseudonimização HMAC** | `tests_rate_limit` | Inspeção de chaves de cache e logs de rate limit | Zero IPs brutos ou usernames armazenados |

---

### 2.5 Camada de Acessibilidade Digital (WCAG 2.2 AA)
| Critério WCAG | Requisito Técnico | Cenário Auditado | Resultado |
| :--- | :--- | :--- | :---: |
| **3.1.1 Idioma da Página** | Tag `<html>` com declaração de idioma | Verificação nas 16 páginas | `lang="pt-BR"` em 100% |
| **2.4.1 Ignorar Blocos** | Link de salto para conteúdo principal | Skip link presente no topo do DOM | Aponta para `#conteudo-principal` com `tabindex="-1"` |
| **1.3.1 Info e Relações** | Semântica nativa sem roles redundantes | Tags `<header>`, `<main>`, `<footer>` | Zero roles redundantes |
| **4.1.2 Nome, Função e Valor** | Diferenciação de múltiplos blocos `<nav>` | Menu principal e menu de rodapé | `aria-label` exclusivos e descritivos |
| **1.3.1 Rótulos em Formulários**| Associação de `<label>` e controles | Todos os campos de `/contato/` | `<label for="id_campo">` presente |
| **3.3.1 / 3.3.3 Erros** | Anúncio de erros para leitores de tela | Submissão com campos vazios | Sumário com `role="alert"` e `aria-invalid="true"` |
| **4.1.2 Blindagem Honeypot** | Ocultação de armadilhas para bots | Campo de verificação no DOM | `aria-hidden="true"` e `tabindex="-1"` |
| **1.1.1 Mídias Não-Textuais** | Texto alternativo em imagens | Todas as tags `<img>` das páginas | Atributo `alt` presente em 100% |

---

### 2.6 Camada de Performance Estrutural
| Parâmetro | Meta / Limite | Cenário Auditado | Resultado |
| :--- | :---: | :--- | :---: |
| **Queries Home** | <= 6 queries | Acesso à rota `/` | 6 queries executadas |
| **Queries Sobre Mim** | <= 5 queries | Acesso à rota `/sobre-mim/` | 5 queries executadas |
| **Queries Conteúdos** | <= 6 queries | Acesso à rota `/conteudos/` | 6 queries executadas |
| **Queries Contato** | <= 4 queries | Acesso à rota `/contato/` | 4 queries executadas |
| **Scripts não-bloqueantes** | 100% com defer | Inclusão de scripts em `base.html` | Atributo `defer` em todos os `<script>` |
| **Otimização de Fontes** | Preconnect duplo | Carregamento de fontes Google | Preconnect para `fonts.googleapis.com` e `fonts.gstatic.com` |
| **Prioridade LCP** | Carregamento prioritário | Imagem principal do Hero | `loading="eager"` e `fetchpriority="high"` |

---

### 2.7 Camada de Regressão Global
| Teste de Regressão | Finalidade | Comportamento Verificado | Status |
| :--- | :--- | :--- | :---: |
| **Link Crawler Global** | Varrer todas as páginas e links internos | Zero links internos quebrados (zero 404, zero 500) | Aprovado |
| **Escalabilidade O(1)** | Verificar queries com 1 vs 10 artigos | Quantidade de queries idêntica (sem regressão N+1) | Aprovado |
| **Resiliência UTF-8** | Submissão e busca com acentos e emojis | Gravação íntegra e exibição sem corrupção de caracteres | Aprovado |
| **Página de Erro 500** | Simulação de falha interna do servidor | Exibição de `erros/500.html` sem vazamento de traceback | Aprovado |
| **Fronteira LGPD 30 dias**| Expurgo temporal no comando administrativo | 29d 23h mantido; 30d 1h expurgado; dry-run simulado | Aprovado |
| **Isolamento de Mídia** | Garantir limpeza do diretório `media/` | Diretório limpo sem acúmulo de resíduos de teste | Aprovado |
