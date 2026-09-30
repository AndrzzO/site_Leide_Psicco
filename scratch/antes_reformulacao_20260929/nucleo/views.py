"""
Views do app nucleo: Verificação de integridade (health check) e tratamento de erros HTTP.
"""
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def robots_txt(request):
    """
    Gera o conteúdo de robots.txt dinamicamente com base nas configurações de ambiente.
    Se SEO_ALLOW_INDEXING for False: bloqueia rastreamento com Disallow: /.
    Se SEO_ALLOW_INDEXING for True: permite rastreamento seguro e aponta para o sitemap.xml.
    Nunca expõe rotas administrativas privadas ou sensíveis.
    """
    allow_indexing = getattr(settings, 'SEO_ALLOW_INDEXING', False)
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000').rstrip('/')
    return render(
        request,
        'seo/robots.txt',
        {
            'SEO_ALLOW_INDEXING': allow_indexing,
            'SITE_URL': site_url,
        },
        content_type='text/plain; charset=utf-8'
    )


import logging
from django.db import connection

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Endpoint simples e seguro de liveness (health check).
    Retorna apenas 'OK' sem vazar detalhes de versão, banco ou infraestrutura.
    """
    response = HttpResponse("OK", content_type="text/plain", status=200)
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response


def health_ready(request):
    """
    Endpoint de prontidão (readiness check) para infraestrutura / load balancers.
    Executa consulta mínima de conectividade com o banco de dados (SELECT 1).
    Retorna 200 'OK' ou 503 'UNAVAILABLE' sem expor erros SQL ou secrets.
    """
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


def tratar_erro_400(request, exception=None):
    """Handler para erro 400 (Bad Request)."""
    return render(request, 'erros/400.html', status=400)


def tratar_erro_403(request, exception=None):
    """Handler para erro 403 (Acesso Negado)."""
    return render(request, 'erros/403.html', status=403)


def tratar_erro_404(request, exception=None):
    """Handler para erro 404 (Página Não Encontrada)."""
    return render(request, 'erros/404.html', status=404)


def tratar_erro_500(request):
    """Handler para erro 500 (Erro Interno do Servidor)."""
    return render(request, 'erros/500.html', status=500)
