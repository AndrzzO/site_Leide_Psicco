"""
Roteador principal de URLs do Instituto Mente em Foco.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from nucleo.views import robots_txt
from nucleo.sitemaps import sitemaps

# Configuração customizada dos títulos do Django Admin
admin.site.site_header = "Instituto Mente em Foco — Gestão Administrativa"
admin.site.site_title = "Admin Mente em Foco"
admin.site.index_title = "Painel de Controle Institucional"

# Garante que a rota do admin seja limpa de barras duplas
admin_path = settings.DJANGO_ADMIN_URL.strip('/') + '/'

urlpatterns = [
    # SEO Técnico: robots.txt e sitemap.xml
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Rota configurável do painel administrativo
    path(admin_path, admin.site.urls),

    # App nucleo (health check, utilitários globais)
    path('', include('nucleo.urls')),

    # App paginas (Home, Sobre Mim, Políticas)
    path('', include('paginas.urls')),

    # Apps modulares para desenvolvimento incremental
    path('servicos/', include('servicos.urls')),
    path('conteudos/', include('conteudos.urls')),
    path('contato/', include('contato.urls')),
]

# Handlers globais de erro HTTP customizados e acolhedores
handler400 = 'nucleo.views.tratar_erro_400'
handler403 = 'nucleo.views.tratar_erro_403'
handler404 = 'nucleo.views.tratar_erro_404'
handler500 = 'nucleo.views.tratar_erro_500'

# Em ambiente de desenvolvimento local, servir arquivos de mídia pelo Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
