from django.urls import path
from . import painel_views as views
app_name = 'painel'
urlpatterns = [
    path('entrar/', views.entrar, name='login'),
    path('', views.index, name='index'),
    path('novo/', views.editar, name='novo'),
    path('artigo/<int:pk>/', views.editar, name='editar'),
    path('artigo/<int:pk>/excluir/', views.excluir, name='excluir'),
    path('sair/', views.sair, name='sair'),
]
