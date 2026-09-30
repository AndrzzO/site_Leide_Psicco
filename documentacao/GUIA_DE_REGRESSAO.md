# GUIA DE PREVENÇÃO DE REGRESSÃO — INSTITUTO MENTE EM FOCO
**MANUAL OPERACIONAL PARA DESENVOLVEDORES, PIPELINE DE CI/CD E HOMOLOGAÇÃO PRÉ-DEPLOY**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0+

---

## 1. OBJETIVO DO GUIA

Este guia estabelece os procedimentos padronizados que qualquer desenvolvedor, mantenedor ou pipeline de integração contínua (CI/CD) deve executar rigorosamente antes de homologar código para o ambiente de produção do **Instituto Mente em Foco**.

A suíte de testes do projeto é a **primeira linha de defesa** contra quebras funcionais, brechas de segurança, degradação de performance ou violações éticas e legais.

---

## 2. CHECKLIST DE VERIFICAÇÃO RÁPIDA (GATEWAY PRÉ-COMMIT / PRÉ-DEPLOY)

Antes de enviar qualquer código para o repositório ou autorizar um deploy, execute a sequência de quatro comandos essenciais:

```bash
# 1. Executar a suíte completa de testes automatizados (232 testes)
python manage.py test

# 2. Executar as verificações de sistema do Django (incluindo SEO e Rate Limit)
python manage.py check

# 3. Validar ausência de migrações esquecidas ou modelos não sincronizados
python manage.py makemigrations --check

# 4. Validar integridade e ausência de conflitos nas dependências pip
python -m pip check
```

### Critério de Aceite:
- **Zero Falhas (`0 failures`):** Todos os 232 testes devem passar com `OK`.
- **Zero Erros (`0 errors`):** Nenhuma exceção não capturada ou erro de ambiente.
- **Zero Issues no Check (`0 issues`):** System checks limpos.
- **No changes detected:** O banco de dados e os modelos estão perfeitamente sincronizados.
- **No broken requirements found:** Dependências em perfeita compatibilidade.

---

## 3. PROCEDIMENTOS DE DIAGNÓSTICO EM CASO DE FALHA

### 3.1 Falha em Teste de Escalabilidade SQL (Prevenção de N+1)
- **Sintoma:** Erro do tipo `Regressão N+1 detectada! Queries saltaram de X para Y` ou `6 queries != 7 queries`.
- **Diagnóstico:**
  - Verifique se na view correspondente foi omitido o uso de `select_related()` para relacionamentos de chave estrangeira (ex: autor ou categoria do artigo) ou `prefetch_related()`.
  - Inspecione se novas chamadas ao context processor foram introduzidas sem cache ou singleton.

### 3.2 Falha em Teste de Link Crawler (Código 404 Detectado)
- **Sintoma:** Mensagem `Link interno quebrado detectado: /rota/ retornou status 404`.
- **Diagnóstico:**
  - Verifique os templates editados e confirme se links foram escritos manualmente em vez de utilizar a tag nativa `{% url 'app:nome' %}`.
  - Certifique-se de que a rota correspondente está declarada em `urls.py` e possui a barra final canônica (`trailing slash`).

### 3.3 Falha em Teste de Rate Limiting (Retorno 429 Inesperado)
- **Sintoma:** Um teste aleatório falha com status 429 Too Many Requests quando esperava 200 ou 302.
- **Diagnóstico:**
  - Certifique-se de que o método `setUp()` ou `tearDown()` da classe de teste executa `cache.clear()` para isolar o estado dos limites de taxa entre as execuções.

### 3.4 Falha em Teste de Acessibilidade (Atributo alt ou Rótulo Ausente)
- **Sintoma:** Falha em `test_todas_as_imagens_possuem_alt` ou `test_formulario_contato_labels_e_legenda`.
- **Diagnóstico:**
  - Toda tag `<img>` criada deve conter o atributo `alt` (mesmo que vazio para decorativas, ou descritivo para informativas).
  - Todo campo de formulário deve conter um `<label for="...">` correspondente e legenda textual de obrigatoriedade.

---

## 4. MATRIZ DE RISCO DE REGRESSÃO POR TIPO DE ALTERAÇÃO

| Componente Alterado | Testes Mais Impactados | Ação Preventiva Recomendada |
| :--- | :--- | :--- |
| **`templates/base/base.html`** | `tests_acessibilidade`, `tests_performance`, `tests_regressao` | Rodar `manage.py test nucleo` completo; verificar skip-link, landmarks e defer nos scripts |
| **`contato/forms.py` ou `views.py`** | `contato.tests`, `tests_rate_limit`, `tests_seguranca`, `tests_regressao` | Verificar integridade do token CSRF, honeypot, validação cruzada e rate limit |
| **`conteudos/views.py`** | `conteudos.tests`, `tests_performance`, `tests_regressao` | Verificar query count de listagem, paginação, sanitização anti-XSS e isolamento de rascunhos |
| **`configuracoes/settings/*.py`** | `tests_seguranca`, `nucleo.tests`, `tests_rate_limit` | Validar comportamento fail-closed de produção, CSP, hosts autorizados e validadores de senha |
| **Menu ou Rodapé (`base.html`)** | `paginas.tests`, `tests_seo_editorial`, `tests_regressao` | Rodar `LinkCrawlerRegressionTest` para garantir ausência de links quebrados |

---

## 5. INTEGRAÇÃO COM CI/CD (EXEMPLO GITHUB ACTIONS / GITLAB CI)

Caso seja configurado pipeline de CI/CD para o projeto, a rotina padrão deve reproduzir o ambiente hermético do Django:

```yaml
name: Testes e Prevenção de Regressão

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configurar Python 3.14
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - name: Instalar Dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Executar Checagens de Integridade
        run: |
          python manage.py check
          python manage.py makemigrations --check
          python -m pip check
      - name: Executar Suíte Completa de Testes
        run: |
          python manage.py test --verbosity=2
```
