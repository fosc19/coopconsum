from django.contrib import admin
from .models import ConfiguracioWeb, GaleriaCategoria, GaleriaImagen

@admin.register(ConfiguracioWeb)
class ConfiguracioWebAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informació General', {
            'fields': ('nom_cooperativa',),
            'description': 'Dades bàsiques de la cooperativa'
        }),
        ('Secció Hero (Banner Principal)', {
            'fields': ('titol_hero', 'subtitol_hero'),
            'description': 'Text del banner principal de la pàgina d\'inici. Pots usar {nom_cooperativa} per inserir automàticament el nom'
        }),
        ('Secció "Qui som"', {
            'fields': ('titol_qui_som', 'text_qui_som', 'imatge_principal_home'),
            'description': 'Contingut de la secció "Qui som" amb imatge'
        }),
        ('Característiques/Valors', {
            'fields': (
                'titol_caracteristiques',
                ('titol_caracteristica_1', 'icona_caracteristica_1'),
                'text_caracteristica_1',
                ('titol_caracteristica_2', 'icona_caracteristica_2'),
                'text_caracteristica_2',
                ('titol_caracteristica_3', 'icona_caracteristica_3'),
                'text_caracteristica_3',
            ),
            'description': 'Les tres característiques principals que destaquen els valors de la cooperativa. Per icones usa classes Font Awesome (ex: fas fa-leaf)'
        }),
        ('Call to Action Final', {
            'fields': ('titol_cta', 'text_cta', 'text_boto_cta'),
            'description': 'Secció final per captar nous socis. Pots usar {nom_cooperativa} en els textos'
        }),
    )
    
    def has_add_permission(self, request):
        return not ConfiguracioWeb.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }

@admin.register(GaleriaCategoria)
class GaleriaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(GaleriaImagen)
class GaleriaImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha_subida')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')