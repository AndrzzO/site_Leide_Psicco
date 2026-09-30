"""
Configuração WSGI para o projeto Instituto Mente em Foco.
Expõe o callable WSGI como uma variável em nível de módulo chamada ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracoes.settings.desenvolvimento')

application = get_wsgi_application()
