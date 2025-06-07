from rest_framework import serializers
from productos.models import Producto, Proveedor, Categoria
from eventos.models import EventoCalendario


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para categorías de productos"""
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class ProveedorSerializer(serializers.ModelSerializer):
    """Serializer para proveedores públicos"""
    
    class Meta:
        model = Proveedor
        fields = [
            'id',
            'nombre',
            'descripcion_corta',
            'contacto',
            'email',
            'direccion',
            'imagen',
            'visible_en_web',
            'visible_en_inicio'
        ]


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para productos públicos"""
    proveedor = ProveedorSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    unidad_venta_display = serializers.CharField(source='get_unidad_venta_display', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion', 
            'precio',
            'unidad_venta',
            'unidad_venta_display',
            'categoria',
            'proveedor',
            'imagen',
            'es_stock',
            'destacado_en_inicio'
        ]


class EventoCalendarioSerializer(serializers.ModelSerializer):
    """Serializer para eventos del calendario"""
    
    class Meta:
        model = EventoCalendario
        fields = [
            'id',
            'titulo',
            'descripcion',
            'fecha',
            'color',
            'fecha_creacion'
        ]