# GUIA DE GESTÃO DO DJANGO ADMIN — INSTITUTO MENTE EM FOCO
**MANUAL OPERACIONAL PARA ADMINISTRAÇÃO DO SITE INSTITUCIONAL**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **FRAMEWORK:** DJANGO

---

## 1. COMO ACESSAR O PAINEL ADMINISTRATIVO

1. Certifique-se de que o servidor local esteja em execução:
   ```bash
   python manage.py runserver
   ```
2. Abra seu navegador e acesse a URL configurada:
   ```
   http://localhost:8000/admin/
   ```
3. Informe o nome de usuário e a senha do seu usuário administrador (criado localmente através de `python manage.py createsuperuser`).

> [!NOTE]
> Por questões de segurança, nenhuma credencial de acesso ou senha é versionada ou gravada no código-fonte.

---

## 2. CONFIGURAÇÕES INSTITUCIONAIS (CONFIGURAÇÃO DO SITE)

O modelo **Configuração do Site** adota o padrão *Singleton* (apenas 1 registro existe no sistema para evitar conflitos).

* **Como editar:** No menu lateral do Admin, clique em **Núcleo Institucional e Configurações** $\rightarrow$ **Configuração do Site** e selecione o registro existente ("Instituto Mente em Foco").
* **Seções disponíveis:**
  * **Identidade Institucional:** Nome do Instituto, Conceito/Slogan tríplice (*COMPREENDER • CUIDAR • RECONSTRUIR*), Frase Institucional, Frase Emocional e CTA Principal.
  * **Canais de Contato:** Telefone fixo, número do WhatsApp comercial (apenas números com DDD, ex: `5561999999999`), mensagem padrão de acolhimento e e-mail institucional.
  * **Localização e Atendimento:** Modalidade de atendimento (*Presencial, Online ou Híbrido*), endereço completo, cidade, UF, horário de atendimento e link do Google Maps.
  * **Identidade Visual e Imagens:** Logotipo principal, versões horizontal/vertical, Favicon e imagem padrão para redes sociais (Open Graph).

> [!IMPORTANT]
> **Proteção Ativa:** O registro de configuração do site não pode ser excluído acidentalmente e o botão de criar um segundo registro é bloqueado nativamente.

---

## 3. GESTÃO DA PROFISSIONAL (MARI MENEZES)

* **Onde gerenciar:** No Admin, acesse **Núcleo Institucional e Configurações** $\rightarrow$ **Profissionais**.
* **Como editar:**
  * **Nome e Apresentação:** Nome completo, nome de exibição para a Home (*Psicóloga Mari Menezes*), título profissional (*Psicóloga, palestrante e facilitadora de grupos*) e áreas de atuação.
  * **Biografia:** Biografia curta (utilizada nos cards e na Home) e biografia completa (utilizada na página Sobre Mim).
  * **Fotografias Editoriais:** Envio das fotos em alta resolução para o Hero, Seção Sobre e fotos complementares.
  * **Registro Profissional (CRP):** Informar o número oficial de inscrição no CRP com a respectiva região.
* **Regra Ética Inegociável:** **NUNCA INVENTAR** formações acadêmicas, títulos, cursos de pós-graduação ou certificados que não tenham sido oficialmente fornecidos e comprovados pela profissional.

---

## 4. ÁREAS DE ATUAÇÃO E SERVIÇOS

A estrutura foi modelada para permitir controle total de exibição sem necessidade de alterar o código do site.

### 4.1 Áreas de Atuação
Representam os grandes pilares do Instituto (Psicologia, Neuropsicologia, Traumas, Separação e Recomeços, Novos Relacionamentos):
* **Campos principais:** Título, Resumo, Descrição, Frase de Destaque e Imagem do Card.
* **Ordem de Exibição:** O campo **Ordem** (número inteiro positivo: 1, 2, 3...) define a ordem dos cards na página inicial e menus.
* **Controles de Visibilidade:**
  * `Ativo`: desmarque para desativar temporariamente a área sem apagá-la.
  * `Mostrar na Página Inicial`: marque para exibir o card correspondente na Home.

