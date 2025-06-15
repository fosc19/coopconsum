from django.contrib import admin
from .models import ConfiguracioWeb, GaleriaCategoria, GaleriaImagen

@admin.register(ConfiguracioWeb)
class ConfiguracioWebAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏢 Informació General', {
            'fields': ('nom_cooperativa', 'logo_principal'),
            'description': 'Dades bàsiques de la cooperativa que s\'utilitzaran a tota la web'
        }),
        
        ('🏠 PÀGINA D\'INICI - Secció Hero (Banner Principal)', {
            'fields': ('titol_hero', 'subtitol_hero'),
            'description': 'Text del banner principal de la pàgina d\'inici. Pots usar {nom_cooperativa} per inserir automàticament el nom'
        }),
        ('🏠 PÀGINA D\'INICI - Secció "Qui som"', {
            'fields': ('titol_qui_som', 'text_qui_som', 'imatge_principal_home'),
            'description': 'Contingut de la secció "Qui som" amb imatge a la pàgina d\'inici'
        }),
        ('🏠 PÀGINA D\'INICI - Característiques/Valors', {
            'fields': (
                'titol_caracteristiques',
                ('titol_caracteristica_1', 'icona_caracteristica_1'),
                'text_caracteristica_1',
                ('titol_caracteristica_2', 'icona_caracteristica_2'),
                'text_caracteristica_2',
                ('titol_caracteristica_3', 'icona_caracteristica_3'),
                'text_caracteristica_3',
            ),
            'description': 'Les tres característiques principals que destaquen els valors de la cooperativa. Selecciona icones dels desplegables'
        }),
        ('🏠 PÀGINA D\'INICI - Call to Action Final', {
            'fields': ('titol_cta', 'text_cta', 'text_boto_cta'),
            'description': 'Secció final per captar nous socis. Pots usar {nom_cooperativa} en els textos'
        }),
        
        ('👥 PÀGINA "QUI SOM" - Contingut Principal', {
            'fields': ('pagina_qui_som_titol', 'pagina_qui_som_introducció'),
            'description': 'Títol i introducció de la pàgina "Qui som" (URL: /qui-som/)'
        }),
        ('👥 PÀGINA "QUI SOM" - Secció Cistella', {
            'fields': ('qui_som_titol_cistella', 'qui_som_text_cistella'),
            'description': 'Contingut sobre la cistella setmanal (permet HTML per enllaços)'
        }),
        ('👥 PÀGINA "QUI SOM" - Secció Altres Productes', {
            'fields': ('qui_som_titol_altres_productes', 'qui_som_text_altres_productes', 'qui_som_criteris_seleccio'),
            'description': 'Informació sobre altres productes i criteris de selecció (usar doble salt de línia per separar punts)'
        }),
        ('👥 PÀGINA "QUI SOM" - Ubicació', {
            'fields': ('qui_som_titol_ubicacio', 'qui_som_text_ubicacio'),
            'description': 'Informació sobre la ubicació del local'
        }),
        
        ('📝 PÀGINA "COM APUNTAR-SE" - Contingut Principal', {
            'fields': ('pagina_apuntarse_titol', 'pagina_apuntarse_introducció'),
            'description': 'Títol i introducció de la pàgina "Com apuntar-se" (URL: /com-apuntar-se/)'
        }),
        ('📝 PÀGINA "COM APUNTAR-SE" - Secció Compromís', {
            'fields': ('apuntarse_titol_compromis', 'apuntarse_text_compromis'),
            'description': 'Informació sobre el compromís necessari per formar part de la cooperativa'
        }),
        ('📝 PÀGINA "COM APUNTAR-SE" - Secció Comissions', {
            'fields': ('apuntarse_titol_comissions', 'apuntarse_text_comissions'),
            'description': 'Descripció de les diferents comissions (usar doble salt de línia per separar cada comissió)'
        }),
        ('📝 PÀGINA "COM APUNTAR-SE" - Formalització', {
            'fields': ('apuntarse_titol_formalitzacio', 'apuntarse_text_formalitzacio', 'apuntarse_requisits'),
            'description': 'Informació sobre com formalitzar l\'ingrés i requisits econòmics'
        }),
        
        ('📞 PÀGINA "CONTACTE" - Contingut', {
            'fields': ('pagina_contacte_titol', 'pagina_contacte_subtitol'),
            'description': 'Títol i subtítol de la pàgina de contacte (URL: /contacte/)'
        }),
        ('📞 PÀGINA "CONTACTE" - Dades de Contacte', {
            'fields': ('contacte_email', 'contacte_telefon', 'contacte_adreca'),
            'description': 'Informació de contacte que apareixerà a la pàgina'
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