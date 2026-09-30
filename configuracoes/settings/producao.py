"""
Configurações para ambiente de produção do Instituto Mente em Foco.
Ativa proteções estritas de segurança, desativa DEBUG e valida variáveis essenciais.
"""
from django.core.exceptions import ImproperlyConfigured
from decouple import config, Csv
import dj_database_url
from django.utils.csp import CSP
from .base import *

# Em produção, DEBUG é rigorosamente False
DEBUG = False

# Validação estrita da SECRET_KEY em produção
# Em produção, a chave deve ser fornecida por variável de ambiente segura
SECRET_KEY = config('DJANGO_SECRET_KEY', default=None)
if not SECRET_KEY or 'django-insecure' in SECRET_KEY or 'chavelocal' in SECRET_KEY or 'sua-chave' in SECRET_KEY:
    raise ImproperlyConfigured(
        'A variável de ambiente DJANGO_SECRET_KEY é obrigatória e deve conter '
        'uma chave segura única em ambiente de produção (sem prefixo django-insecure ou placeholder).'
    )

# Hosts permitidos em produção (não aceita vazio nem wildcard irrestrito '*')
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='', cast=Csv())
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        'A variável DJANGO_ALLOWED_HOSTS deve ser definida explicitamente em produção '
        'e não pode conter wildcard irrestrito (*).'
    )

# Origens confiáveis para submissão CSRF
CSRF_TRUSTED_ORIGINS = config('DJANGO_CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# Banco de dados em produção (PostgreSQL gerenciado via DATABASE_URL)
DATABASE_URL = config('DATABASE_URL', default=None)
if not DATABASE_URL:
    raise ImproperlyConfigured(
        'A variável DATABASE_URL deve ser definida em produção apontando para o banco relacional.'
    )

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}

# Proteções e Headers de Segurança HTTP/HTTPS em Produção
SECURE_SSL_REDIRECT = config('DJANGO_SECURE_SSL_REDIRECT', default=config('SECURE_SSL_REDIRECT', default=True, cast=bool), cast=bool)

# HSTS com Rollout Progressivo e Seguro
# Durante a fase de preparação pré-deploy o padrão seguro é 0 (desativado).
# Após o domínio final e os certificados TLS estarem validados em produção,
# incremente progressivamente: 300 (5 min) -> 86400 (1 dia) -> 31536000 (1 ano).
SECURE_HSTS_SECONDS = config('DJANGO_SECURE_HSTS_SECONDS', default=config('SECURE_HSTS_SECONDS', default=0, cast=int), cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('DJANGO_SECURE_HSTS_PRELOAD', default=False, cast=bool)

# Cookies seguros (somente trafegados via canal criptografado HTTPS)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # Mantido False para compatibilidade e integridade do fluxo de formulários
CSRF_COOKIE_SAMESITE = 'Lax'

# Proteções contra MIME-sniffing, Clickjacking e isolamento de janelas
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Header de Proxy Reverso: SOMENTE ativar quando o provedor/proxy terminar TLS de forma comprovada
_proxy_ssl_header_enabled = config('DJANGO_SECURE_PROXY_SSL_HEADER', default=False, cast=bool)
if _proxy_ssl_header_enabled:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    SECURE_PROXY_SSL_HEADER = None

# Content Security Policy (CSP) nativa do Django 6.0
SECURE_CSP = {
    'default-src': [CSP.SELF],
    'script-src': [CSP.SELF, CSP.NONCE],
    'style-src': [CSP.SELF, CSP.UNSAFE_INLINE, 'https://fonts.googleapis.com'],
    'font-src': [CSP.SELF, 'https://fonts.gstatic.com', 'data:'],
    'img-src': [CSP.SELF, 'data:'],
    'connect-src': [CSP.SELF],
    'object-src': [CSP.NONE],
    'base-uri': [CSP.SELF],
    'form-action': [CSP.SELF],
    'frame-ancestors': [CSP.NONE],
    'frame-src': [CSP.NONE],
}

# Suporte a Content-Security-Policy-Report-Only para homologação / diagnóstico
if config('DJANGO_SECURE_CSP_REPORT_ONLY', default=False, cast=bool):
    SECURE_CSP_REPORT_ONLY = SECURE_CSP
    SECURE_CSP = {}

# Envio de E-mails em Produção (SMTP configurável via variáveis de ambiente)
# Se EMAIL_HOST não for fornecido, a aplicação continua funcionando normalmente;
# as mensagens de contato são preservadas com integridade na base de dados relacional.
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# Suporte opcional a ManifestStaticFilesStorage se configurado pelo deploy
if config('DJANGO_MANIFEST_STATIC_STORAGE', default=False, cast=bool):
    STORAGES['staticfiles'] = {
        'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    }

# Logging estruturado para produção (nível WARNING, sem registrar senhas ou dados clínicos)
LOGGING['root']['level'] = 'WARNING'
