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

    @classmethod
    def verificar_login_ip(cls, ip: str) -> tuple[bool, int]:
        """Verifica se o IP de origem atingiu o limite de falhas de login."""
        janela_block = getattr(settings, 'ADMIN_LOGIN_IP_BLOCK', 900)
        digest = gerar_digest_origem('admin_ip', ip)
        chave_bloqueio = f"security:rl:v1:admin_ip:block:{digest}"

        try:
            if cache.get(chave_bloqueio):
                return False, janela_block
            return True, 0
        except Exception:
            logger.warning("Indisponibilidade no backend de cache durante verificação de login IP.")
            return True, 0

    @classmethod
    def verificar_login_combo(cls, ip: str, username: str) -> tuple[bool, int]:
        """Verifica se a combinação (origem, username) atingiu o limite de falhas."""
        janela_block = getattr(settings, 'ADMIN_LOGIN_COMBO_BLOCK', 900)
        username_norm = (username or '').strip().casefold()[:150]
        digest = gerar_digest_origem('admin_combo', f"{ip}:{username_norm}")
        chave_bloqueio = f"security:rl:v1:admin_combo:block:{digest}"

        try:
            if cache.get(chave_bloqueio):
                return False, janela_block
            return True, 0
        except Exception:
            logger.warning("Indisponibilidade no backend de cache durante verificação de login combo.")
            return True, 0

    @classmethod
    def registrar_falha_login(cls, ip: str, username: str) -> None:
        """
        Registra uma falha de autenticação para a origem e para a combinação (origem, username).
        Funciona uniformemente mesmo quando o usuário não existe, evitando enumeração de contas.
        """
        limite_ip = getattr(settings, 'ADMIN_LOGIN_IP_LIMIT', 10)
        janela_ip = getattr(settings, 'ADMIN_LOGIN_IP_WINDOW', 900)
        block_ip = getattr(settings, 'ADMIN_LOGIN_IP_BLOCK', 900)

        limite_combo = getattr(settings, 'ADMIN_LOGIN_COMBO_LIMIT', 5)
        janela_combo = getattr(settings, 'ADMIN_LOGIN_COMBO_WINDOW', 900)
        block_combo = getattr(settings, 'ADMIN_LOGIN_COMBO_BLOCK', 900)

        username_norm = (username or '').strip().casefold()[:150]

        digest_ip = gerar_digest_origem('admin_ip', ip)
        chave_tentativas_ip = f"security:rl:v1:admin_ip:attempts:{digest_ip}"
        chave_block_ip = f"security:rl:v1:admin_ip:block:{digest_ip}"

        digest_combo = gerar_digest_origem('admin_combo', f"{ip}:{username_norm}")
        chave_tentativas_combo = f"security:rl:v1:admin_combo:attempts:{digest_combo}"
        chave_block_combo = f"security:rl:v1:admin_combo:block:{digest_combo}"

        try:
            # Incrementa tentativas de IP
            tentativas_ip = cache.get(chave_tentativas_ip, 0) + 1
            cache.set(chave_tentativas_ip, tentativas_ip, timeout=janela_ip)
            if tentativas_ip >= limite_ip:
                cache.set(chave_block_ip, 1, timeout=block_ip)

            # Incrementa tentativas de Combo (Origem + Username)
            tentativas_combo = cache.get(chave_tentativas_combo, 0) + 1
            cache.set(chave_tentativas_combo, tentativas_combo, timeout=janela_combo)
            if tentativas_combo >= limite_combo:
                cache.set(chave_block_combo, 1, timeout=block_combo)

        except Exception:
            logger.warning("Indisponibilidade no backend de cache durante registro de falha de login.")

    @classmethod
    def limpar_login_combo(cls, ip: str, username: str) -> None:
        """
        Limpa os contadores de falhas da combinação (origem, username) após autenticação bem-sucedida.
        Preserva o contador de IP para que o atacante não resete seu orçamento global de tentativas.
        """
        username_norm = (username or '').strip().casefold()[:150]
        digest_combo = gerar_digest_origem('admin_combo', f"{ip}:{username_norm}")
        chave_tentativas_combo = f"security:rl:v1:admin_combo:attempts:{digest_combo}"
        chave_block_combo = f"security:rl:v1:admin_combo:block:{digest_combo}"

        try:
            cache.delete(chave_tentativas_combo)
            cache.delete(chave_block_combo)
        except Exception:
            logger.warning("Falha ao limpar contadores de cache após login bem-sucedido.")


def wrap_admin_login(admin_site):
    """
    Aplica envelope protetor sobre a view de login do Django Admin.
    Assegura que tentativas excessivas sofram rate limiting antes de invocar
    hashing de senha computacionalmente custoso (mitigando DoS de CPU).
    """
    if getattr(admin_site, '_rate_limit_wrapped', False):
        return

    original_login = admin_site.login

    @sensitive_post_parameters('password')
    def rate_limited_login(request, extra_context=None):
        if request.method != 'POST':
            # GET não consome contadores nem sofre rate limit
            return original_login(request, extra_context)

        ip = obter_ip_cliente(request)
        username = request.POST.get('username', '')

        # 1. Verifica bloqueio prévio do IP de origem
        permitido_ip, retry_after_ip = RateLimiter.verificar_login_ip(ip)
        if not permitido_ip:
            return criar_resposta_429(request, retry_after=retry_after_ip, escopo='admin_login_ip')

        # 2. Verifica bloqueio prévio da combinação (IP + Username)
        permitido_combo, retry_after_combo = RateLimiter.verificar_login_combo(ip, username)
        if not permitido_combo:
            return criar_resposta_429(request, retry_after=retry_after_combo, escopo='admin_login_combo')

        # 3. Invoca a autenticação padrão do Django
        response = original_login(request, extra_context)

        # 4. Avalia o resultado da tentativa
        if response.status_code == 302 and request.user.is_authenticated:
            # Login bem-sucedido: limpa o contador combo do par (IP, usuário)
            RateLimiter.limpar_login_combo(ip, username)
        elif response.status_code == 200:
            # Login falhou (formulário re-renderizado com erro): contabiliza tentativa
            RateLimiter.registrar_falha_login(ip, username)

        return response

    admin_site.login = rate_limited_login
    admin_site._rate_limit_wrapped = True
