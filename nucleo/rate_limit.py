"""
Módulo de proteção contra abuso, rate limiting e defesa contra brute force.
Implementação centralizada, minimalista e segura:
- Identificação de cliente com preferência estrita por REMOTE_ADDR (anti-spoofing).
- Pseudonimização irreversível via HMAC-SHA256 com SECRET_KEY (zero IP nos logs/cache).
- Limites direcionados exclusivamente a POST sensíveis (Contato e Login Admin).
- Resiliência fail-open em caso de falha de backend de cache (zero HTTP 500 indevido).
- Resposta HTTP 429 padronizada com cabeçalhos Retry-After e Cache-Control: no-store.
"""
import hashlib
import hmac
import logging
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

logger = logging.getLogger(__name__)


def obter_ip_cliente(request) -> str:
    """
    Recupera o endereço IP do cliente de forma segura:
    - Se TRUST_PROXY_CLIENT_IP for False (padrão seguro): utiliza estritamente REMOTE_ADDR,
      ignorando solenemente cabeçalhos HTTP_X_FORWARDED_FOR passíveis de falsificação.
    - Se TRUST_PROXY_CLIENT_IP for True: inspeciona HTTP_X_FORWARDED_FOR configurado pelo proxy.
    """
    confia_proxy = getattr(settings, 'TRUST_PROXY_CLIENT_IP', False)
    if confia_proxy:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Em arquitetura com proxy confiável, o IP do cliente é o primeiro endereço da cadeia
            primeiro_ip = x_forwarded_for.split(',')[0].strip()
            if primeiro_ip:
                return primeiro_ip

    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def gerar_digest_origem(escopo: str, identificador: str) -> str:
    """
    Gera um digest HMAC-SHA256 de 32 caracteres para pseudonimizar a origem.
    Evita a pré-computação do espaço de IPv4 e impede a exposição de IPs ou nomes
    de usuário em texto puro nas chaves de cache e nos arquivos de log.
    """
    segredo = getattr(settings, 'SECRET_KEY', 'mente-em-foco-default-secret').encode('utf-8')
    mensagem = f"{escopo}:{identificador}".encode('utf-8')
    return hmac.new(segredo, mensagem, hashlib.sha256).hexdigest()[:32]


def criar_resposta_429(request, retry_after: int = 900, escopo: str = 'geral'):
    """
    Gera uma resposta HTTP 429 Too Many Requests com template acessível,
    cabeçalho Retry-After e política Cache-Control: no-store.
    Preserva os cabeçalhos de segurança do projeto (CSP, X-Frame-Options, nosniff).
    """
    logger.warning("Rate limit excedido no escopo '%s'. Resposta HTTP 429 retornada.", escopo)
    response = render(request, 'erros/429.html', status=429)
    response['Retry-After'] = str(max(1, int(retry_after)))
    response['Cache-Control'] = 'no-store'
    return response


class RateLimiter:
    """
    Gerenciador centralizado de rate limit transitório via Django Cache.
    Utiliza namespace padronizado 'security:rl:v1:' e expiração automática por TTL.
    """

    @classmethod
    def verificar_contato(cls, request) -> tuple[bool, int]:
        """
        Verifica a cota de submissões do formulário de contato por origem.
        Retorna (True, 0) se permitido, ou (False, retry_after) se bloqueado.
        """
        limite = getattr(settings, 'CONTACT_RATE_LIMIT_COUNT', 5)
        janela = getattr(settings, 'CONTACT_RATE_LIMIT_WINDOW', 900)

        ip = obter_ip_cliente(request)
        digest = gerar_digest_origem('contato', ip)

        chave_tentativas = f"security:rl:v1:contato:attempts:{digest}"
        chave_bloqueio = f"security:rl:v1:contato:block:{digest}"

        try:
            # 1. Verifica se a origem já está sob bloqueio temporário
            if cache.get(chave_bloqueio):
                return False, janela

            # 2. Incrementa contador de tentativas dentro da janela
            tentativas = cache.get(chave_tentativas)
            if tentativas is None:
                cache.set(chave_tentativas, 1, timeout=janela)
                return True, 0

            if tentativas < limite:
                cache.set(chave_tentativas, tentativas + 1, timeout=janela)
                return True, 0

            # 3. Limite atingido: ativa bloqueio temporário
            cache.set(chave_bloqueio, 1, timeout=janela)
            return False, janela

        except Exception:
            # Resiliência Fail-Open: se o cache falhar, não derruba a aplicação com 500
            logger.warning("Indisponibilidade no backend de cache durante rate limit de contato.")
            return True, 0



def wrap_admin_login(admin_site):
    if getattr(admin_site, '_rate_limit_wrapped', False):
        return
    from .login_security import proteger_login
    admin_site.login = proteger_login(admin_site.login)
    admin_site._rate_limit_wrapped = True
