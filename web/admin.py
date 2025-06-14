from django.contrib import admin
from .models import ConfiguracioWeb, GaleriaCategoria, GaleriaImagen

@admin.register(ConfiguracioWeb)
class ConfiguracioWebAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Imatges de la Web', {
            'fields': ('imatge_principal_home',),
            'description': 'Gestiona les imatges principals que apareixen a la web pública'
        }),
    )
    
    def has_add_permission(self, request):
        return not ConfiguracioWeb.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(GaleriaCategoria)
class GaleriaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(GaleriaImagen)
class GaleriaImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha_subida')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')