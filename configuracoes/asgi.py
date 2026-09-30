"""
Configuração ASGI para o projeto Instituto Mente em Foco.
Expõe o callable ASGI como uma variável em nível de módulo chamada ``application``.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracoes.settings.desenvolvimento')

application = get_asgi_application()
