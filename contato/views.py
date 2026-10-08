"""
Views do app contato:
- index: Página de Canais de Contato e Formulário Seguro com validação server-side,
  honeypot contra bots, rate limiting transitório via cache e padrão Post/Redirect/Get.
"""
import logging
from urllib.parse import quote, urlsplit
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
from nucleo.models import ConfiguracaoSite
from nucleo.rate_limit import RateLimiter, criar_resposta_429
from .forms import ContatoForm

logger = logging.getLogger(__name__)


@sensitive_post_parameters('nome', 'email', 'telefone', 'mensagem')
def index(request):
    """
    Página institucional de Canais de Contato e Formulário Seguro.
    Implementa o padrão Post/Redirect/Get (PRG) com feedback via Django Messages.
    """
    if request.method == 'POST':
        # 1. Verificação de Rate Limit transitório
        permitido, retry_after = RateLimiter.verificar_contato(request)
        if not permitido:
            return criar_resposta_429(request, retry_after=retry_after, escopo='contato')

        form = ContatoForm(request.POST)

        # 2. Validação do formulário
        if form.is_valid():
            # Proteção Honeypot: se for bot, descarta silenciosamente sem poluir o banco
            if getattr(form, 'is_spam', False):
                logger.info("Envio de formulário descartado por detecção de honeypot.")
                messages.success(
                    request,
                    "Mensagem enviada com sucesso! Entraremos em contato pelos dados informados."
                )
                return redirect('contato:index')

            if request.POST.get('destino') == 'whatsapp':
                from nucleo.context_processors import dados_institucionais
                link_padrao = dados_institucionais(request)['WHATSAPP_LINK']
                if link_padrao:
                    dados = form.cleaned_data
                    linhas = [f"Olá Dra. Marileide, me chamo {dados['nome']}."]
                    servico = dados.get('servico_interesse')
                    linhas.append(f"Quero saber mais a respeito de {servico.nome}." if servico else 'Quero saber mais a respeito dos seus atendimentos.')
                    if dados.get('mensagem'):
                        linhas.append(dados['mensagem'])
                    contatos = []
                    if dados.get('telefone'):
                        contatos.append(f"Telefone: {dados['telefone']}")
                    if dados.get('email'):
                        contatos.append(f"E-mail: {dados['email']}")
                    linhas.append('\n'.join(contatos))
                    numero = urlsplit(link_padrao).path.strip('/')
                    texto = "\n\n".join(linhas)
                    resposta = render(request, 'contato/abrir_whatsapp.html', {
                        'whatsapp_destino': f"https://wa.me/{numero}?text={quote(texto, safe='')}",
                        'texto_whatsapp': texto,
                    })
                    resposta['Cache-Control'] = 'no-store, private'
                    resposta['Referrer-Policy'] = 'no-referrer'
                    return resposta

            # Salva mensagem legítima no banco
            mensagem_obj = form.save()

            # Notificação opcional por e-mail para a equipe (sem quebrar se o envio falhar)
            configuracao = ConfiguracaoSite.get_solo()
            if configuracao.email and configuracao.email != 'PENDENTE_DEFINICAO':
                try:
                    assunto = "[Novo Contato] Nova mensagem recebida pelo site"
                    corpo = (
                        f"Uma nova mensagem de contato foi recebida pelo site do Instituto Mente em Foco.\n\n"
                        f"Nome: {mensagem_obj.nome}\n"
                        f"E-mail: {mensagem_obj.email or 'Não informado'}\n"
                        f"Telefone: {mensagem_obj.telefone or 'Não informado'}\n"
                        f"Serviço de Interesse: {mensagem_obj.servico_interesse or 'Não especificado'}\n"
                        f"Data: {mensagem_obj.criado_em.strftime('%d/%m/%Y às %H:%M')}\n\n"
                        f"Para visualizar o conteúdo completo com segurança, acesse o painel administrativo."
                    )
                    send_mail(
                        assunto,
                        corpo,
                        getattr(settings, 'DEFAULT_FROM_EMAIL', 'contato@institutomenteemfoco.com.br'),
                        [configuracao.email],
                        fail_silently=True
                    )
                except Exception:
                    logger.warning("Falha técnica ao despachar notificação interna de e-mail de contato.")

            messages.success(
                request,
                "Mensagem enviada com sucesso! Entraremos em contato pelos dados informados."
            )
            # Padrão Post/Redirect/Get: previne reenvio por atualização de página
            return redirect('contato:index')
        else:
            messages.error(
                request,
                "Não foi possível enviar a mensagem. Por favor, verifique os campos destacados abaixo."
            )
    else:
        assuntos = {
            'avaliacao': 'Gostaria de solicitar uma avaliação psicológica.',
            'consulta': 'Gostaria de agendar uma consulta.',
            'psicoterapia': 'Gostaria de informações sobre psicoterapia.',
            'credenciamento': 'Tenho interesse no credenciamento de psicólogos.',
        }
        from servicos.editorial import AVALIACOES
        assuntos.update({a['slug']: 'Gostaria de informações sobre ' + a['h1'].lower() + '.' for a in AVALIACOES})
        mensagem_inicial = assuntos.get(request.GET.get('assunto', ''), '')
        form = ContatoForm(initial={'mensagem': mensagem_inicial})

    contexto = {
        'form': form,
        'enviar_whatsapp': True,
        'titulo_pagina': 'Contato e Agendamento | Instituto Mente em Foco',
        'meta_descricao': (
            'Entre em contato com o Instituto Mente em Foco. Atendimento ético e '
            'acolhedor em avaliações psicológicas e psicoterapia com Mari Menezes.'
        ),
    }
    return render(request, 'contato/index.html', contexto)

