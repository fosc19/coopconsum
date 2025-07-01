from rest_framework import serializers
from productos.models import Producto, Proveedor, Categoria
from eventos.models import EventoCalendario


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer per categories de productes en català"""
    nom = serializers.CharField(source='nombre')
    descripcio = serializers.CharField(source='descripcion')
    
    class Meta:
        model = Categoria
        fields = ['id', 'nom', 'descripcio']


class ProveedorSerializer(serializers.ModelSerializer):
    """Serializer per proveïdors públics en català"""
    nom = serializers.CharField(source='nombre')
    descripcio_curta = serializers.CharField(source='descripcion_corta')
    contacte = serializers.CharField(source='contacto')
    direccio = serializers.CharField(source='direccion')
    imatge = serializers.ImageField(source='imagen')
    
    class Meta:
        model = Proveedor
        fields = [
            'id',
            'nom',
            'descripcio_curta',
            'contacte',
            'email',
            'direccio',
            'imatge'
        ]


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer per productes públics en català (sense preus per seguretat)"""
    nom = serializers.CharField(source='nombre')
    descripcio = serializers.CharField(source='descripcion')
    proveidor = ProveedorSerializer(source='proveedor', read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    imatge = serializers.ImageField(source='imagen')
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nom',
            'descripcio',
            'categoria',
            'proveidor',
            'imatge'
        ]


class EventoCalendarioSerializer(serializers.ModelSerializer):
    """Serializer per esdeveniments del calendari en català"""
    titol = serializers.CharField(source='titulo')
    descripcio = serializers.CharField(source='descripcion')
    data = serializers.DateField(source='fecha')
    
    class Meta:
        model = EventoCalendario
        fields = [
            'id',
            'titol',
            'descripcio',
            'data'
        ]