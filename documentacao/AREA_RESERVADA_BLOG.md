# Área reservada do Blog

## Uso

O link **Área reservada** fica no rodapé, abaixo das políticas. O endereço é `/area-cliente/entrar/`.
A conta solicitada foi configurada no banco local, com senha armazenada pelo hash do Django. A conta possui apenas a permissão `conteudos.gerenciar_blog`; não é staff nem superusuária. O painel permite gerenciar todos os artigos institucionais existentes.

A autora pode escrever com negrito, itálico, subtítulos, listas e citações; escolher Montserrat, Georgia, Arial ou Palatino; adicionar capa; salvar rascunhos; publicar; editar e excluir. O servidor remove estilos, tamanhos arbitrários e elementos HTML não permitidos. A fonte afeta o corpo do artigo; a hierarquia visual é definida pelo site.

## Expiração automática

A data usa o fuso America/Sao_Paulo. Ao atingir o prazo, o artigo deixa imediatamente de aparecer nas consultas públicas, detalhes e sitemap. O comando `python manage.py apagar_artigos_expirados` exclui os registros vencidos do banco. A exclusão não remove cópias em backups nem arquivos de capa do armazenamento.

No computador local foi registrada a tarefa do Windows `MenteEmFoco-ExpirarBlog`, executada a cada minuto com o usuário conectado. Última execução verificada com resultado 0. Se o computador estiver desligado, executará novamente quando disponível. A retirada pública não depende dessa tarefa.

### Publicação no servidor

A tarefa do Windows não é transferida junto com o código. Configure no agendador da hospedagem, a cada minuto, com o mesmo banco e ambiente do servidor web:

```sh
cd /caminho/do/site && /caminho/da/venv/bin/python manage.py apagar_artigos_expirados
```

Ou mantenha `python manage.py apagar_artigos_expirados --continuo` sob o supervisor da hospedagem, com reinício automático. A exclusão física ocorre na próxima execução (normalmente em até um minuto). Não deixar o processo solto sem supervisor em produção.

Aplicar `migrate` e `collectstatic`. Se a hospedagem usar um banco novo, criar a conta pelo procedimento administrativo, usando o e-mail em minúsculas como username e atribuindo `conteudos.gerenciar_blog`. A senha local não está em migrations nem em arquivos de código.

## Proteção dos logins

Cliente e Django Admin compartilham o contador por origem. A décima falha retorna 404 e bloqueia GET e POST do login. A sequência é 2, 4, 8, 16 horas e bloqueio permanente na quinta reincidência (o próximo intervalo seria 32 horas, acima de 20). Acertos não apagam o histórico de falhas. Não há expiração automática do histórico de reincidências.

O estado está no banco, com IP pseudonimizado por HMAC. Uma reserva atômica por IP evita autenticações caras simultâneas. Requisições concorrentes durante a reserva recebem 404 e não somam falhas; reserva abandonada expira em dois minutos. Falha no banco fecha o login com 503. CSRF permanece obrigatório. IPs diferentes têm contadores independentes.

`TRUST_PROXY_CLIENT_IP=False` ignora cabeçalhos enviados pelo visitante. Só ativar atrás de proxy que sobrescreva X-Forwarded-For e impeça acesso direto à aplicação. O bloqueio atua nos endpoints de login, não nas páginas públicas ou nas sessões já autenticadas. Ataques distribuídos e volume de rede exigem limites adicionais na hospedagem.

Para corrigir um bloqueio legítimo, executar no servidor:

```sh
python manage.py desbloquear_login 203.0.113.10
```

Isso limpa o contador e a reincidência desse IP. As antigas variáveis `ADMIN_LOGIN_*` de cache foram substituídas pela regra fixa acima. O limite do formulário de contato continua separado.

## Validação realizada

- 243 testes aprovados: permissões, CSRF, sanitização, publicação/rascunho, datas, sitemap, exclusão e progressão dos bloqueios.
- `check` sem problemas e `makemigrations --check` sem diferenças.
- Fluxo no Edge: login real, edição, publicação pública, exclusão e logout; sem erros JavaScript ou overflow horizontal no celular.
- Backup SQLite anterior à migração em `scratch/antes_painel_*.sqlite3` (ignorado pelo Git).

## Enquadramento da capa

No editor, selecionar uma foto mostra a prévia 16:9. Arraste com mouse ou toque; use Centralizar foto para restaurar o centro. As setas do teclado também deslocam a foto. Salvar/publicar o artigo guarda o enquadramento para a capa pública, os cards e os conteúdos relacionados. O arquivo original é preservado. Imagens com a mesma proporção do quadro já cabem inteiras; o deslocamento atua no eixo que possui sobra de imagem. Campos de posição são internos, limitados a 0–100 pelo servidor, sem entrada numérica visível.

Validação adicional: 11 testes do painel aprovados e fluxo de navegador com upload, arraste, salvamento, reabertura, centralização e posição na capa pública.

Atualização de exibição pública: capas, cards e destaques usam reduzir para caber (`object-fit: contain`), preservando a imagem completa com fundo neutro. Removido o zoom de hover que recortava bordas. Conferido no artigo existente em 1440px e 390px, além dos cards.

## Agendamento local desativado

Em 30/09/2026, a tarefa Windows `MenteEmFoco-ExpirarBlog` foi desativada a pedido do proprietário, pois iniciava o Python da venv automaticamente a cada minuto. A venv foi preservada e suas dependências verificadas. No ambiente local, os artigos vencidos continuam ocultos nas consultas públicas; a exclusão física depende de executar o comando manualmente. Na hospedagem, configurar o agendador conforme descrito acima.
