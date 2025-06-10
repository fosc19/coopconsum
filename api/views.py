from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from productos.models import Producto, Proveedor, Categoria
from eventos.models import EventoCalendario
from .serializers import (
    ProductoSerializer, 
    ProveedorSerializer, 
    CategoriaSerializer,
    EventoCalendarioSerializer
)


@api_view(['GET'])
def api_info(request):
    """Informació bàsica de l'API"""
    return Response({
        'nom': 'API Cooperatives CoopConsum',
        'versio': '1.0',
        'descripcio': 'API pública per compartir informació entre cooperatives de consum',
        'documentacio': {
            'completa': '/docs/API_COOPERATIVAS.md',
            'exemples': '/docs/README_API.md'
        },
        'endpoints': {
            'proveedores': '/api/proveedores/',
            'productos': '/api/productos/',
            'categorias': '/api/categorias/',
            'eventos': '/api/eventos/',
        },
        'filtres_disponibles': {
            'productos': ['categoria', 'proveedor', 'es_stock', 'destacado_en_inicio'],
            'proveedores': ['visible_en_web', 'visible_en_inicio'],
            'eventos': ['color', 'fecha_inicio', 'fecha_fin']
        },
        'funcionalitats': [
            'Cerca per text en noms i descripcions',
            'Filtrat per múltiples camps',
            'Ordenació per diferents criteris',
            'Paginació automàtica (20 elements per pàgina)',
            'Format JSON estàndard',
            'CORS habilitat per cooperatives'
        ]
    })


class ProveedorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para proveedores públicos.
    Solo muestra proveedores marcados como visibles en web.
    """
    serializer_class = ProveedorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visible_en_web', 'visible_en_inicio']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        # Solo proveedores visibles en web
        return Proveedor.objects.filter(visible_en_web=True)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para categorías de productos.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']
    ordering = ['nombre']


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para productos públicos.
    Solo muestra productos de proveedores visibles en web.
    """
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'proveedor', 'es_stock', 'destacado_en_inicio']
    search_fields = ['nombre', 'descripcion', 'proveedor__nombre']
    ordering_fields = ['nombre', 'precio']
    ordering = ['nombre']
    
    def get_queryset(self):
        # Solo productos de proveedores visibles en web
        return Producto.objects.filter(proveedor__visible_en_web=True)


class EventoCalendarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para eventos del calendario.
    Muestra todos los eventos (no hay campo público en el modelo actual).
    """
    queryset = EventoCalendario.objects.all()
    serializer_class = EventoCalendarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['color']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha', 'fecha_creacion']
    ordering = ['fecha']