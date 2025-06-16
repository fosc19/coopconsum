from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto # Importar Producto
from django.utils import timezone # Para la fecha

class Socio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='socio', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    # Nuevo campo para indicar si el socio gestiona el stock
    gestiona_stock = models.BooleanField(
        default=False,
        help_text="Marcar si aquest soci és el responsable de gestionar l'estoc."
    )
    gestiona_productos = models.BooleanField(
        default=False,
        help_text="Marcar si aquest soci pot gestionar productes (afegir, editar, etc.)."
    )
    puede_crear_comandas_esporadicas = models.BooleanField(
        default=False,
        help_text="Marcar si aquest soci pot crear comandes recurrents de tipus esporàdic."
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socis"


class CuentaSocio(models.Model):
    socio = models.OneToOneField(Socio, on_delete=models.CASCADE)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cuenta de {self.socio}"

    class Meta:
        verbose_name = "Cuenta de Socio"
        verbose_name_plural = "Comptes de socis"

class MovimientoCuenta(models.Model):
    cuenta = models.ForeignKey(CuentaSocio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=50)  # Ej: ingreso, egreso, abono
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=False, help_text="Poseu el vostre numero de uf")
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('validado', 'Validado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    
    def clean(self):
        """Validaciones personalizadas del modelo."""
        from django.core.exceptions import ValidationError
        from decimal import Decimal
        
        errors = {}
        
        # Validar monto
        if self.monto is not None:
            if self.monto <= 0:
                errors['monto'] = "L'import ha de ser major que 0."
            elif self.monto > Decimal('9999.99'):
                errors['monto'] = "L'import no pot ser superior a 9999.99€."
        
        # Validar descripción
        if self.descripcion:
            descripcion_clean = self.descripcion.strip()
            if len(descripcion_clean) < 3:
                errors['descripcion'] = "La descripció ha de tenir almenys 3 caràcters."
            elif len(descripcion_clean) > 500:
                errors['descripcion'] = "La descripció no pot tenir més de 500 caràcters."
        
        # Validar tipo de movimiento
        if self.tipo_movimiento:
            tipos_validos = ['ingreso', 'egreso', 'abono', 'test_ingreso', 'test_debug', 'test_debug_servidor', 'test_manual', 'test_permisos']
            if self.tipo_movimiento not in tipos_validos:
                errors['tipo_movimiento'] = f"Tipus de moviment no vàlid. Tipus permesos: {', '.join(tipos_validos)}"
        
        # Validar estado
        if self.estado:
            estados_validos = [choice[0] for choice in self.ESTADO_CHOICES]
            if self.estado not in estados_validos:
                errors['estado'] = f"Estat no vàlid. Estats permesos: {', '.join(estados_validos)}"
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """Override del método save para ejecutar validaciones."""
        self.full_clean()  # Ejecuta clean() y otras validaciones
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.fecha}"

    class Meta:
        verbose_name = "Movimiento de Cuenta"
        verbose_name_plural = "Moviments de comptes"
        ordering = ['-fecha']  # Ordenar por fecha descendente por defecto

class RegistroCompraSocio(models.Model):
    """Modelo para registrar manualmente una compra de producto por un socio."""
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='compras_registradas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='ventas_registradas') # PROTECT para no borrar si hay registros
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, help_text="Cantidad comprada (en unidades o kg/g según el producto)")
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_compra_realizados', help_text="Usuario que realizó el registro")
    notas = models.TextField(blank=True, help_text="Notas adicionales sobre la compra")
    # Campos para el proceso de validación y cobro
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('validado', 'Validado'),
        ('error', 'Error'), # Opcional: para marcar si hubo error al validar/cobrar
    ]
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente',
        db_index=True # Indexar para búsquedas rápidas por estado
    )
    costo_total_calculado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, # Puede ser nulo hasta que se valide
        blank=True,
        help_text="Costo total calculado en el momento de la validación (cantidad * precio producto)"
    )
    movimiento_cuenta = models.OneToOneField(
        MovimientoCuenta,
        on_delete=models.SET_NULL, # Si se borra el movimiento, no borrar el registro
        null=True,
        blank=True,
        related_name='registro_compra_asociado',
        help_text="Movimiento en la cuenta del socio generado al validar"
    )


    def __str__(self):
        estado_str = f" ({self.get_estado_display()})" if self.estado != 'pendiente' else ""
        return f"Compra de {self.cantidad} {self.producto.get_unidad_venta_display()} de {self.producto.nombre} por {self.socio} el {self.fecha_registro.strftime('%Y-%m-%d %H:%M')}{estado_str}"

    class Meta:
        ordering = ['estado', '-fecha_registro'] # Ordenar por estado (pendientes primero) y luego fecha
        verbose_name = "Registro de Compra de Socio"
        verbose_name_plural = "Registres de Compres de Socis"
