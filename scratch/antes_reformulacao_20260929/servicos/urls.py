"""URLs do app servicos."""
from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('psicologia/', views.psicologia, name='psicologia'),
    path('neuropsicologia/', views.neuropsicologia, name='neuropsicologia'),
    path('traumas/', views.traumas, name='traumas'),
    path('separacao-e-recomecos/', views.separacao_recomecos, name='separacao_recomecos'),
    path('novos-relacionamentos/', views.novos_relacionamentos, name='novos_relacionamentos'),
    path('avaliacao/', views.avaliacao, name='avaliacao'),
    path('avaliacao-psicologica/', views.avaliacao_psicologica, name='avaliacao_psicologica'),
    path('avaliacao-neuropsicologica/', views.avaliacao_neuropsicologica, name='avaliacao_neuropsicologica'),
    path('reabilitacao-neurocognitiva/', views.reabilitacao_neurocognitiva, name='reabilitacao_neurocognitiva'),
]