### 4.2 Serviços e Avaliações
Representam os atendimentos específicos (Psicologia Clínica, Avaliação Psicológica, Avaliação Neuropsicológica, Reabilitação Neurocognitiva, etc.):
* **Associação:** Cada serviço pode ser associado opcionalmente a uma **Área de Atuação**.
* **SEO e Buscadores:** Você pode personalizar os campos **Meta Title** (até 60-70 caracteres) e **Meta Description** (entre 140 e 160 caracteres) para cada serviço individualmente.

---

## 5. REDES SOCIAIS

* **Onde gerenciar:** Acesse **Redes Sociais**.
* **Campos:** Nome da rede, URL completa do perfil (ex.: `https://instagram.com/...`), seletor de ícone (*Instagram, LinkedIn, YouTube, Facebook, WhatsApp*) e ordem de exibição.
* **Segurança:** O sistema não permite a inserção de tags HTML arbitrárias ou scripts nos campos de rede social.

---

## 6. GESTÃO DE CONTEÚDOS EDUCATIVOS E BLOG

O app **Conteúdos** permite o gerenciamento editorial completo e seguro de artigos informativos e reflexões clínicas.

### 6.1 Categorias de Artigos
* **Onde gerenciar:** Acesse **Conteúdos e Artigos** $\rightarrow$ **Categorias de Artigos**.
* **Campos:** Nome da categoria, slug amigável (gerado automaticamente), descrição editorial, ordem de exibição e status ativo.
* **Filtros e Contagem:** A listagem exibe automaticamente o número de artigos publicados e rascunhos vinculados a cada categoria.

### 6.2 Gestão e Publicação de Artigos
* **Onde gerenciar:** Acesse **Conteúdos e Artigos** $\rightarrow$ **Artigos**.
* **Ciclo de Vida Editorial:**
  * `Rascunho` (*Padrão*): Artigos em rascunho **nunca são exibidos publicamente**. Tentativas de acesso direto pela URL retornam HTTP 404.
  * `Publicado`: O artigo fica visível no site imediatamente, desde que a **Data de Publicação** seja menor ou igual ao momento atual. Se a data estiver vazia no momento da publicação, o sistema a preenche automaticamente.
  * `Agendado` (Data Futura): Se você definir uma data de publicação no futuro, o artigo permanecerá privado até o exato instante configurado.
* **Formatação em Markdown Seguro:**
  * Escreva o texto do artigo utilizando a formatação padrão Markdown.
  * Utilize `##` para subtítulos de seção (H2) e `###` para subtópicos (H3).
  * **Atenção:** Não utilize `#` (H1) no corpo do texto, pois o H1 é gerado exclusivamente a partir do título do artigo para proteção da hierarquia semântica e SEO.
  * **Segurança Anti-XSS:** Todas as publicações passam por um processo automático de sanitização estrita via biblioteca `bleach`. Tags `<script>`, manipuladores inline de eventos (`onload`, `onerror`) e links `javascript:` são sumariamente removidos.
* **Imagem de Capa e Acessibilidade:**
  * Proporção recomendada: `~16:9` (ex: 1200x675px).
  * Preencha sempre o **Texto Alternativo da Capa (alt)** descrevendo a imagem com clareza para leitores de tela e acessibilidade de deficientes visuais.
* **Conexão Clínica (Serviço Relacionado):**
  * Você pode selecionar um serviço do Instituto (ex: *Psicologia Clínica*, *Avaliação Neuropsicológica*, *Separação e Recomeços*) para que o artigo exiba automaticamente um box de encaminhamento ético e acolhedor ao final da leitura.
* **Destaque na Listagem:**
  * Marcar o campo `Destaque Principal na Listagem` posiciona o artigo com destaque visual e diagramação horizontal no topo da página `/conteudos/`.

---

## 7. DIRETRIZES PARA UPLOAD DE IMAGENS E FOTOGRAFIAS

