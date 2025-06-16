from django.contrib import admin
from django.utils.html import format_html # Importar format_html
from .models import EventoCalendario
from .forms import EventoCalendarioForm # Importar el formulario

@admin.register(EventoCalendario)
class EventoCalendarioAdmin(admin.ModelAdmin):
    form = EventoCalendarioForm # Usar el formulario personalizado
    list_display = ('titulo', 'fecha', 'creado_por', 'compartir_api', 'fecha_creacion', 'color_display') # Añadir compartir_api
    list_filter = ('fecha', 'creado_por', 'compartir_api')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

    def color_display(self, obj):
        # Método para mostrar el color como un pequeño cuadrado en la lista del admin
        return format_html('<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></span>', obj.color)
    color_display.short_description = 'Color'
    
    class Media:
        css = {
            'all': ('admin/css/color_select_widget.css',)
        }
        js = ('admin/js/color_select_widget.js',)