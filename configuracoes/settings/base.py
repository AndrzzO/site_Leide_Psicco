"""
Configurações base do Django para o projeto Instituto Mente em Foco.
Contém definições comuns compartilhadas entre todos os ambientes.
"""
from pathlib import Path
from decouple import config

# Diretório raiz do projeto (onde está o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Aplicações instaladas
INSTALLED_APPS = [
    # Aplicações nativas do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Aplicações do Instituto Mente em Foco
    'nucleo.apps.NucleoConfig',
    'paginas.apps.PaginasConfig',
    'servicos.apps.ServicosConfig',
    'conteudos.apps.ConteudosConfig',
    'contato.apps.ContatoConfig',
]

# Middlewares essenciais de segurança e requisição
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csp.ContentSecurityPolicyMiddleware',
    'nucleo.middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nucleo.middleware.SEOMiddleware',
]

ROOT_URLCONF = 'configuracoes.urls'

# Configuração de templates com diretório global
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csp',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'nucleo.context_processors.dados_institucionais',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracoes.wsgi.application'

# Validação de senhas do Django Admin (fortalecida com mínimo de 12 caracteres)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configurações de Headers de Segurança Base (padrão)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_CSP = {}
SECURE_CSP_REPORT_ONLY = {}



# Internacionalização e Localização (Brasil)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, Imagens do tema)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Arquivos de mídia (Uploads do CMS: fotos profissionais e capas)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuração padronizada de Storages (Django 5/6)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rota configurável do Admin
DJANGO_ADMIN_URL = config('DJANGO_ADMIN_URL', default='admin/')

# Configurações institucionais carregadas de variáveis de ambiente
# (Valores não definidos utilizam o marcador padrão PENDENTE_DEFINICAO)
WHATSAPP_NUMERO = config('WHATSAPP_NUMERO', default='PENDENTE_DEFINICAO')
EMAIL_CONTATO = config('EMAIL_CONTATO', default='PENDENTE_DEFINICAO')
INSTAGRAM_URL = config('INSTAGRAM_URL', default='PENDENTE_DEFINICAO')
CRP_PROFISSIONAL = config('CRP_PROFISSIONAL', default='PENDENTE_DEFINICAO')
SITE_URL = config('SITE_URL', default='http://localhost:8000').rstrip('/')

# Governança de SEO e Indexação por Ambiente
# Em desenvolvimento/staging este valor DEVE ser False para impedir indexação em buscadores.
# Em produção, após conferência dos metadados e SSL, defina SEO_ALLOW_INDEXING=True no .env.
SEO_ALLOW_INDEXING = config('SEO_ALLOW_INDEXING', default=False, cast=bool)

# Verificação de Propriedade do Domínio (Google Search Console e Bing Webmaster Tools)
GOOGLE_SITE_VERIFICATION = config('GOOGLE_SITE_VERIFICATION', default='')
BING_SITE_VERIFICATION = config('BING_SITE_VERIFICATION', default='')

# Governança de Dados e Retenção (LGPD)
# Prazo de retenção de mensagens de contato em dias (se None/vazio, nenhuma exclusão automática é realizada)
def _converter_retencao_dias(valor):
    if valor and str(valor).strip().isdigit():
        return int(valor)
    return None

CONTATO_RETENCAO_DIAS = config('CONTATO_RETENCAO_DIAS', default=None, cast=_converter_retencao_dias)

# Cache Transitório da Aplicação (usado para rate limiting e throttling de segurança)
# Em desenvolvimento e mono-instância, LocMemCache provê contadores atômicos in-memory.
# Em produção multi-worker/distribuída, recomenda-se backend compartilhado (Redis/Memcached) ou WAF de borda.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'mente-em-foco-cache-local',
    }
}

# Proteção contra Abuso, Rate Limiting e Brute Force (Prompt 17)
# Limites do Formulário de Contato (POST)
CONTACT_RATE_LIMIT_COUNT = config('CONTACT_RATE_LIMIT_COUNT', default=5, cast=int)
CONTACT_RATE_LIMIT_WINDOW = config('CONTACT_RATE_LIMIT_WINDOW', default=900, cast=int)

# Limites do Login Administrativo (POST)
ADMIN_LOGIN_IP_LIMIT = config('ADMIN_LOGIN_IP_LIMIT', default=10, cast=int)
ADMIN_LOGIN_IP_WINDOW = config('ADMIN_LOGIN_IP_WINDOW', default=900, cast=int)
ADMIN_LOGIN_IP_BLOCK = config('ADMIN_LOGIN_IP_BLOCK', default=900, cast=int)

ADMIN_LOGIN_COMBO_LIMIT = config('ADMIN_LOGIN_COMBO_LIMIT', default=5, cast=int)
ADMIN_LOGIN_COMBO_WINDOW = config('ADMIN_LOGIN_COMBO_WINDOW', default=900, cast=int)
ADMIN_LOGIN_COMBO_BLOCK = config('ADMIN_LOGIN_COMBO_BLOCK', default=900, cast=int)

# Confiança em cabeçalho X-Forwarded-For para resolução de IP (SOMENTE ativar atrás de proxy reverso homologado)
TRUST_PROXY_CLIENT_IP = config('TRUST_PROXY_CLIENT_IP', default=False, cast=bool)

# Logging base
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'padrao': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'padrao',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