Para garantir que o site carregue com velocidade excepcional e mantenha a elegância do design aprovado, siga estas recomendações:

| Elemento Visual | Proporção Recomendada | Formatos Permitidos | Limite de Tamanho | Observações |
|---|---|---|---|---|
| **Foto Hero Mari Menezes** | `~4:5` (Vertical, ex: 800x1000px) | JPG, PNG, WEBP | Máx. 10 MB | Iluminação suave, olhar acolhedor, fundo neutro/desfocado. |
| **Foto Seção Sobre Mim** | `~4:5` (Vertical, ex: 800x1000px) | JPG, PNG, WEBP | Máx. 10 MB | Retrato de escuta ou postura profissional humanizada. |
| **Cards de Áreas de Atuação** | `~4:3` (Horizontal, ex: 600x450px) | JPG, PNG, WEBP | Máx. 10 MB | Imagens conceituais serenas, harmonia com a paleta de cores. |
| **Capas de Serviços** | `~16:9` (Panorâmica, ex: 1200x675px)| JPG, PNG, WEBP | Máx. 10 MB | Imagem de topo para as páginas internas de serviços. |
| **Logotipos** | Vetorial ou PNG com fundo transparente | PNG, WEBP | Máx. 10 MB | Alta nitidez para telas Retina / alta densidade. |
| **Favicon** | `1:1` (Quadrado: 32x32, 192x192px) | ICO, PNG | Máx. 10 MB | Símbolo minimalista legível em abas pequenas de navegadores. |

### Regras de Segurança Automáticas
* O sistema valida internamente o cabeçalho real do arquivo através da biblioteca Pillow. Arquivos com extensões forçadas (ex: um `.exe` renomeado para `.jpg`) são **automaticamente rejeitados**.
* Arquivos que ultrapassarem o limite configurado (10 MB) serão bloqueados com mensagem explicativa no painel.

---

## 8. GESTÃO DE MENSAGENS DE CONTATO

O módulo **Comunicação e Atendimento** gerencia as mensagens institucionais recebidas por meio do formulário do site.

* **Onde gerenciar:** No Admin, acesse **Comunicação e Atendimento** $\rightarrow$ **Mensagens de Contato**.
* **Objetivo e Triagem:**
  * Visualização organizada das mensagens com identificação do remetente (Nome, E-mail, Telefone/WhatsApp), serviço de interesse e data/hora do envio.
  * O indicador de status visual (**Lida** ou **Nova**) pode ser alternado diretamente na listagem ou na tela de visualização.
  * O corpo da mensagem é preservado como texto puro no banco de dados e protegido contra injeção de scripts (XSS).
* **Campos Somente-Leitura:**
  * Os dados submetidos pelo usuário (Nome, E-mail, Telefone, Serviço, Mensagem, Aceite da Política e Data de Envio) tornam-se de leitura exclusiva (`readonly`) após a gravação, garantindo a integridade e rastreabilidade da comunicação original.

> [!IMPORTANT]
> **ALERTA ÉTICO E LEGAL (CFP & LGPD):**
> Este módulo destina-se **exclusivamente ao acolhimento inicial e triagem de atendimento**.
> * **ESTE NÃO É UM PRONTUÁRIO ELETRÔNICO.**
> * **ESTE NÃO É UM CRM CLÍNICO.**
> * **NUNCA registre diagnósticos, sintomas clínicos, hipóteses diagnósticas, medicamentos, evoluções de sessões ou notas terapêuticas confidenciais no painel administrativo.**
> * O prontuário psicológico deve seguir estritamente as resoluções vigentes do CFP em sistema clínico dedicado e apartado.

---

## 9. PRIVACIDADE DOS CONTATOS E BOAS PRÁTICAS OPERACIONAIS (LGPD)

As mensagens enviadas por visitantes através do formulário do site contêm **dados pessoais** protegidos pela LGPD (Lei nº 13.709/2018). Todos os operadores do painel administrativo devem seguir rigorosamente estas diretrizes operacionais:

