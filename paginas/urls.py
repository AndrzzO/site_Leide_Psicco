"""URLs do app paginas."""
from django.urls import path
from . import views

app_name = 'paginas'

urlpatterns = [
    path('', views.home, name='inicio'),
    path('credenciamento/', views.credenciamento, name='credenciamento'),
    path('sobre-mim/', views.sobre_mim, name='sobre_mim'),
    path('politica-de-privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('privacidade/', views.politica_privacidade, name='privacidade'),
    path('politica-de-cookies/', views.politica_cookies, name='politica_cookies'),
    path('cookies/', views.politica_cookies, name='cookies'),
    path('design-system/', views.laboratorio_design_system, name='laboratorio_design_system'),
]


