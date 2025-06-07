from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    # Campo opcional para subcategorías
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategorias'
    )

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.CharField(max_length=255, blank=True, help_text="Descripción breve del proveedor para mostrar en la galería.")
    imagen = models.ImageField(upload_to='proveedores/', blank=True, null=True, help_text="Imagen del proveedor para la galería.")
    contacto = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    visible_en_web = models.BooleanField(default=True, verbose_name="Visible en la web", help_text="Si está marcado, el proveedor aparecerá en la web.")
    visible_en_inicio = models.BooleanField(default=False, verbose_name="Visible en la página de inicio", help_text="Si está marcado, el proveedor aparecerá en la página de inicio.")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveïdor"
        verbose_name_plural = "Proveïdors"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0) # Considerar si el stock es en unidades o gramos/kg
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    # Campo de imagen
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    # Nuevo campo booleano
    es_stock = models.BooleanField(default=False, help_text="Marcar si este producto se gestiona como stock.")
    # Campo para destacar productos en la página de inicio
    destacado_en_inicio = models.BooleanField(default=False, verbose_name="Destacado en inicio", help_text="Si está marcado, el producto aparecerá en la sección de productos destacados de la página de inicio.")

    UNIDAD_VENTA_CHOICES = [
        ('ud', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litre'), # Nueva opción para Litros
    ]
    unidad_venta = models.CharField(
        max_length=2, # Sigue siendo suficiente para 'l', 'ud', 'kg', 'g'
        choices=UNIDAD_VENTA_CHOICES,
        default='ud',
        help_text="Unidad en la que se vende y se expresa el precio."
    )

    def __str__(self):
        # Añadir unidad al nombre mostrado
        return f"{self.nombre} ({self.get_unidad_venta_display()})"

    class Meta:
        verbose_name = "Producte"
        verbose_name_plural = "Productes"