* **Restrição de Acesso:** O acesso à listagem e leitura de mensagens é concedido exclusivamente a membros da equipe formalmente autorizados pela responsável técnica Mari Menezes.
* **Proibição de Exportações Informais:** Não copie dados de contato (nomes, e-mails, telefones) para planilhas avulsas, arquivos de texto locais, dispositivos pessoais ou grupos de mensagens sem necessidade estrita de serviço.
* **Não Utilização como Prontuário:** Lembre-se de que este módulo existe unicamente para responder a dúvidas e triar solicitações. O histórico clínico, sessões e evoluções terapêuticas devem ser registrados exclusivamente no prontuário profissional sob sigilo do CFP.
* **Eliminação e Expurgos:** Mensagens antigas que não resultaram em atendimento podem ser excluídas manualmente no painel ou por meio do comando administrativo seguro de expurgo (`python manage.py limpar_contatos_expirados`), respeitando a política institucional de retenção.

---

## 10. ORIENTAÇÕES DE SEO EDITORIAL E BUSCADORES

Tanto nos **Serviços** quanto nos **Artigos do Blog**, o painel administrativo disponibiliza campos específicos de metadados para otimização nos mecanismos de busca (Google, Bing, etc.):

* **Meta Título (SEO):**
  * Título conciso e informativo para exibição na aba do navegador e no resultado de busca.
  * Extensão ideal: até **60 a 70 caracteres**.
  * Se deixado em branco em um artigo, o sistema utiliza automaticamente o título principal do texto.
* **Meta Descrição (SEO):**
  * Resumo atrativo e factual apresentado no snippet do buscador abaixo do título.
  * Extensão ideal: entre **140 e 160 caracteres**.
  * Se deixado em branco em um artigo, o sistema utiliza automaticamente o resumo do artigo.
* **Sitemap.xml Automático:**
  * O mapa do site (`/sitemap.xml`) é gerado dinamicamente em tempo real.
  * Artigos salvos como **Rascunho** ou com data de publicação futura são **automaticamente excluídos** do sitemap e de mecanismos de busca até que sua publicação esteja formalmente no ar.
* **Semântica e Acessibilidade:**
  * Sempre preencha o **Texto Alternativo da Imagem (alt)** nas capas de artigos e serviços, descrevendo com objetividade o conteúdo da fotografia.

---

## 11. CHECKLIST EDITORIAL PRÉ-PUBLICAÇÃO (PROMPT 13)

Antes de alterar o status de um artigo para **Publicado** ou cadastrar uma nova página no sistema, execute obrigatoriamente este checklist de qualidade e conformidade ética:

### 1. Hierarquia Semântica (Headings)
- [ ] O título principal do artigo será o único `<h1>` da página gerado automaticamente pelo template.
- [ ] No corpo do texto (editor rich text / HTML formatado), utilize exclusivamente `<h2>` para os títulos de seção e `<h3>` para subdivisões. **NUNCA** insira tags `<h1>` no corpo do texto.
- [ ] Não pule níveis estruturais (não use `<h4>` sem um `<h3>` precedente).

### 2. Metadados de Busca (SEO On-Page)
- [ ] **Meta Título:** Preenchido com até 65 caracteres, contendo o tema principal com clareza.
- [ ] **Meta Descrição:** Preenchida com 120 a 160 caracteres, resumindo o valor do artigo sem jargões indecifráveis e sem promessas sensacionalistas.
- [ ] **Slug da URL:** Curto, legível, em minúsculas e separado por hifens (gerado automaticamente a partir do título).

### 3. Interlinking e Conexão Clínica
- [ ] **Serviço Relacionado:** Selecione obrigatoriamente a qual área clínica o artigo se conecta (ex: conectar um artigo sobre luto ao serviço *Traumas e Experiências Difíceis* ou *Psicologia Clínica*).
- [ ] **Links Internos no Texto:** Sempre que citar conceitos clínicos abordados em outras páginas do site, crie um link contextual natural (ex: linkar para `/servicos/avaliacao-neuropsicologica/` ao mencionar testes de memória e atenção).
- [ ] **Texto-Âncora:** O texto do link deve ser explicativo e natural (ex: *"conheça nosso acompanhamento em separação"*), evitando termos vazios como *"clique aqui"* ou repetições forçadas.

