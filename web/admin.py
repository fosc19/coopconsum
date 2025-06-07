from django.contrib import admin
from .models import GaleriaCategoria, GaleriaImagen

@admin.register(GaleriaCategoria)
class GaleriaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(GaleriaImagen)
class GaleriaImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha_subida')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')