# stock/forms.py
from django import forms
from django.forms import modelformset_factory, inlineformset_factory
# Importar solo los modelos necesarios que existen
from productos.models import Producto
from socios.models import Socio

class SeleccionarSocioForm(forms.Form):
    """Formulario simple para seleccionar un socio."""
    socio = forms.ModelChoiceField(
        queryset=Socio.objects.order_by('apellido', 'nombre'),
        label="Seleccionar Socio",
        widget=forms.Select(attrs={'class': 'form-control select2'}) # Usar select2 para búsqueda si está instalado
    )

# (Formularios ItemRetiradoForm y ItemRetiradoFormSet eliminados por ser obsoletos)


# Podríamos necesitar un formulario para la validación más adelante,
# por ejemplo, para añadir notas o confirmar la acción.
# Mantenemos este por si acaso, aunque podría ser obsoleto también.
class ValidacionSesionForm(forms.Form):
     confirmacion = forms.BooleanField(label="Confirmar Validación", required=True)
     notas = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Notas Adicionales")
# --- Formularios para Registro de Entregas Semanales (Master) ---

from .models import RecogidaSemanal, EntregaSocio, ItemEntrega, StockLocal

class RecogidaForm(forms.ModelForm):
    """Formulario para seleccionar o crear la fecha de recogida."""
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de la Recogida Semanal"
    )

    class Meta:
        model = RecogidaSemanal
        fields = ['fecha']

class EntregaSocioForm(forms.ModelForm):
    """Formulario para seleccionar el socio para la entrega."""
    socio = forms.ModelChoiceField(
        queryset=Socio.objects.order_by('apellido', 'nombre'),
        label="Socio que realiza la recogida",
        widget=forms.Select(attrs={'class': 'form-control select2'}) # Asumiendo select2
    )

    class Meta:
        model = EntregaSocio
        fields = ['socio']

class ItemEntregaForm(forms.ModelForm):
    """Formulario para un ítem específico de la entrega."""
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(es_stock=True).order_by('categoria__nombre', 'nombre'),
        widget=forms.Select(attrs={'class': 'form-control producto-select'}) # Clase para posible JS
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control cantidad-input'}) # Clase para posible JS
    )

    class Meta:
        model = ItemEntrega
        fields = ['producto', 'cantidad']

    def clean_cantidad(self):
        """Validación básica de cantidad positiva."""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser un número positivo.")
        return cantidad

    # Podríamos añadir validación de stock aquí, pero es mejor hacerla
    # en la vista al procesar el formset completo, ya que necesitamos
    # el producto y la cantidad total solicitada para ese producto en la entrega.

# FormSet para manejar múltiples ítems de entrega asociados a una EntregaSocio
ItemEntregaFormSet = inlineformset_factory(
    EntregaSocio,       # Modelo padre
    ItemEntrega,        # Modelo hijo
    form=ItemEntregaForm, # Formulario para cada ítem
    fields=['producto', 'cantidad'], # Campos a incluir
    extra=1,            # Mostrar 1 formulario vacío por defecto
    can_delete=True,    # Permitir eliminar ítems
    min_num=1,          # Requerir al menos un ítem
    validate_min=True,
)