from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear el router para los ViewSets
router = DefaultRouter()
router.register(r'proveedores', views.ProveedorViewSet, basename='proveedor')
router.register(r'productos', views.ProductoViewSet, basename='producto')
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    # Información de la API
    path('', views.api_info, name='api_info'),
    
    # Incluir todas las rutas del router
    path('', include(router.urls)),
]