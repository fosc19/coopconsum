from django.contrib import admin
from .models import (
    PedidoColectivo, SeleccionSocio, DetalleSeleccion, ComandaRecurrente,
    PropuestaCorreccionComanda # Quitar modelos de Desitjos
)

@admin.register(PedidoColectivo)
class PedidoColectivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado', 'fecha_apertura', 'fecha_inicio_pedidos', 'fecha_cierre','fecha_entrega','comanda')
    list_filter = ('estado', 'tipo', 'fecha_apertura', 'fecha_inicio_pedidos', 'fecha_cierre')
    fieldsets = (
        (None, {
            'fields': ('tipo', 'estado', 'comanda', 'socio')
        }),
        ('Fechas Importantes', {
            'fields': ('fecha_apertura', 'fecha_inicio_pedidos', 'fecha_cierre', 'fecha_entrega')
        }),
        ('Filtros de Productos (Opcional)', {
            'fields': ('categoria', 'proveedor'),
            'classes': ('collapse',), # Para que aparezca colapsado por defecto
        }),
    )
    # Si quieres que fecha_creacion (si existiera y fuera auto_now_add) no sea editable:
    # readonly_fields = ('fecha_creacion',)

@admin.register(ComandaRecurrente)
class ComandaRecurrenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_inicio', 'frecuencia', 'dia_semana', 'socio_asignado', 'fecha_fin')
    exclude = ('ultima_generacion', 'dia_mes') # dia_mes parece no usarse, se podría quitar del modelo si no es necesario

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.frecuencia != 'esporadico':
            # Hacemos una tupla para asegurar inmutabilidad si es necesario, y añadimos fecha_fin
            return tuple(readonly_fields) + ('fecha_fin',)
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.frecuencia != 'esporadico':
            if 'fecha_fin' in form.base_fields:
                form.base_fields['fecha_fin'].help_text = "La fecha de fin solo es aplicable a comandas con frecuencia 'esporádico'."
        elif not obj: # Si es un objeto nuevo, podríamos querer un texto de ayuda general
             if 'fecha_fin' in form.base_fields:
                form.base_fields['fecha_fin'].help_text = (
                    "Dejar vacío para comandas recurrentes (semanal, quincenal, mensual) "
                    "a menos que tengan una fecha de finalización específica. "
                    "Obligatorio para frecuencia 'esporádico' si se desea que finalice."
                )
        return form

admin.site.register(SeleccionSocio)
admin.site.register(DetalleSeleccion)

@admin.register(PropuestaCorreccionComanda)
class PropuestaCorreccionComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'comanda', 'usuario', 'estado', 'fecha_propuesta', 'fecha_validacion')
    list_filter = ('estado', 'fecha_propuesta', 'fecha_validacion', 'comanda')
    search_fields = ('comanda__nombre', 'usuario__username')
    ordering = ('-fecha_propuesta',)

    actions = ['eliminar_propuestas_seleccionadas']

    def eliminar_propuestas_seleccionadas(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Se han eliminado {count} propuestas de corrección seleccionadas.")
    eliminar_propuestas_seleccionadas.short_description = "Eliminar propuestas seleccionadas"
