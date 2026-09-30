# Matriz Responsiva Universal — 16 Rotas Públicas vs 13 Faixas de Resolução

**Projeto:** Instituto Mente em Foco  
**Data da Matriz:** 26 de Setembro de 2026  
**Status Consolidado:** 100% DAS ROTAS ESTÁVEIS EM TODAS AS FAIXAS (ZERO HORIZONTAL SCROLL DESTRUTIVO)

---

## 1. Mapeamento das 16 Rotas Públicas Auditadas

| ID | Rota | Nome da Página / Função | Tipo de Conteúdo |
| :---: | :--- | :--- | :--- |
| **R01** | `/` | Home / Página Inicial | Editorial Misto, Grids, Snap Carousel, FAQ |
| **R02** | `/sobre-mim/` | Sobre a Dra. Leide Feitosa | Biografia, Formação, Pilares, Trajetória |
| **R03** | `/servicos/psicologia/` | Psicoterapia Clínica | Apresentação do serviço, indicação, benefícios |
| **R04** | `/servicos/neuropsicologia/` | Neuropsicologia Clínica | Eixo técnico, funções cognitivas, intervenção |
| **R05** | `/servicos/traumas/` | Traumas e Processamento (EMDR) | Tratamento especializado, abordagem sensível |
| **R06** | `/servicos/separacao-e-recomecos/` | Separação e Recomeços | Terapia para transições de vida e vínculos |
| **R07** | `/servicos/avaliacao/` | Hub de Avaliações | Hub estrutural, roteamento para diagnósticos |
| **R08** | `/servicos/avaliacao-psicologica/` | Avaliação Psicológica | Procedimentos, baterias de testes, laudo |
| **R09** | `/servicos/avaliacao-neuropsicologica/` | Avaliação Neuropsicológica | Investigação clínica em 6 etapas detalhadas |
| **R10** | `/servicos/reabilitacao-neurocognitiva/` | Reabilitação Neurocognitiva | Treino cognitivo, plasticidade neural |
| **R11** | `/conteudos/` | Blog / Listagem de Artigos | Barra de busca, categorias, paginação, cards |
| **R12** | `/contato/` | Contato e Agendamento | Formulário com CSRF, cartões de contato direto |
| **R13** | `/politica-de-privacidade/` | Política de Privacidade | Documento legal, tabela LGPD, leitura fluida |
| **R14** | `/politica-de-cookies/` | Política de Cookies | Gestão de consentimento e diretrizes técnicas |
| **R15** | `/robots.txt` | Diretrizes de Indexação | Texto puro estruturado para rastreadores |
| **R16** | `/sitemap.xml` | Mapa do Site para Mecanismos de Busca | XML padronizado e validado pelo W3C |

---

## 2. Matriz de Avaliação Cruzada (Rotas x Resoluções)

### Legenda dos Critérios Auditados:
- **H:** Ausência de transbordamento horizontal (`scrollWidth <= clientWidth`).
- **N:** Navegação adaptada (Menu Desktop completo ou Drawer móvel com trap focus).
- **T:** Tipografia e botões legíveis sem quebras desarmônicas ou sobreposição.
- **I:** Imagens e placeholders estruturais com aspect ratio preservado (4:5, 4:3, 1:1, 16:9).
- **Status:** **OK** (Conformidade Plena).

| Rota / Resolução | 320x568 (SE 1ª) | 360x640 (Android) | 390x844 (iPhone 14) | 430x932 (Pro Max) | 768x1024 (iPad Port) | 820x1180 (iPad Air) | 1024x768 (iPad Land) | 1024x1366 (iPad Pro) | 1280x720 (Note HD) | 1366x768 (Note Std) | 1440x900 (MacBook) | 1920x1080 (FHD) | 2560x1440 (2K/4K) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **R01 (Home)** | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R02 (Sobre)** | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R03 (Psico)** | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R04 (Neuro)** | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R05 (Trauma)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R06 (Recome)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R07 (Hub Av)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R08 (Av Psi)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R09 (Av Neu)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R10 (Reabil)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R11 (Blog)**  | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R12 (Cont)**  | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R13 (Privac)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R14 (Cookie)**| OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) | OK (H,N,T,I) |
| **R15 (Robots)**| N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   | N/A (Texto)   |
| **R16 (Sitemap)**| N/A (XML)    | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     | N/A (XML)     |

---

## 3. Síntese do Comportamento Estrutural por Faixa

1. **Faixa 320px – 480px (Smartphones Pequenos e Médios):**
   - Drawer de navegação ativo via botão hamburger (44x44px).
   - Botão CTA do cabeçalho oculto abaixo de 480px para evitar concorrência com o logotipo.
   - Botões CTA em grupo (`.cta-group`) quebram linhas harmoniosamente com largura adaptativa de 100% ou centralização suave.
   - Textos de títulos com `text-wrap: balance` e clamp calibrado, impedindo linhas orfãs com 1 palavra ou caracteres espremidos.
   - Fileira de identificação funcionando como snap-carousel horizontal fluido.
2. **Faixa 768px – 1024px (Tablets e Híbridos):**
   - Grids comutam de 1 para 2 colunas equilibradas.
   - Citação flutuante da profissional na Home posiciona-se no topo superior direito com backdrop blur e sombra suave.
   - Rodapé exibe layout em 2 colunas com tipografia nítida e espaçamento confortável.
3. **Faixa 1080px+ (Notebooks e Monitores Desktop):**
   - Transição imediata para o menu desktop horizontal completo com sublinhado suave no link ativo.
   - Desativação do botão hamburger e garantia de gaveta oculta (`hidden`).
   - Fileira de identificação expande-se em grade estática contínua de 7 colunas.
   - Containers centrais respeitam `max-width: 1280px` com margens automáticas, evitando perda de foco em telas ultrawide.
