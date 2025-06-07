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
            # Añade un pequeño cuadrado de color usando un span con estilo
            # La etiqueta original ya está escapada por el método super().create_option
            # Usamos format_html para combinar el span con la etiqueta escapada
            option['label'] = format_html(
                '<span style="display: inline-block; width: 12px; height: 12px; background-color: {}; margin-right: 5px; vertical-align: middle;"></span>{}',
                value,
                label # La etiqueta ya viene escapada
            )
            # También podríamos añadir un atributo data-color para usar con JS si fuera necesario
            # option['attrs']['data-color'] = value

        return option


class EventoCalendarioForm(forms.ModelForm):
    COLOR_CHOICES = [
        ('#007bff', 'Azul'),
        ('#28a745', 'Verde'),
        ('#ffc107', 'Amarillo'),
        ('#dc3545', 'Rojo'),
        ('#6c757d', 'Gris'),
        # Puedes añadir más colores aquí
    ]
    # Usar el widget personalizado para el campo color
    color = forms.ChoiceField(choices=COLOR_CHOICES, label="Color", widget=ColorSelectWidget)

    class Meta:
        model = EventoCalendario
        fields = '__all__'
        # No necesitamos widgets específicos para los otros campos si los por defecto son suficientes