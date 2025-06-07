# socios/forms.py
from django import forms
from decimal import Decimal
from .models import RegistroCompraSocio, Socio, MovimientoCuenta
from productos.models import Producto

class RegistroCompraSocioForm(forms.ModelForm):
    # Opcional: Filtrar productos si solo quieres mostrar los de stock o activos
    # producto = forms.ModelChoiceField(
    #     queryset=Producto.objects.filter(es_stock=True).order_by('nombre'), # Ejemplo: solo productos de stock
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )

    class Meta:
        model = RegistroCompraSocio
        fields = ['socio', 'producto', 'cantidad', 'notas'] # Campos a mostrar en el formulario
        widgets = {
            'socio': forms.Select(attrs={'class': 'form-select'}), # Usar clases Bootstrap
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), # Permitir decimales
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'socio': 'Soci/a',
            'producto': 'Producte Comprat',
            'cantidad': 'Quantitat',
            'notas': 'Notes Addicionals',
        }
        help_texts = {
            'cantidad': "Indica la quantitat en la unitat de venda del producte (ud, kg, g).",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Ordenar socios por nombre en el desplegable
        self.fields['socio'].queryset = Socio.objects.order_by('nombre', 'apellido')
        # Opcional: Ordenar productos por nombre
        self.fields['producto'].queryset = Producto.objects.filter(es_stock=True).order_by('nombre')


class IngresoForm(forms.Form):
    """Formulario para envío de ingresos por parte de los socios."""
    
    monto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('9999.99'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'max': '9999.99',
            'placeholder': '0.00'
        }),
        label='Import (€)',
        help_text='Import entre 0.01€ i 9999.99€'
    )
    
    comentario = forms.CharField(
        min_length=3,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Poseu el vostre numero de uf i qualsevol comentari addicional...'
        }),
        label='Comentari',
        help_text='Mínim 3 caràcters. Poseu el vostre numero de uf.'
    )
    
    justificante = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'accept': '.pdf,.jpg,.jpeg,.png,.gif'
        }),
        label='Justificant (opcional)',
        help_text='Formats acceptats: PDF, JPG, PNG, GIF. Màxim 5MB.'
    )
    
    def clean_monto(self):
        """Validación personalizada para el monto."""
        monto = self.cleaned_data.get('monto')
        
        if monto is None:
            raise forms.ValidationError("L'import és obligatori.")
        
        if monto <= 0:
            raise forms.ValidationError("L'import ha de ser major que 0.")
        
        if monto > Decimal('9999.99'):
            raise forms.ValidationError("L'import no pot ser superior a 9999.99€.")
        
        return monto
    
    def clean_comentario(self):
        """Validación personalizada para el comentario."""
        comentario = self.cleaned_data.get('comentario', '').strip()
        
        if not comentario:
            raise forms.ValidationError("El comentari és obligatori.")
        
        if len(comentario) < 3:
            raise forms.ValidationError("El comentari ha de tenir almenys 3 caràcters.")
        
        if len(comentario) > 500:
            raise forms.ValidationError("El comentari no pot tenir més de 500 caràcters.")
        
        return comentario
    
    def clean_justificante(self):
        """Validación personalizada para el archivo justificante."""
        justificante = self.cleaned_data.get('justificante')
        
        if justificante:
            # Verificar tamaño del archivo (máximo 5MB)
            if justificante.size > 5 * 1024 * 1024:  # 5MB en bytes
                raise forms.ValidationError("L'arxiu no pot ser superior a 5MB.")
            
            # Verificar extensión del archivo
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']
            file_extension = justificante.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError("Format d'arxiu no permès. Formats acceptats: PDF, JPG, PNG, GIF.")
        
        return justificante