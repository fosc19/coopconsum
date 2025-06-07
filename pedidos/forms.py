# pedidos/forms.py

from django import forms
from .models import DetalleSeleccion, ComandaRecurrente, Categoria, Proveedor
from django.utils import timezone
from datetime import timedelta

class DetalleSeleccionModelForm(forms.ModelForm):
    class Meta:
        model = DetalleSeleccion
        fields = ['producto', 'cantidad']

class ComandaEsporadicaSocioForm(forms.ModelForm):
    # Para asegurar que solo se puedan seleccionar categorías y proveedores activos/visibles si es necesario
    # Esto dependerá de la lógica de negocio de Categoria y Proveedor
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(), # Idealmente filtrar por activas/visibles
        required=False,
        label="Categoria (Opcional)" # Traducido "Categoría"
    )
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(), # Idealmente filtrar por activos/visibles
        required=False,
        label="Proveïdor (Opcional)" # Traducido "Proveedor"
    )

    class Meta:
        model = ComandaRecurrente
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'categoria', 'proveedor']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}), # Eliminado el atributo 'min'
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'nombre': 'Un nom descriptiu per a la teva comanda esporàdica.', # Traducido
            'fecha_inicio': 'Dia en què aquesta comanda esporàdica s\'activarà i es crearà la comanda col·lectiva.', # Traducido
            'fecha_fin': 'Dia en què aquesta comanda esporàdica deixarà d\'estar activa. d\'inici.', # Traducido
            'categoria': 'Si la comanda és per a una categoria específica de productes.', # Traducido
            'proveedor': 'Si la comanda és per a un proveïdor específic.', # Traducido
        }
        labels = {
            'nombre': 'Nom de la Comanda', # Traducido
            'fecha_inicio': 'Data d\'Inici de la Comanda', # Traducido
            'fecha_fin': 'Data de Fi de la Comanda', # Traducido
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha_inicio por defecto a hoy y fecha_fin a 7 días desde hoy
        # El usuario podrá modificarlas.
        if not self.instance.pk: # Solo para formularios nuevos
            today = timezone.now().date()
            self.initial['fecha_inicio'] = today
            self.initial['fecha_fin'] = today + timedelta(days=7) # Por defecto, una semana de duración para la comanda

        # Validar que fecha_fin no sea anterior a fecha_inicio
        # Eliminamos la actualización dinámica del atributo 'min' aquí también
        # if 'fecha_inicio' in self.fields and 'fecha_fin' in self.fields:
        #     self.fields['fecha_fin'].widget.attrs['min'] = self.initial.get('fecha_inicio', timezone.now().date()).strftime('%Y-%m-%d')


    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
            # Una comanda esporádica debería durar al menos lo que dura un pedido (ej. 7 días)
            # O la fecha de fin de la comanda debe ser al menos la fecha de fin del pedido que se creará.
            # Si el pedido se crea en fecha_inicio y dura 7 días, la comanda debe estar activa al menos hasta fecha_inicio.
            # La fecha_fin de la ComandaRecurrente es para la vigencia de la propia comanda recurrente.
            # El PedidoColectivo generado tendrá su propia fecha_apertura, fecha_cierre, etc.
            # Por ahora, solo validamos que fin >= inicio.
        elif not fecha_fin: # Fecha fin es obligatoria para esporádicas
             raise forms.ValidationError("La fecha de fin es obligatoria para comandas esporádicas.")
        return fecha_fin

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio and fecha_inicio < timezone.now().date():
            raise forms.ValidationError("La fecha de inicio no puede ser en el pasado.")
        if not fecha_inicio:
            raise forms.ValidationError("La fecha de inicio es obligatoria.")
        return fecha_inicio
