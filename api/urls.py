from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear el router per als ViewSets amb URLs en català
router = DefaultRouter()
router.register(r'proveidors', views.ProveedorViewSet, basename='proveidor')
router.register(r'productes', views.ProductoViewSet, basename='producte')
router.register(r'categories', views.CategoriaViewSet, basename='categoria')
router.register(r'esdeveniments', views.EventoCalendarioViewSet, basename='esdeveniment')

urlpatterns = [
    # Informació de l'API
    path('', views.api_info, name='api_info'),
    
    # Incloure totes les rutes del router
    path('', include(router.urls)),
]