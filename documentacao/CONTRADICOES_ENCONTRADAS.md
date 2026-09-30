# Contradições Encontradas — Verificação Independente
## Instituto Mente em Foco — Auditoria Prompt 23

> [!CAUTION]
> Este documento registra contradições reais identificadas durante verificação independente do código-fonte vs. documentação. Para cada contradição, a fonte de verdade foi determinada com base no código real verificado.

---

## Metodologia

Para cada contradição:
- **FONTE A:** O que a documentação afirma
- **FONTE B:** O que o código real faz
- **CÓDIGO REAL:** Trecho verificado
- **DECISÃO:** Qual é a fonte correta
- **AÇÃO:** O que deve ser feito

---

## C-001 — Formato de resposta dos Health Checks

**ÁREA:** Endpoints de Observabilidade  
**SEVERIDADE:** Baixa (comportamento correto, documentação incorreta)

**FONTE A (Documentação):**
> Múltiplos documentos (AUDITORIA_PRONTIDAO_PRODUCAO.md, CHECKLIST_DE_QUALIDADE.md, CHECKLIST_DE_SEGURANCA_PRODUCAO.md, relatório do Prompt 22) afirmam que:
> - `/health/` retorna HTTP 200 com `{"status": "ok"}`
> - `/health/ready/` retorna HTTP 200 com `{"status": "ready", "database": "connected"}` ou HTTP 503 com `{"status": "unavailable", "database": "unavailable"}`

**FONTE B (Código Real — nucleo/views.py linhas 35-61):**
```python
def health_check(request):
    response = HttpResponse("OK", content_type="text/plain", status=200)
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response

def health_ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        response = HttpResponse("OK", content_type="text/plain", status=200)
    except Exception:
        logger.exception("Falha na verificação de prontidão do banco de dados (health/ready).")
        response = HttpResponse("UNAVAILABLE", content_type="text/plain", status=503)
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
```

**CÓDIGO REAL:** `text/plain`, não JSON.

**DECISÃO:** O código real é a fonte de verdade. O comportamento de `text/plain` é funcionalmente correto e seguro para health checks. A documentação foi escrita com formato JSON planejado mas o código foi implementado com `text/plain`.

**AÇÃO:** 
1. ✅ Documentação atualizada neste prompt para refletir `text/plain`.
2. Astra 01 pode avaliar se converter para JSON seria benéfico para integração com load balancers modernos (mudança não crítica).

---

## C-002 — Número de testes nos documentos vs. execução real

**ÁREA:** Suíte de Testes  
**SEVERIDADE:** Informativa

**FONTE A (Documentação):**
> README.md e outros documentos mencionavam "232 testes" após o Prompt 22.

**FONTE B (Execução Real — Prompt 23):**
```
Ran 234 tests in 38.277s
OK
```

**CÓDIGO REAL:** 234 testes (2 testes adicionais foram descobertos ao reexecutar).

**DECISÃO:** O número correto é 234. A discrepância se deve a testes adicionados no final do Prompt 22 que não foram contabilizados imediatamente.

**AÇÃO:** ✅ Todos os documentos atualizados para 234 testes durante a execução do Prompt 23.

---

## C-003 — Rate Limiting em Produção Multi-Worker

**ÁREA:** Segurança / Rate Limit  
**SEVERIDADE:** Alta (risco operacional em produção multi-worker)

**FONTE A (Documentação):**
> Documentos afirmam que o rate limiting protege contra abuso com "limite de 5 envios/15 min".

