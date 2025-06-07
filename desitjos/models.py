from django.db import models
from django.conf import settings
from productos.models import Producto, Proveedor # Importar Producto y Proveedor
from socios.models import Socio # Importar Socio
from decimal import Decimal # Importar Decimal

# Modelos para la Funcionalidad de "Desitjos"
class CartaDeseo(models.Model):
    ESTADO_CARTA_CHOICES = [
        ('borrador', 'Esborrany'),
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('minimo_alcanzado', 'Mínim Aconseguit'),
        ('completada', 'Completada'),
        ('archivada', 'Arxivada'),
    ]
    TIPO_MINIMO_CHOICES = [
        ('unidades_producto', 'Unidades totales de un producto específico'),
        ('socios_producto', 'Número de socios interesados en un producto específico'),
        ('importe_total', 'Importe total acumulado para la carta'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Títol de la Carta de Desig")
    descripcion = models.TextField(blank=True, verbose_name="Descripció")
    productos = models.ManyToManyField(
        Producto,
        related_name='cartas_deseo_productos', # Cambiado related_name para evitar conflicto
        verbose_name="Productes inclosos en aquesta carta"
    )
    proveedor_sugerido = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Proveïdor Suggerit (opcional)"
    )
    imagen_representativa = models.ImageField(
        upload_to='desitjos_cartas/',
        null=True,
        blank=True,
        verbose_name="Imatge Representativa (opcional)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Data Creació")
    fecha_limite_interes = models.DateField(null=True, blank=True, verbose_name="Data Límit per Expressar Interès")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CARTA_CHOICES,
        default='borrador',
        verbose_name="Estat de la Carta"
    )
    tipo_minimo = models.CharField(
        max_length=30,
        choices=TIPO_MINIMO_CHOICES,
        null=True, blank=True,
        verbose_name="Tipus de Mínim Requerit"
    )
    producto_objetivo_minimo = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cartas_objetivo_minimo_productos', # Cambiado related_name
        verbose_name="Producte Objectiu (si el mínim és per producte)"
    )
    valor_minimo_requerido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name="Valor del Mínim Requerit"
    )
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cartas_deseo_creadas_usuario', # Cambiado related_name
        verbose_name="Creada Per"
    )

    class Meta:
        verbose_name = "Carta de Desig"
        verbose_name_plural = "Cartes de Desitjos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def actualizar_estado_minimo(self):
        if not self.tipo_minimo or self.valor_minimo_requerido is None:
            return

        intereses_en_carta = InteresSocioEnCarta.objects.filter(carta_deseo=self)
        alcanzado = False

        if self.tipo_minimo == 'unidades_producto' and self.producto_objetivo_minimo:
            total_unidades_producto_objetivo = sum(
                (item.cantidad_deseada if isinstance(item.cantidad_deseada, Decimal) else Decimal(str(item.cantidad_deseada)))
                for item in intereses_en_carta
                if item.producto == self.producto_objetivo_minimo
            )
            if total_unidades_producto_objetivo >= self.valor_minimo_requerido:
                alcanzado = True
        elif self.tipo_minimo == 'socios_producto' and self.producto_objetivo_minimo:
            num_socios_interesados_producto_objetivo = intereses_en_carta.filter(
                producto=self.producto_objetivo_minimo, cantidad_deseada__gt=Decimal('0')
            ).values('socio').distinct().count()
            if num_socios_interesados_producto_objetivo >= self.valor_minimo_requerido:
                alcanzado = True
        elif self.tipo_minimo == 'importe_total':
            importe_total_acumulado = Decimal('0.0')
            for item in intereses_en_carta:
                if item.producto.precio is not None:
                    cantidad = Decimal(str(item.cantidad_deseada)) if not isinstance(item.cantidad_deseada, Decimal) else item.cantidad_deseada
                    precio = Decimal(str(item.producto.precio)) if not isinstance(item.producto.precio, Decimal) else item.producto.precio
                    importe_total_acumulado += cantidad * precio
            if importe_total_acumulado >= self.valor_minimo_requerido:
                alcanzado = True
        
        estado_ha_cambiado = False
        if alcanzado:
            if self.estado == 'activa':
                self.estado = 'minimo_alcanzado'
                estado_ha_cambiado = True
        else: # No alcanzado
            if self.estado == 'minimo_alcanzado':
                self.estado = 'activa'
                estado_ha_cambiado = True
        
        if estado_ha_cambiado:
            self.save(update_fields=['estado'])

class InteresSocioEnCarta(models.Model):
    carta_deseo = models.ForeignKey(
        CartaDeseo,
        on_delete=models.CASCADE,
        related_name='intereses_socios',
        verbose_name="Carta de Desig Associada"
    )
    socio = models.ForeignKey(
        Socio,
        on_delete=models.CASCADE,
        related_name='intereses_en_cartas_socio', # Cambiado related_name
        verbose_name="Socio"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        verbose_name="Producte Desitjat"
    )
    cantidad_deseada = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Quantitat Desitjada"
    )
    fecha_registro_interes = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registre de l'Interès")
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name="Darrera Modificació")

    class Meta:
        verbose_name = "Interès de Soci en Carta"
        verbose_name_plural = "Interessos de Socis en Cartes"
        unique_together = ('carta_deseo', 'socio', 'producto')
        ordering = ['carta_deseo', 'socio', '-fecha_registro_interes']

    def __str__(self):
        return f"Interès de {self.socio} en {self.producto.nombre} ({self.cantidad_deseada}) per a la carta '{self.carta_deseo.titulo}'"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.carta_deseo.actualizar_estado_minimo()