### 4. Responsabilidade Ética em Saúde Mental (CFP)
- [ ] O texto **não promete cura, alívio imediato ou prazos pré-determinados** para superação de conflitos psíquicos.
- [ ] O artigo **não diagnostica o leitor** nem incentiva autodiagnóstico sem acompanhamento profissional qualificado.
- [ ] O conteúdo **não expõe casos clínicos identificáveis de pacientes** nem inclui depoimentos promocionais (*social proof*).
- [ ] A linguagem é acolhedora, respeitosa, cientificamente fundamentada e empática.

### 5. Ativos Visuais e Acessibilidade
- [ ] A imagem de capa possui proporção paisagem (16:9 ou 3:2), tamanho inferior a 10 MB e alta qualidade visual.
- [ ] O campo de **Texto Alternativo (alt)** da imagem está preenchido obrigatoriamente, descrevendo a fotografia para tecnologias assistivas (leitores de tela) de forma concisa e factual (ex: *"Mulher em reflexão junto a uma janela iluminada pela luz da manhã"*).

---

## 12. DIRETRIZES OPERACIONAIS DE ACESSIBILIDADE (WCAG 2.2 AA)

A acessibilidade é responsabilidade contínua de todos os editores e administradores que publicam conteúdos no portal. Ao redigir novos artigos, serviços ou páginas, observe impreterivelmente as seguintes regras:

1. **Textos Alternativos de Imagens (Critério 1.1.1):**
   - **Regra:** Toda imagem carregada no sistema que transmita informação clínica ou editorial deve possuir o campo `Texto Alternativo` preenchido.
   - **Como preencher:** Descreva de maneira concisa o que está na foto (sujeito, ação e ambiente). Não utilize prefixos como "Foto de..." ou "Imagem de...".
   - **Imagens decorativas:** Se a imagem for puramente ornamental e não agregar informação contextual, o campo pode ficar em branco para que o sistema a oculte adequadamente das tecnologias assistivas com `alt=""`.

2. **Hierarquia Estrutural de Títulos (Critério 1.3.1):**
   - O título da página ou artigo já é gerado como o único `<h1>`.
   - No corpo do texto, inicie suas divisões com `<h2>` (Título de Seção) e suas subdivisões com `<h3>` (Subtítulo).
   - **Nunca pule níveis:** Não insira um `<h3>` sem um `<h2>` anterior.
   - **Nunca use negrito para simular títulos:** Use sempre o formato de cabeçalho nativo do editor.

3. **Links Significativos e Claros (Critério 2.4.4):**
   - **Proibição absoluta:** Nunca utilize frases como *"clique aqui"*, *"saiba mais"*, *"leia mais"* ou *"acesse o link"*.
   - **Correto:** O texto do link deve explicar por si só o seu destino, mesmo fora de contexto (ex: *"consulte as etapas da avaliação neuropsicológica"* ou *"leia nosso artigo sobre acolhimento do luto"*).

4. **Clareza de Linguagem e Legibilidade (Critério 3.1.2):**
   - Mantenha parágrafos curtos (entre 2 e 4 frases).
   - Utilize listas com marcadores (`<ul>` ou `<ol>`) para elencar etapas, sintomas ou reflexões sequenciais.
   - Explique termos técnicos da neuropsicologia e da psicologia logo após sua menção.

---

## 13. DIRETRIZES DE PERFORMANCE E GESTÃO DE IMAGENS (PROMPT 15)

O portal foi projetado para oferecer carregamento ultrarrápido aos visitantes. Ao gerenciar fotografias no painel administrativo:

1. **Formatos Modernos:**
   - Dê preferência aos formatos **WebP** ou **JPG otimizado**.
