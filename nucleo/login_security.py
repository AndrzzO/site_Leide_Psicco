"""Bloqueio persistente e reserva atômica por IP antes de verificar senhas."""
from datetime import timedelta
from functools import wraps
import uuid
from django.db import DatabaseError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .models import BloqueioLogin
from .rate_limit import obter_ip_cliente, gerar_digest_origem


def disponivel(agora):
    return Q(permanente=False) & (Q(bloqueado_ate__isnull=True) | Q(bloqueado_ate__lte=agora))


def resposta_bloqueada(request):
    return render(request, 'erros/404.html', status=404)


def proteger_login(view):
    @wraps(view)
    @sensitive_post_parameters('password')
    @csrf_protect
    def protegida(request, *args, **kwargs):
        token = None
        registro = None
        try:
            agora = timezone.now()
            origem = gerar_digest_origem('login', obter_ip_cliente(request))
            registros = BloqueioLogin.objects.filter(origem=origem)
            if registros.exclude(disponivel(agora)).exists():
                response = resposta_bloqueada(request)
            elif request.method != 'POST':
                response = view(request, *args, **kwargs)
            else:
                registro, _ = BloqueioLogin.objects.get_or_create(origem=origem)
                token = uuid.uuid4().hex
                # Compare-and-swap funciona em SQLite e PostgreSQL, entre processos.
                # Apenas uma autenticação cara por IP fica em andamento por vez.
                reservado = registros.filter(disponivel(agora)).filter(
                    Q(reserva_ate__isnull=True) | Q(reserva_ate__lte=agora)
                ).update(reserva_token=token, reserva_ate=agora + timedelta(minutes=2))
                if not reservado:
                    response = resposta_bloqueada(request)
                else:
                    response = view(request, *args, **kwargs)
                    if response.status_code == 200:
                        registro.refresh_from_db()
                        falhas = registro.falhas + 1
                        valores = {'falhas': falhas}
                        if falhas >= 10:
                            nivel = min(registro.nivel + 1, 5)
                            horas = 2 ** nivel
                            valores.update(falhas=0, nivel=nivel, permanente=horas > 20,
                                           bloqueado_ate=timezone.now() + timedelta(hours=min(horas, 20)))
                        registros.filter(reserva_token=token).update(**valores)
                        if falhas >= 10:
                            response = resposta_bloqueada(request)
        except DatabaseError:
            # Não autenticar sem proteção quando o banco estiver indisponível.
            response = HttpResponse('Acesso temporariamente indisponível.', status=503)
        finally:
            if token and registro:
                try:
                    BloqueioLogin.objects.filter(pk=registro.pk, reserva_token=token).update(reserva_token='', reserva_ate=None)
                except DatabaseError:
                    pass
        response['Cache-Control'] = 'no-store, private'
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
    return protegida
