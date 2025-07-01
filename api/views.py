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
    from web.models import ConfiguracioWeb
    
    # Obtenir nom dinàmic de la cooperativa
    try:
        config = ConfiguracioWeb.objects.first()
        nom_cooperativa = config.nom_cooperativa if config else "CoopConsum"
    except:
        nom_cooperativa = "CoopConsum"
    
    return Response({
        'nom': f'API {nom_cooperativa}',
        'versio': '1.0',
        'descripcio': 'API pública per compartir informació entre cooperatives de consum',
        'documentacio': {
            'completa': '/docs/API_COOPERATIVAS.md',
            'exemples': '/docs/README_API.md'
        },
        'endpoints': {
            'proveidors': '/api/proveidors/',
            'productes': '/api/productes/',
            'categories': '/api/categories/',
            'esdeveniments': '/api/esdeveniments/',
        },
        'funcionalitats': [
            'Cerca per text en noms i descripcions',
            'Ordenació per diferents criteris',
            'Paginació automàtica (20 elements per pàgina)',
            'Format JSON estàndard',
            'CORS habilitat per cooperatives'
        ]
    })


class ProveedorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet per proveïdors públics.
    Mostra tots els proveïdors visibles en web.
    """
    serializer_class = ProveedorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion_corta']
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        # Només proveïdors visibles en web
        return Proveedor.objects.filter(visible_en_web=True)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet per categories de productes.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']
    ordering = ['nombre']


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet per productes públics.
    Només mostra productes de proveïdors visibles en web.
    """
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'proveedor']
    search_fields = ['nombre', 'descripcion', 'proveedor__nombre', 'proveedor__descripcion_corta']
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        # Només productes de proveïdors visibles en web
        return Producto.objects.filter(proveedor__visible_en_web=True)


class EventoCalendarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet per esdeveniments del calendari.
    Mostra esdeveniments marcats per compartir a l'API.
    """
    serializer_class = EventoCalendarioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha']
    ordering = ['fecha']
    
    def get_queryset(self):
        # Esdeveniments marcats per compartir a l'API
        # Compatible amb BDs que no tenen el camp compartir_api encara
        try:
            return EventoCalendario.objects.filter(compartir_api=True)
        except Exception:
            # Si el camp no existeix, retornar tots els esdeveniments
            return EventoCalendario.objects.all()