**FONTE B (Código Real — configuracoes/settings/base.py linhas 147-152):**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'mente-em-foco-cache-local',
    }
}
```

**CÓDIGO REAL:** LocMemCache — cada processo Gunicorn mantém seus próprios contadores em memória. Em produção com N workers, um atacante pode realizar N×limite requests antes de ser bloqueado.

**DECISÃO:** O código está correto para desenvolvimento mono-instância. A documentação cita a limitação (MATRIZ_VARIAVEIS_AMBIENTE.md menciona Redis como alternativa). A contradição é que documentos de segurança não deixam claro que o limite efetivo em multi-worker é `N × 5` requests.

**AÇÃO:**
- Documentação atualizada no CONTEXTO_PARA_GPT_ASTRA_6.md com aviso explícito.
- Astra 02 deve avaliar se isto é um release blocker para produção multi-worker.
- Solução: substituir LocMemCache por Redis compartilhado no CACHES em produção.

---

## C-004 — WCAG 2.1 vs WCAG 2.2

**ÁREA:** Acessibilidade  
**SEVERIDADE:** Informativa

**FONTE A (README.md):**
> "focada em alta sofisticação editorial, segurança, clareza, acessibilidade (WCAG 2.1 AA)"

**FONTE B (AUDITORIA_DE_ACESSIBILIDADE.md e CHECKLIST_DE_QUALIDADE.md):**
> Documentos mais recentes mencionam WCAG 2.2 AA, incluindo critério 2.4.11 (scroll-margin-top para foco não obscurecido).

**CÓDIGO REAL:** A implementação segue critérios do WCAG 2.2 AA (como o critério 2.4.11 que é exclusivo do 2.2). O README está desatualizado.

**DECISÃO:** WCAG 2.2 AA é a versão implementada (mais recente e mais rigorosa).

**AÇÃO:** ✅ Contradição documentada. Atualizar README.md para WCAG 2.2 AA em revisão futura do Astra 03.

---

## C-005 — Arquivos de Script na pasta scratch/

**ÁREA:** Código Morto / Temporário  
**SEVERIDADE:** Baixa

**FONTE A (Nenhuma documentação menciona):**
> Ausência de documentação sobre scripts temporários.

**FONTE B (Código Real — listagem do diretório):**
```
scratch/check_case.py
scratch/check_http.py
scratch/audit_deep.py
scratch/audit_functional.py
```

**CÓDIGO REAL:** 4 scripts de auditoria existem na pasta `scratch/` mas não são documentados nem referenciados em nenhum documento de governança.

**DECISÃO:** Estes são scripts temporários de auditoria criados durante os Prompts 18-22. Devem ser mantidos como referência histórica mas não são código de produção.

**AÇÃO:** Classificados como TEMPORÁRIOS / HISTÓRICOS. O Astra 01 pode avaliar se devem ser mantidos, movidos para documentação ou descartados.

---

## C-006 — Template inicio_temporario.html

**ÁREA:** Templates  
**SEVERIDADE:** Baixa

**FONTE A (Nenhuma documentação menciona):**
> Ausência de documentação sobre template temporário.

**FONTE B (Código Real):**
```
templates/paginas/inicio_temporario.html
```

**CÓDIGO REAL:** Existe um template `inicio_temporario.html` na pasta de templates que parece ser um template legado do início do projeto.

**DECISÃO:** Provavelmente é um template legado (placeholder inicial). Precisa verificar se está sendo referenciado em alguma view ativa.

**AÇÃO:** Astra 01 deve verificar se `inicio_temporario.html` é referenciado por alguma URL/view ativa. Se não, pode ser arquivado ou removido.

---

## C-007 — laboratorio_design_system.html disponível publicamente

**ÁREA:** SEO / Segurança  
**SEVERIDADE:** Baixa

**FONTE A (Documentação):**
> Menção a "laboratório de design system" sem detalhar acessibilidade da rota.

**FONTE B (Código Real — middleware.py linhas 57-59):**
```python
if path.startswith('/health/') or path.startswith('/design-system/'):
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response
```

**CÓDIGO REAL:** A rota `/design-system/` está no SEOMiddleware para receber `noindex, nofollow`, sugerindo que existe como rota pública mas não indexável. O template `laboratorio_design_system.html` existe.

**DECISÃO:** A rota provavelmente existe mas não está indexada. Deve ser protegida ou removida em produção para evitar exposição de informações sobre a arquitetura visual.

**AÇÃO:** Astra 02 deve verificar se a rota `/design-system/` está ativa, se há necessidade de autenticação e se deve ser removida em produção.

---

## RESUMO EXECUTIVO

| ID | Área | Severidade | Status |
| :--- | :--- | :--- | :--- |
| C-001 | Health Check format (text/plain vs JSON) | Baixa | Documentação corrigida |
| C-002 | Contagem de testes (232 vs 234) | Informativa | Documentação corrigida |
| C-003 | Rate limit LocMemCache em multi-worker | Alta | Documentado para Astra 02 |
| C-004 | WCAG 2.1 vs WCAG 2.2 no README | Informativa | Documentado para Astra 03 |
| C-005 | Scripts em scratch/ não documentados | Baixa | Documentado para Astra 01 |
| C-006 | Template inicio_temporario.html | Baixa | Documentado para Astra 01 |
| C-007 | Rota /design-system/ pública | Baixa | Documentado para Astra 02 |

### Contradições Corrigidas Neste Prompt:
- C-001: Documentação atualizada para `text/plain`
- C-002: Número de testes corrigido para 234 em todos os documentos

### Contradições Para Astra:
- C-003: Rate limit multi-worker → **Astra 02** (Segurança)
- C-004: WCAG version → **Astra 03** (UI/UX)
- C-005: Scripts scratch → **Astra 01** (Código)
- C-006: Template legado → **Astra 01** (Código)
- C-007: Design system público → **Astra 02** (Segurança)
