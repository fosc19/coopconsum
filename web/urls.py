from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='web_home'), # Página principal
    path('qui-som/', views.quienes_somos, name='web_quienes_somos'),
    path('productors/', views.productores, name='web_productores'),
    path('productes/', views.productos, name='web_productos'),
    path('contacte/', views.contacto, name='web_contacto'),
    path('com-apuntar-se/', views.com_apuntarse, name='web_com_apuntarse'), # Nueva URL
    path('imatges/', views.galeria, name='web_galeria'),
    path('cooperatives/', views.cooperatives, name='web_cooperatives'), # Nueva página para cooperativas
    path('ajuda/', views.ajuda, name='web_ajuda'), # Página de ayuda interactiva
]