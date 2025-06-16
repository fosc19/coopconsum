from django import forms
from django.forms.widgets import Select
from django.utils.html import format_html # Importar format_html

from .models import EventoCalendario

# Widget personalizado para mostrar una muestra de color en el desplegable
class ColorSelectWidget(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        # Llama al método original para obtener la opción base
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        # Si el valor es un código hexadecimal de color válido, añade un estilo de fondo
        if isinstance(value, str) and value.startswith('#') and len(value) in (4, 7):
            # Añade un cuadrado de color más grande y visual usando un span con estilo
            # La etiqueta original ya está escapada por el método super().create_option
            # Usamos format_html para combinar el span con la etiqueta escapada
            option['label'] = format_html(
                '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; margin-right: 8px; vertical-align: middle; border: 1px solid #ccc; border-radius: 3px;"></span>{}',
                value,
                label # La etiqueta ya viene escapada
            )
            # También podríamos añadir un atributo data-color para usar con JS si fuera necesario
            # option['attrs']['data-color'] = value

        return option


class EventoCalendarioForm(forms.ModelForm):
    COLOR_CHOICES = [
        # Colors principals
        ('#007bff', 'Blau principal'),
        ('#28a745', 'Verd'),
        ('#ffc107', 'Groc'),
        ('#dc3545', 'Vermell'),
        ('#fd7e14', 'Taronja'),
        ('#6f42c1', 'Morat'),
        ('#e83e8c', 'Rosa'),
        ('#20c997', 'Verd menta'),
        ('#17a2b8', 'Cian'),
        # Colors neutres
        ('#6c757d', 'Gris'),
        ('#343a40', 'Gris fosc'),
        ('#495057', 'Gris mitjà'),
        # Colors adicionals
        ('#8B4513', 'Marró'),
        ('#2F4F4F', 'Gris pissarra'),
        ('#800080', 'Morat fosc'),
        ('#FF6347', 'Vermell tomàquet'),
        ('#32CD32', 'Verd lima'),
        ('#FFD700', 'Or'),
    ]
    # Usar el widget personalizado para el campo color
    color = forms.ChoiceField(choices=COLOR_CHOICES, label="Color", widget=ColorSelectWidget)

    class Meta:
        model = EventoCalendario
        fields = '__all__'
        # No necesitamos widgets específicos para los otros campos si los por defecto son suficientes