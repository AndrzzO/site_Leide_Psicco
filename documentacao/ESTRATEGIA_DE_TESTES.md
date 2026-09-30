# ESTRATÉGIA DE TESTES AUTOMATIZADOS — INSTITUTO MENTE EM FOCO
**DIRETRIZES DE ARQUITETURA DE TESTES, FILOSOFIA DE ENGENHARIA E CONTRATOS**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0+

---

## 1. FILOSOFIA E PRINCÍPIOS FUNDAMENTAIS

A estratégia de testes do **Instituto Mente em Foco** é orientada a **comportamento e contratos reais**, e não à busca cega por métricas superficiais de cobertura (*coverage vanity*).

### Regras Cardeais da Suíte:
1. **Teste Contratos, Não Detalhes Internos:** O foco recai sobre o que o sistema entrega (status HTTP, cabeçalhos de segurança, integridade de dados no banco, proteção contra abusos e conformidade WCAG/LGPD), e não sobre implementações temporárias ou nomes de variáveis internas.
2. **Zero Dependência de Rede Externa:** Nenhum teste realiza chamadas a APIs externas, requisições HTTP para a internet ou conexões a servidores SMTP reais. Toda e qualquer integração é simulada em sandbox ou resolvida localmente.
3. **Zero Dados Pessoais Reais (LGPD & CFP):** Todos os dados utilizados nos testes (nomes, e-mails, telefones, números de registro profissional) são **100% sintéticos e fictícios** (ex: `paciente@exemplo.com.br`, `(61) 98888-7777`, `mariana@exemplo.com.br`).
4. **Isolamento Estrito de Estado:** Cada classe e método de teste é executado em transações atômicas isoladas ou com bancos de dados SQLite voláteis em memória, garantindo que nenhum teste contamine o estado de outro.
5. **Zero Resíduos em Disco:** Testes que envolvem arquivos de upload (Pillow) manipulam dados binários estritamente em memória (`io.BytesIO` e `SimpleUploadedFile`), garantindo que o diretório `media/` físico permaneça limpo (apenas com `.gitkeep`).

---

## 2. A PIRÂMIDE DE TESTES DO PROJETO

```
          / \
         /   \
        / Reg \       Testes de Regressão Global & Link Crawler
       /------- \     (nucleo/tests_regressao.py)
      / Integra- \    Testes de Integração de Fluxos, Views, PRG,
     /    ção     \   SEO, Acessibilidade WCAG e Rate Limiting
    /--------------\
   /   Unitários    \  Testes de Modelos, Validadores, Formatações,
  /   (Fundação)     \ Sanitização e Slugs Únicos
 /--------------------\
```

### 2.1 Camada da Base: Testes Unitários de Modelos e Validadores
- **Foco:** Validação de regras de negócio puras, integridade de campos, cálculo dinâmico de tempo de leitura, filtros de QuerySet (`publicados()`), validação de dimensões e formato de imagens com Pillow, e sanitização de Markdown com Bleach.
- **Velocidade:** Execução instantânea (milissegundos por teste).

### 2.2 Camada Intermediária: Testes de Integração e Contratos HTTP
- **Foco:** Ciclo completo de requisição e resposta do Django Test Client.
  - Submissão de formulário e padrão PRG (302 com mensagens flash).
  - Bloqueio de submissões sem CSRF (403).
  - Proteção contra Host Header Poisoning (400).
  - Cabeçalhos de segurança (CSP, nosniff, DENY, Permissions-Policy).
  - Isolamento de rascunhos e conteúdos agendados no futuro (404).
  - Rate limiting contextual com retorno 429 e `Retry-After`.
  - Conformidade de acessibilidade estrutural (HTML5 semântico, skip link, landmarks, labels e alertas).

### 2.3 Camada de Cúpula: Testes de Regressão Global e Prevenção de N+1
- **Foco:** Garantir que novas alterações no código não quebrem funcionalidades já homologadas.
  - Link crawler que audita todas as páginas e links internos renderizados.
  - Testes de escalabilidade de consultas SQL garantindo que o aumento de registros mantenha complexidade $O(1)$.
  - Verificação de encoding UTF-8 com acentos brasileiros e emojis.
  - Simulação de rotinas de retenção temporal de dados da LGPD.

---

## 3. POLÍTICAS DE MOCK E ISOLAMENTO

| Recurso do Sistema | Abordagem de Teste | Implementação |
| :--- | :--- | :--- |
| **Banco de Dados** | SQLite volátil gerenciado pelo Django Test Runner | `file:memorydb_default` isolado; transações revertidas entre testes (`setUpTestData` e transações) |
| **Envio de E-mails** | Backend nativo de e-mail em memória (`locmem`) | `django.core.mail.outbox` auditado sem disparar sockets de rede |
| **Cache & Rate Limit**| Cache local em memória (`LocMemCache`) | `cache.clear()` em `setUp`/`tearDown` de cada teste para evitar interferência |
| **Arquivos de Mídia** | Imagens sintéticas geradas via Pillow em `io.BytesIO` | `SimpleUploadedFile` em memória sem gravação no disco rígido |
| **Hora do Sistema** | `django.utils.timezone.now` e manipulação de deltas | Simulação determinística de agendamentos e expurgo de retenção |
| **Settings de Produção** | `override_settings` e `unittest.mock.patch` | Teste de fail-closed sem alterar arquivos de configuração reais |

---

## 4. DIRETRIZES PARA ADIÇÃO DE NOVOS TESTES

Ao implementar novas funcionalidades ou corrigir eventuais bugs no futuro, siga este roteiro:

1. **Bug Report -> Teste Primeiro (TDD de Regressão):**
   - Ao identificar uma falha ou oportunidade de melhoria, escreva primeiro um teste que reproduza a falha.
   - Aplique o ajuste no código até que o teste seja aprovado.
2. **Evite Asserções Frágeis:**
   - Não teste cores hexadecimais exatas ou pixels no CSS que possam mudar em ajustes de design.
   - Teste a presença de classes semânticas, atributos ARIA e tags de estrutura.
3. **Mantenha os Nomes Descritivos:**
   - O nome do teste deve explicar claramente o que está sendo testado e qual o resultado esperado. Exemplo: `test_anonimo_acessando_admin_redirecionado_para_login`.
4. **Verificação Pré-Commit Obrigatória:**
   - Antes de qualquer commit, execute o comando completo:
     ```bash
     python manage.py test
     python manage.py check
     python manage.py makemigrations --check
     ```
