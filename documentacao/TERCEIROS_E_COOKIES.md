# TERCEIROS, COOKIES E ARMAZENAMENTO — INSTITUTO MENTE EM FOCO
**DOCUMENTO TÉCNICO DE AUDITORIA DE RECURSOS EXTERNOS E MECANISMOS DE ARMAZENAMENTO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO | **ESTADO:** AUDITADO / REAL

---

## 1. DIRETRIZ E PRINCÍPIO ARQUITETURAL

> [!IMPORTANT]
> **REGRA DE OURO DA AUDITORIA:**
> Este documento registra estritamente as dependências de terceiros, tecnologias de armazenamento e cookies **realmente existentes e verificados** no código-fonte.
> Tecnologias ausentes (como Google Analytics, Meta Pixel, Hotjar, Google Tag Manager ou CAPTCHAs invasivos) **NÃO são listadas como existentes** e **NÃO justificam a criação de banners falsos de consentimento**.

---

## 2. INVENTÁRIO AUDITADO DE TERCEIROS

| Terceiro | Recurso / Biblioteca | Páginas Afetadas | Dados / Requisições Envolvidas | Cookie / Storage Local | Carrega Automaticamente? | Requer Decisão de Consentimento? | Status Atual |
|---|---|---|---|---|---|---|---|
| **Google LLC (Google Fonts)** | Tipografias *Cormorant Garamond* e *Montserrat* | Todas (`base.html`) | Requisição GET aos servidores `fonts.googleapis.com` e `fonts.gstatic.com`. O Google recebe IP do visitante e User-Agent para entrega das fontes. | Nenhum cookie de rastreamento enviado pelo Google Fonts. | **SIM** (via tags `<link>` no `<head>`). | **NÃO** (recurso tipográfico essencial de apresentação; documentado para futuro self-hosting). | Ativo e Otimizado com `preconnect` e `display=swap`. |
| **Meta Platforms / WhatsApp LLC** | Link direto de conversa | Home, Contato, Serviços, Blog, Rodapé e Botão Flutuante | Nenhum dado é enviado automaticamente ao WhatsApp. Somente no momento em que o visitante **clica no link**, seu navegador abre a URL oficial `https://api.whatsapp.com/send?...`. | Nenhum cookie ou storage no site do Instituto. | **NÃO** (requer ação humana voluntária de clique). | **NÃO** (link externo direto iniciado pelo titular). | Ativo via link parametrizado (`WHATSAPP_LINK`). |
| **Meta Platforms / Instagram** | Link para perfil institucional | Rodapé e Canais de Contato | Nenhum dado transmitido antes do clique. Link externo simples sem embed de post ou script de rastreamento. | Nenhum no site do Instituto. | **NÃO** (requer clique voluntário). | **NÃO** (link externo simples). | Ativo via link direto. |
| **Google LLC (Google Maps)** | Link de localização do consultório | Rodapé e Página de Contato | Nenhum dado transmitido antes do clique. **Não há `<iframe>` ou script incorporado**. Link externo simples para o aplicativo Maps. | Nenhum no site do Instituto. | **NÃO** (requer clique voluntário). | **NÃO** (link externo simples). | Ativo condicionalmente via link. |
| **Provedor de E-mail (SMTP)** | Notificação interna de novos contatos | Submissão do formulário `/contato/` | Nome, e-mail, telefone, serviço de interesse e data da mensagem enviados por SMTP interno à profissional. | Nenhum no navegador do usuário. | **SIM** (após submissão bem-sucedida pelo usuário). | **NÃO** (comunicação transacional de atendimento a pedido do titular). | Local via console em dev; aguardando credenciais em prod. |
| **Provedor de Hospedagem / BD** | Servidor web e banco de dados | Todas | Tráfego HTTP/HTTPS e persistência dos dados da aplicação. | Nenhum de terceiros. | **SIM** (infraestrutura técnica mandatória). | **NÃO** (meio indispensável para disponibilização do serviço). | SQLite em dev; PostgreSQL previsto em prod. |

---

## 3. TECNOLOGIAS EXTERNAS AUDITADAS COMO AUSENTES

A auditoria em todo o código-fonte, templates e arquivos estáticos confirmou a **INEXISTÊNCIA TOTAL** dos seguintes recursos:
* ❌ **Google Analytics (Universal Analytics / GA4):** Inexistente.
* ❌ **Google Tag Manager (GTM):** Inexistente.
* ❌ **Meta Pixel (Facebook Pixel):** Inexistente.
* ❌ **Hotjar / Microsoft Clarity / FullStory:** Inexistente.
* ❌ **reCAPTCHA / hCaptcha / Cloudflare Turnstile:** Inexistente (utiliza honeypot de primeira parte e rate limit local via cache).
* ❌ **CDNs Externas de JavaScript ou CSS:** Inexistente (todos os scripts e estilos são servidos localmente via `static/`).
* ❌ **Vídeos Incorporados (YouTube / Vimeo via `<iframe>`):** Inexistente.
* ❌ **Widgets de Redes Sociais com Scripts Inline:** Inexistente (apenas ícones SVG vetoriais estáticos de primeira parte).

---

## 4. INVENTÁRIO TÉCNICO DE COOKIES REAIS

