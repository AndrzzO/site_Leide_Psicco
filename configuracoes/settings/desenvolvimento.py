"""
Configurações para ambiente de desenvolvimento local.
Permite depuração ativa, uso do SQLite e envio de e-mails para console.
"""
from decouple import config, Csv
import dj_database_url
from .base import *

# Em desenvolvimento, DEBUG é True por padrão
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

# Chave secreta de desenvolvimento (claramente identificada como insegura para prod)
SECRET_KEY = config(
    'DJANGO_SECRET_KEY',
    default='django-insecure-dev-local-mente-em-foco-chavelocal2026'
)

# Hosts permitidos em desenvolvimento local
ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost,127.0.0.1,[::1],testserver',
    cast=Csv()
)

# Origens confiáveis para CSRF em desenvolvimento
CSRF_TRUSTED_ORIGINS = config(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000',
    cast=Csv()
)

# Banco de dados local: SQLite como padrão, com suporte opcional a DATABASE_URL
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Envio de e-mails em desenvolvimento: direcionado para o console do terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
