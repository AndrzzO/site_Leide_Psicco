"""
Views do app contato:
- index: Página de Canais de Contato e Formulário Seguro com validação server-side,
  honeypot contra bots, rate limiting transitório via cache e padrão Post/Redirect/Get.
"""
import logging
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
        form = ContatoForm()

    contexto = {
        'form': form,
        'titulo_pagina': 'Contato e Agendamento | Instituto Mente em Foco',
        'meta_descricao': (
            'Entre em contato com o Instituto Mente em Foco. Atendimento ético e '
            'acolhedor em Psicologia e Neuropsicologia com a Psicóloga Mari Menezes.'
        ),
    }
    return render(request, 'contato/index.html', contexto)