| Nome do Cookie | Provedor | Finalidade Técnica | Categoria | Duração / Expiração | Necessário para o Funcionamento? |
|---|---|---|---|---|---|
| **`csrftoken`** | Primeira parte (Django / Instituto Mente em Foco) | Garante a integridade e segurança de formulários HTTP POST, prevenindo ataques de falsificação de requisição entre sites (Cross-Site Request Forgery). | **Estritamente Necessário (Segurança)** | 1 ano (31.449.600 segundos, renovado por requisição com formulário). | **SIM** (indispensável à segurança da aplicação). |
| **`sessionid`** | Primeira parte (Django / Instituto Mente em Foco) | Identifica a sessão autenticada exclusiva de operadores que realizam login no Django Admin (`/admin/`). Não é emitido para visitantes anônimos que apenas leem o site. | **Estritamente Necessário (Autenticação/Operação)** | 2 semanas (1.209.600 segundos) ou até o encerramento do navegador / logout. | **SIM** (indispensável ao controle de acesso administrativo). |
| **`messages`** | Primeira parte (Django / Instituto Mente em Foco) | Armazena temporariamente notificações de feedback de interface (como a mensagem de confirmação de envio do formulário de contato pós-redirecionamento PRG). | **Estritamente Necessário (Funcionalidade/Feedback)** | Efêmero (expira ao fechar a aba do navegador ou imediatamente após ser renderizado e lido). | **SIM** (indispensável à experiência de navegação sem reenvio de dados). |

---

## 5. AUDITORIA DE ARMAZENAMENTO NO NAVEGADOR (WEB STORAGE)

* **`localStorage`:** **ZERO utilização**. Nenhuma chave é gravada pelo código-fonte no armazenamento local persistente do navegador.
* **`sessionStorage`:** **ZERO utilização**. Nenhuma chave é gravada durante a navegação.
* **`IndexedDB` / `WebSQL`:** **ZERO utilização**.
* **`Service Workers` / Cache API:** **ZERO utilização**.

---

## 6. DECISÃO TÉCNICA SOBRE CONSENTIMENTO DE COOKIES

> [!IMPORTANT]
> **CONCLUSÃO DA AUDITORIA:**
> **BANNER NÃO NECESSÁRIO NO ESTADO ATUAL.**

### Justificativa Técnica e Ética:
1. O site do Instituto Mente em Foco utiliza **exclusivamente cookies técnicos e estritamente necessários** (`csrftoken`, `sessionid` para administradores, `messages` para feedback imediato).
2. **Não existem cookies analíticos, comportamentais, publicitários ou de terceiros.**
3. Conforme as diretrizes da ANPD (Autoridade Nacional de Proteção de Dados) e do Guia de Cookies de autoridades internacionais de proteção de dados, **cookies estritamente necessários não exigem consentimento prévio do usuário**, pois são indispensáveis para prestar o serviço expressamente solicitado pelo titular e para garantir a segurança da infraestrutura.
4. Apresentar um banner com botões como "Aceitar Todos" ou "Recusar" quando não existem tecnologias optativas configuraria um **Dark Pattern (Falsa Escolha)**, induzindo o usuário a acreditar que cookies essenciais poderiam ser desativados ou que cookies de rastreamento estariam operando no site.
5. Em substituição à falsa escolha, o site fornece **total transparência ativa** através da página pública dedicada `/cookies/`, discriminando de forma clara cada tecnologia técnica empregada.

---

## 7. PROTOCOLO E CHECKLIST PARA ADIÇÃO FUTURA DE TERCEIROS

Caso a instituição decida, futuramente, incorporar novos serviços externos ou ferramentas de medição, a equipe técnica **DEVERÁ** seguir rigorosamente o seguinte fluxo de governança:

- [ ] **1. Identificar a Finalidade Específica:** O recurso é indispensável para a clínica ou pode ser suprido por solução de primeira parte que preserve a privacidade?
- [ ] **2. Mapear Dados Transmitidos:** Identificar exatamente quais dados (IP, metadados, identificadores de dispositivo) serão enviados ao terceiro.
- [ ] **3. Avaliar Localização e Transferência Internacional:** Verificar se os dados trafegarão para servidores fora do Brasil e se há salvaguardas contratuais adequadas.
- [ ] **4. Avaliar Impacto em Cookies e Storage:** O serviço instala cookies persistentes, beacons ou acessa o `localStorage`?
- [ ] **5. Implementar Mecanismo Prévio de Consentimento (Consent Manager):** Se o serviço for **não essencial** (ex: Google Analytics, Meta Pixel), ele **NÃO PODERÁ** ser disparado antes de autorização explícita do visitante.
- [ ] **6. Atualizar Documentação Interna:** Atualizar este arquivo (`TERCEIROS_E_COOKIES.md`) e o `MAPA_DE_DADOS.md`.
- [ ] **7. Atualizar Políticas Públicas:** Atualizar a `/privacidade/` e `/cookies/` com a descrição do fornecedor e seu período de retenção.
- [ ] **8. Submeter à Revisão Jurídica:** Homologar o contrato e a adequação legal do fornecedor.

---
*Documento auditado e alinhado com os princípios de Privacy by Design e Transparência da LGPD.*
