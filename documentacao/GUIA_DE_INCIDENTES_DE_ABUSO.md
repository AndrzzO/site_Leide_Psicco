# GUIA OPERACIONAL DE INCIDENTES DE ABUSO E RATE LIMIT
**INSTITUTO MENTE EM FOCO — PROCEDIMENTOS PRÁTICOS PARA GESTÃO DE TRÁFEGO SUSPEITO**
**VERSÃO:** 1.0.0 | **PROJETO:** INSTITUTO MENTE EM FOCO

---

## 1. COMO IDENTIFICAR AUMENTO DE RESPOSTAS HTTP 429

- **Sintoma:** Alerta de monitoramento ou linhas frequentes no log do servidor:
  `WARNING nucleo.rate_limit: Rate limit excedido no escopo 'contato'` ou `'admin_login_ip'`.
- **Diagnóstico:**
  - Verificar a proporção entre acessos legítimos e respostas 429.
  - Se os picos de 429 coincidirem com um único escopo (ex.: `/contato/`), o mecanismo está funcionando e contendo uma automação sem afetar a navegação geral do portal.
  - Conferir se pacientes reais estão relatando dificuldade de envio de mensagens no canal WhatsApp.

---

## 2. COMO CONFIRMAR SE É SPAM REAL OU FALSO POSITIVO

1. **Acessar o Painel Administrativo:**
   - Visualizar a listagem de mensagens recebidas em `/painel-admin/contato/mensagemcontato/`.
   - Verificar padrão dos remetentes: links suspeitos no texto, sequências de caracteres sem sentido (`asdfghjkl`), números internacionais inexistentes ou e-mails temporários descartáveis.
2. **Avaliar Falsos Positivos:**
   - Pacientes reais que clicaram múltiplas vezes no botão "Enviar" por ansiedade ou lentidão de conexão móvel. Nesses casos, o texto da mensagem é coerente e humano.

---

## 3. COMO EVITAR O "BLOQUEIO DE TUDO" (NÃO ENTRAR EM PÂNICO)

- **Princípio:** O rate limit da aplicação já isola o abuso na origem específica.
- **Regra:** NUNCA aplicar bloqueios globais no firewall ou derrubar o site por picos pontuais de spam em formulário.
- Mantenha a Home, os Artigos e os canais de WhatsApp sempre acessíveis.

---

## 4. COMO REVISAR THRESHOLDS DE RATE LIMITING

Se for constatado que os limites atuais estão muito restritivos para usuários legítimos em redes compartilhadas (ex.: clínicas parceiras, faculdades ou redes Wi-Fi públicas corporativas):
1. Abrir o arquivo de variáveis de ambiente `.env`.
2. Incrementar moderadamente os limites:
   - Exemplo Contato: `CONTACT_RATE_LIMIT_COUNT=8` e `CONTACT_RATE_LIMIT_WINDOW=600` (8 envios em 10 minutos).
   - Exemplo Admin: `ADMIN_LOGIN_IP_LIMIT=15` e `ADMIN_LOGIN_IP_WINDOW=600`.
3. Reiniciar o serviço web da aplicação.

---

## 5. QUANDO CONSIDERAR A ADOÇÃO DE CAPTCHA

O CAPTCHA **não foi implementado preventivamente** para resguardar a acessibilidade (WCAG 2.2 AA) e a experiência emocional serena do paciente.
- **Critério de Ativação Futura:**
  - Somente considerar CAPTCHA acessível (ex.: Cloudflare Turnstile com fallback de texto) se bots sofisticados começarem a contornar o Honeypot e gerarem mais de 50 mensagens manuais de spam por dia mesmo com o rate limiter ativo.
  - Exigirá revisão do Mapa de Dados (LGPD) e auditoria de acessibilidade.

---

## 6. QUANDO LEVAR A PROTEÇÃO PARA O PROXY OU WAF

Se o ataque de abuso escalar para além da camada da aplicação:
- **Cenários Indicativos:**
  1. *Ataque Volumétrico / DDoS:* Milhares de requisições por segundo esgotando conexões do servidor web (Nginx / Gunicorn).
  2. *Ataque Distribuído:* Milhares de IPs distintos disparando 1 tentativa cada, contornando o limite por IP individual.
- **Ação:** Ativar regras de proteção de borda no **Cloudflare WAF** ou **Nginx `limit_req`**, bloqueando o tráfego malicioso antes que atinja o processo Python do Django.

---

## 7. QUANDO REVISAR LOGS E INVESTIGAR CREDENTIAL STUFFING

- **Sintoma:** Ocorrência continuada de `admin_login_ip` ou `admin_login_combo` nos logs por dias seguidos.
- **Investigação:**
  1. Verificar no servidor se os acessos ao painel administrativo estão restritos ao domínio seguro sob HTTPS.
  2. Certificar-se de que os superusuários utilizam senhas fortes com mais de 12 caracteres (já assegurado pelo `MinimumLengthValidator`).
  3. Avaliar a alteração da rota administrativa através da variável `ADMIN_URL_PATH` no arquivo `.env`.
  4. Planejar a adoção futura de autenticação em dois fatores (MFA/2FA) para contas de gestão.
