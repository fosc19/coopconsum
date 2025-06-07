# productos/forms.py
from django import forms
from .models import Producto, Categoria, Proveedor

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'unidad_venta',
            'categoria',
            'proveedor',
            'imagen',
            'es_stock',
            'destacado_en_inicio',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Hacer que los campos de categoría y proveedor sean más amigables
        self.fields['categoria'].queryset = Categoria.objects.order_by('nombre')
        self.fields['proveedor'].queryset = Proveedor.objects.order_by('nombre')
        # Opcional: Añadir clases CSS para estilizar con Bootstrap u otro framework
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs['class'] = 'form-check-input' # Clase específica para checkboxes