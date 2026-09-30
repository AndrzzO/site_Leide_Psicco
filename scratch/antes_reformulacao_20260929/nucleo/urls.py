"""URLs do app nucleo."""
from django.urls import path
from . import views

app_name = 'nucleo'

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('health/ready/', views.health_ready, name='health_ready'),
]
