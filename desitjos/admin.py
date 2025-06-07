from django.contrib import admin
from .models import CartaDeseo, InteresSocioEnCarta

@admin.register(CartaDeseo)
class CartaDeseoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'fecha_creacion', 'fecha_limite_interes', 'tipo_minimo', 'valor_minimo_requerido', 'creada_por')
    list_filter = ('estado', 'tipo_minimo', 'fecha_creacion', 'fecha_limite_interes', 'proveedor_sugerido')
    search_fields = ('titulo', 'descripcion', 'productos__nombre', 'proveedor_sugerido__nombre')
    filter_horizontal = ('productos',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'estado', 'creada_por')
        }),
        ('Productes i Proveïdor', {
            'fields': ('productos', 'proveedor_sugerido', 'imagen_representativa')
        }),
        ('Dates Importants', {
            'fields': ('fecha_limite_interes',)
        }),
        ('Objectiu Mínim (Opcional)', {
            'fields': ('tipo_minimo', 'producto_objetivo_minimo', 'valor_minimo_requerido'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('fecha_creacion', 'creada_por')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creada_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(InteresSocioEnCarta)
class InteresSocioEnCartaAdmin(admin.ModelAdmin):
    list_display = ('carta_deseo', 'socio', 'producto', 'cantidad_deseada', 'fecha_registro_interes')
    list_filter = ('carta_deseo', 'socio', 'producto', 'fecha_registro_interes')
    search_fields = ('carta_deseo__titulo', 'socio__nombre', 'socio__apellido', 'producto__nombre')
    readonly_fields = ('fecha_registro_interes', 'ultima_modificacion')
    
    def has_add_permission(self, request):
        return False # Gestionado por socios desde la interfaz

    def has_change_permission(self, request, obj=None):
        return False # Gestionado por socios desde la interfaz
