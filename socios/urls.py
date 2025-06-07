from django.urls import path
from .views import home, enviar_ingreso

urlpatterns = [
    path('', home, name='socios_home'),
    path('enviar-ingreso/', enviar_ingreso, name='enviar_ingreso'),
]