2. **Dimensões e Proporções Recomendadas:**
   - **Retratos (4:5):** 960 × 1200 px (máx. 300 KB).
   - **Capas de Artigo e Serviços (16:9):** 1600 × 900 px (máx. 250 KB).
   - **Cards de Atuação (4:3):** 720 × 540 px (máx. 100 KB).
3. **Limite de Upload do Sistema:**
   - O sistema bloqueia automaticamente qualquer arquivo que exceda **5 MB** para preservar a estabilidade da hospedagem.
4. **Sem Perda Perceptível:**
   - Utilize nível de compressão entre 80% e 85% em ferramentas simples como [Squoosh.app](https://squoosh.app/) ou [TinyPNG](https://tinypng.com/) antes do envio.

---

## 14. DIRETRIZES DE SEGURANÇA E PROTEÇÃO DE LOGIN (PROMPT 17)

Para resguardar as contas institucionais da clínica e proteger o painel contra ataques automatizados de força bruta:

1. **Bloqueio Temporário por Falhas Consecutivas:**
   - Caso um usuário ou dispositivo erre a senha de acesso repetidamente, o sistema ativará um **bloqueio temporário de 15 minutos** para aquela origem.
   - **Não existe bloqueio permanente:** Após o intervalo de segurança, o acesso é restabelecido automaticamente sem necessidade de suporte técnico.
2. **Resguardo de Contas Legítimas:**
   - O mecanismo protege o administrador legítimo: tentativas maliciosas originadas de outros computadores ou redes não bloqueiam o acesso do gestor em seu local habitual de trabalho.
3. **Estabilidade de Senhas:**
   - As senhas permanecem criptografadas e blindadas pelos validadores do Django, exigindo no mínimo 12 caracteres com complexidade estruturada. Não compartilhe suas credenciais e mantenha suas senhas individuais em sigilo.

---

## 15. ROTEIRO PRÁTICO DE OPERAÇÃO EDITORIAL E TRIAGEM (PROMPT 21)

### 15.1 Publicação e Despublicação de Artigos
1. **Criar Rascunho com Segurança:**
   - Acesse **Conteúdos e Artigos** $\rightarrow$ **Artigos** $\rightarrow$ **Adicionar Artigo**.
   - Defina o título, selecione a categoria e escreva o texto em Markdown seguro (`##` para seções, `###` para tópicos).
   - O status inicial padrão é **Rascunho**. Salve o artigo. Ele estará 100% privado e invisível para o público externo.
2. **Publicar:**
   - Quando a revisão estiver concluída, altere o status para **Publicado**.
   - Verifique se a **Data de Publicação** está definida para hoje/agora. Salve.
   - O artigo aparecerá imediatamente na página de conteúdos (`/conteudos/`) e no `sitemap.xml`.
3. **Despublicar:**
   - Para remover um artigo do ar sem apagá-lo, basta editar o registro, alterar o status de volta para **Rascunho** e salvar. O acesso público por link direto retornará imediatamente HTTP 404.

### 15.2 Gestão e Ordenação de Serviços e Home
1. **Controlar Exibição na Home:**
   - Em **Áreas de Atuação** ou **Serviços**, utilize o checkbox **Mostrar na Página Inicial** para ligar ou desligar a visibilidade do card na Home.
2. **Reordenar Cards:**
   - Ajuste o número no campo **Ordem** (1, 2, 3...). Números menores aparecem primeiro.

### 15.3 Triagem Segura de Mensagens de Contato
1. **Visualizar Contatos:**
   - Acesse **Contato e Mensagens** $\rightarrow$ **Mensagens de Contato**.
   - Os novos contatos aparecem com badge vermelha (*Nova Mensagem*).
2. **Atendimento e Marcação:**
   - Abra a mensagem para ler as solicitações do paciente em um painel seguro formatado.
   - Para preservar a integridade jurídica e LGPD, os campos de texto do paciente não podem ser editados.
   - Após responder o visitante pelo WhatsApp ou e-mail, marque o campo **Lida** e salve. O status mudará para a badge verde (*Respondida / Lida*).

---
*Este guia operacional é parte integrante da documentação oficial do projeto Instituto Mente em Foco.*

