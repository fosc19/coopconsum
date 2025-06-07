from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Proveedor, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    fields = ('nombre', 'descripcion')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta', 'visible_en_web', 'visible_en_inicio', 'imagen_thumb')
    list_editable = ('visible_en_web', 'visible_en_inicio')
    search_fields = ('nombre', 'descripcion_corta')
    fields = ('nombre', 'descripcion_corta', 'imagen', 'contacto', 'email', 'direccion', 'visible_en_web', 'visible_en_inicio')
    
    def imagen_thumb(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width:50px;height:auto;">', obj.imagen.url)
        return ''
    imagen_thumb.short_description = 'Imagen'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Añadir 'unidad_venta' y 'destacado_en_inicio' a la lista y filtros
    list_display = ('nombre', 'precio', 'unidad_venta', 'stock', 'es_stock', 'destacado_en_inicio', 'categoria', 'proveedor', 'imagen_thumb')
    list_filter = ('unidad_venta', 'es_stock', 'destacado_en_inicio', 'categoria', 'proveedor')
    list_editable = ('destacado_en_inicio',)
    search_fields = ('nombre',)
    # Asegurarse de que 'unidad_venta' sea editable (normalmente lo es por defecto si no se usa fields/fieldsets)

    def imagen_thumb(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width:50px;height:auto;">', obj.imagen.url)
        return ''
    imagen_thumb.short_description = 'Imagen'

