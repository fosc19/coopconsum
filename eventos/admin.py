from django.contrib import admin
from django.utils.html import format_html # Importar format_html
from .models import EventoCalendario
from .forms import EventoCalendarioForm # Importar el formulario

@admin.register(EventoCalendario)
class EventoCalendarioAdmin(admin.ModelAdmin):
    form = EventoCalendarioForm # Usar el formulario personalizado
    list_display = ('titulo', 'fecha', 'creado_por', 'fecha_creacion', 'color_display') # Añadir color_display
    list_filter = ('fecha', 'creado_por')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

    def color_display(self, obj):
        # Método para mostrar el color como un pequeño cuadrado en la lista del admin
        return format_html('<span style="display: inline-block; width: 20px; height: 20px; background-color: {};"></span>', obj.color)
    color_display.short_description = 'Color'