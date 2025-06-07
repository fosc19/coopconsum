from django.urls import path
from . import views

urlpatterns = [
    path('api/eventos/', views.api_eventos_calendario, name='api_eventos_calendario'),
]