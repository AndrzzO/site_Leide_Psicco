"""
Roteador de URLs do app conteudos (Blog / Conteúdos Educativos).
Rotas limpas e semânticas para index geral, filtro por categoria e detalhe do artigo.
"""
from django.urls import path
from . import views

app_name = 'conteudos'

urlpatterns = [
    # Listagem geral de conteúdos com paginação e busca
    path('', views.index, name='index'),

    # Filtro semântico por categoria
    path('categoria/<slug:categoria_slug>/', views.index, name='categoria'),

    # Visualização detalhada do artigo individual
    path('<slug:slug>/', views.detalhe, name='detalhe'),
]
