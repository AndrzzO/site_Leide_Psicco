"""
Verificações de integridade de sistema do Django (System Checks) para SEO e Indexação.
Garante que ambientes de desenvolvimento/teste não sejam indexados e que configurações
críticas de produção estejam corretas.
"""
from django.core.checks import Error, Warning, register, Tags
from django.conf import settings


@register(Tags.security)
def verificar_configuracoes_seo(app_configs, **kwargs):
    """
    Executa validações preventivas quando SEO_ALLOW_INDEXING estiver ativado.
    """
    erros = []
    allow_indexing = getattr(settings, 'SEO_ALLOW_INDEXING', False)
    debug_mode = getattr(settings, 'DEBUG', True)
    site_url = getattr(settings, 'SITE_URL', '').strip().lower()

    if allow_indexing:
        # E001: Impede indexação com DEBUG=True
        if debug_mode:
            erros.append(
                Error(
                    "SEO_ALLOW_INDEXING está ativo enquanto DEBUG=True.",
                    hint="A indexação pública só pode ser habilitada em produção com DEBUG=False.",
                    id="seo.E001",
                )
            )

        # E002: Impede indexação com SITE_URL vazia ou apontando para localhost / 127.0.0.1
        if not site_url or 'localhost' in site_url or '127.0.0.1' in site_url or 'example.com' in site_url:
            erros.append(
                Error(
                    f"SEO_ALLOW_INDEXING está ativo com SITE_URL inválida ou local: '{site_url}'.",
                    hint="Configure o domínio canônico real de produção em SITE_URL (ex: https://institutomenteemfoco.com.br).",
                    id="seo.E002",
                )
            )
        # W001: Alerta se SITE_URL não usar HTTPS em ambiente com indexação autorizada
        elif not site_url.startswith('https://'):
            erros.append(
                Warning(
                    f"SITE_URL não utiliza HTTPS em ambiente com indexação autorizada: '{site_url}'.",
                    hint="Configure o protocolo HTTPS em SITE_URL para conformidade de SEO e segurança.",
                    id="seo.W001",
                )
            )

    return erros


@register(Tags.security)
def verificar_configuracoes_rate_limit(app_configs, **kwargs):
    """
    Executa validações preventivas sobre as variáveis de configuração de rate limit.
    Garante que limites e janelas de tempo sejam números inteiros positivos.
    """
    erros = []
    configs_positivas = [
        ('CONTACT_RATE_LIMIT_COUNT', getattr(settings, 'CONTACT_RATE_LIMIT_COUNT', 5)),
        ('CONTACT_RATE_LIMIT_WINDOW', getattr(settings, 'CONTACT_RATE_LIMIT_WINDOW', 900)),
        ('ADMIN_LOGIN_IP_LIMIT', getattr(settings, 'ADMIN_LOGIN_IP_LIMIT', 10)),
        ('ADMIN_LOGIN_IP_WINDOW', getattr(settings, 'ADMIN_LOGIN_IP_WINDOW', 900)),
        ('ADMIN_LOGIN_IP_BLOCK', getattr(settings, 'ADMIN_LOGIN_IP_BLOCK', 900)),
        ('ADMIN_LOGIN_COMBO_LIMIT', getattr(settings, 'ADMIN_LOGIN_COMBO_LIMIT', 5)),
        ('ADMIN_LOGIN_COMBO_WINDOW', getattr(settings, 'ADMIN_LOGIN_COMBO_WINDOW', 900)),
        ('ADMIN_LOGIN_COMBO_BLOCK', getattr(settings, 'ADMIN_LOGIN_COMBO_BLOCK', 900)),
    ]

    for nome, valor in configs_positivas:
        if not isinstance(valor, int) or valor <= 0:
            erros.append(
                Error(
                    f"A configuração '{nome}' deve ser um número inteiro estritamente positivo (atual: {valor}).",
                    hint="Defina um valor inteiro maior que zero no arquivo .env ou em settings.",
                    id="ratelimit.E001",
                )
            )

    return erros
