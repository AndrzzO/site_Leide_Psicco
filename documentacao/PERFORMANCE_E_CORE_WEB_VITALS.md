# ARQUITETURA DE PERFORMANCE E CORE WEB VITALS
## INSTITUTO MENTE EM FOCO — DIRETRIZES TÉCNICAS E DE ENGENHARIA
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO 6.0+

> [!IMPORTANT]
> **RESTRIÇÃO METODOLÓGICA — FOTOGRAFIAS DEFINITIVAS AINDA NÃO FORNECIDAS:**  
> Como as fotos finais da cliente ainda não foram inseridas no projeto, as medições de peso de assets e LCP presentes neste documento refletem o estado estrutural de desenvolvimento com placeholders leves. A infraestrutura de marcação HTML e CSS já está integralmente preparada para que a inserção futura das fotos reais ocorra com estabilidade dimensional absoluta (**CLS = 0**) e prioridade de carregamento otimizada (**LCP < 2.5s**).

---

## 1. Princípios de Engenharia e Metas de Core Web Vitals

A estratégia de carregamento do Instituto Mente em Foco foi projetada para alinhar a estética sofisticada e acolhedora com os mais altos padrões de engenharia web moderna:

### Metas Técnicas Oficiais (Google Core Web Vitals):
- **LCP (Largest Contentful Paint) $\le 2.5\text{ s}$:**  
  Tempo até a renderização do maior elemento visual acima da dobra (geralmente o retrato da profissional na Home ou a capa nos artigos).
- **CLS (Cumulative Layout Shift) $\le 0.1$ (Meta interna: $0.00$):**  
  Eliminação total de deslocamentos bruscos de conteúdo durante o carregamento por meio de reserva dimensional prévia com CSS `aspect-ratio`.
- **INP (Interaction to Next Paint) $\le 200\text{ ms}$:**  
  Responsividade instantânea a cliques, toques e teclas, garantida pela ausência de frameworks JavaScript pesados e arquitetura baseada em Vanilla JS nativo.
- **TTFB (Time to First Byte) $\le 800\text{ ms}$ (Meta local: $< 50\text{ ms}$):**  
  Tempo de resposta do servidor Django minimizado com consultas otimizadas, ausência de N+1 e templates compilados eficientemente.

---

## 2. Lab Data (Laboratório) vs Field Data (Dados de Campo / RUM)

Para uma governança transparente, a equipe diferencia rigorosamente os dois tipos de medição:

1. **Lab Data (Testes de Laboratório):**
   - Coletados em ambientes controlados (máquina local, CI/CD, Lighthouse, Django Test Client).
   - Úteis para depuração rápida, controle de regressões e garantia de orçamentos de performance (*performance budgets*).
   - **Limitação:** Não refletem condições reais de redes instáveis 3G/4G, dispositivos de baixa potência ou comportamento imprevisível de usuários.
2. **Field Data (Dados de Campo / RUM):**
   - Telemetria agregada de visitantes reais coletada pelo Chrome User Experience Report (CrUX) e APIs de navegação (`PerformanceObserver`).
   - **Estado Atual:** Marcado tecnicamente como **NÃO DISPONÍVEL / AGUARDANDO DEPLOY PÚBLICO**, pois o projeto encontra-se em ambiente de homologação local antes do apontamento do domínio de produção.

---

## 3. Estratégia dos Recursos Críticos

### 3.1 CSS Modular e Ordem de Carregamento
O CSS é organizado em uma cadeia estrita e sem encadeamento de `@import`:
1. `tokens.css`: Variáveis de cor, espaçamento, tipografia e raios de borda.
2. `base.css`: Reset, acessibilidade, container central e regras de movimento reduzido.
3. `tipografia.css`: Hierarquia visual H1 a H6 e pesos padronizados.
4. `layout.css`: Sistema de grids e flexbox.
5. `componentes.css`: Botões, cards, frames com aspect-ratio, header e footer.
6. `utilitarios.css`: Helpers de espaçamento e alinhamento.
7. CSS específico por rota (`home.css`, `paginas_internas.css`, `conteudos.css`, `contato.css`).

*Orçamento Total de CSS na Home:* ~76.9 KB sem compressão (em produção com Gzip/Brotli: ~15.2 KB).

### 3.2 JavaScript Não-Bloqueante (Zero Bloqueio de Thread Principal)
- **Atributo `defer` Universal:** Todos os scripts (`base.js`, `navegacao.js`, `home.js`) são carregados com o atributo `defer`, executando de forma sequencial apenas após o parsing completo do DOM.
- **Sem Bibliotecas Terceirizadas:** Zero jQuery, React, Vue, Lodash ou plugins volumosos.
- **Volume Total de JS:** Apenas **6.3 KB** sem compressão (~2.1 KB transferidos em produção).
- **Tratamento de Scroll e Eventos:** Uso de `IntersectionObserver` com desconexão imediata dos elementos observados (`unobserve`), sem qualquer listener no evento `window.onscroll`.

### 3.3 Fontes Web Otimizadas (Google Fonts)
- **Pré-conexão Dupla:**
  - `<link rel="preconnect" href="https://fonts.googleapis.com">`
  - `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
- **Font-Display Swap:** Evita FOIT (*Flash of Invisible Text*), garantindo que os textos em fontes de sistema de fallback (Georgia e sans-serif) sejam lidos imediatamente enquanto os glifos elegantes são baixados.

---

## 4. Estratégia de Banco de Dados e Consultas Django

1. **Prevenção de N+1 Queries:**
   - Uso de `select_related('categoria', 'autor')` nas consultas públicas de artigos (`conteudos.views`).
   - Uso de `select_related('area')` na listagem de serviços destacados na Home (`paginas.views`).
2. **Consultas Otimizadas no Context Processor:**
   - `nucleo.context_processors.dados_institucionais` executa buscas diretas indexadas e encapsula os dados da marca para todos os templates.
3. **Eliminação de Consultas Duplicadas:**
   - Na view de Contato (`contato.views.index`), a busca de `ConfiguracaoSite` foi postergada para a submissão de formulário POST, eliminando 1 query no carregamento inicial da página (GET reduzido de 5 para 4 queries).

---

## 5. Recomendações de Infraestrutura para Produção

Quando o site for implantado no servidor definitivo (Nginx / Gunicorn / WhiteNoise), as seguintes configurações de cache e compressão devem ser ativadas:

1. **Compressão Estática (Gzip e Brotli):**  
   Ativar compressão para tipos MIME `text/html`, `text/css`, `application/javascript`, `image/svg+xml`.
2. **Cabeçalhos de Cache Estático Imutável:**  
   Para arquivos versionados em `/static/`:
   ```http
   Cache-Control: public, max-age=31536000, immutable
   ```
3. **Cabeçalhos para Páginas HTML Dinâmicas:**  
   Para respostas SSR geradas pelo Django:
   ```http
   Cache-Control: public, max-age=0, must-revalidate
   Vary: Accept-Encoding, Cookie
   ```
4. **Pool de Conexões de Banco de Dados:**  
   Manter `conn_max_age=600` e `conn_health_checks=True` já configurados em `configuracoes/settings/producao.py`.
