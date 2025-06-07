from django.db import models
from socios.models import Socio
from productos.models import Producto, Categoria, Proveedor

class PedidoColectivo(models.Model):
    TIPO_PEDIDO_CHOICES = [
        ('semanal', 'Semanal'),
        ('esporadico', 'Esporádico'),
        ('mensual', 'Mensual'),
        ('quincenal', 'Quincenal'),
    ]
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),          # Se pueden añadir productos (si fecha_inicio_pedidos ha pasado)
        ('cerrado', 'Cerrado'),          # Ya no se pueden añadir productos
        ('pendiente', 'Pendiente'),      # Cerrado, pero esperando revisión/ajustes del gestor
        ('listo_para_finalizar', 'Listo para Finalizar'), # Ajustes hechos (si los hubo), listo para descontar monederos
        ('inactivo', 'Inactivo'),        # Proceso completado (monederos descontados)
    ]
    # Para pedidos recurrentes se asignará la comanda,
    # y para pedidos esporádicos se asigna directamente un socio.
    comanda = models.ForeignKey(
        'ComandaRecurrente',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Unificamos el campo de socio para ambos casos (recurrentes y esporádicos).
    socio = models.ForeignKey(
        Socio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    fecha_inicio_pedidos = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora a partir de la cual los socios pueden empezar a añadir productos a este pedido."
    )
    tipo = models.CharField(max_length=20, choices=TIPO_PEDIDO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        categoria_str = self.categoria.nombre if self.categoria else "Sin categoría"
        proveedor_str = self.proveedor.nombre if self.proveedor else "Sin proveedor"
        socio_str = self.socio.__str__() if self.socio else "Sin responsable"
        return f"{categoria_str} - {proveedor_str} - {socio_str} - (comanda {self.get_tipo_display()})"

    def save(self, *args, **kwargs):
        # Si el tipo de pedido no es semanal y fecha_inicio_pedidos está vacío o queremos forzarlo,
        # lo igualamos a fecha_apertura.
        if self.tipo != 'semanal':
            if not self.fecha_inicio_pedidos or self.fecha_inicio_pedidos != self.fecha_apertura:
                self.fecha_inicio_pedidos = self.fecha_apertura
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Comanda Col·lectiva"
        verbose_name_plural = "Comandes colectives"

class SeleccionSocio(models.Model):
    pedido = models.ForeignKey(PedidoColectivo, on_delete=models.CASCADE)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fecha_seleccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Selección de {self.socio} en {self.pedido}"

    class Meta:
        verbose_name = "Selecció de Soci"
        verbose_name_plural = "Seleccions de Socis"

class DetalleSeleccion(models.Model):
    seleccion = models.ForeignKey(SeleccionSocio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"

    class Meta:
        verbose_name = "Detall de Selecció"
        verbose_name_plural = "Detalls selecció"

class ComandaRecurrente(models.Model):
    FRECUENCIA_CHOICES = [
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('quincenal', 'Quincenal'),
        ('esporadico', 'Esporádico'),
    ]
    DIA_SEMANA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    nombre = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES)
    dia_semana = models.CharField(max_length=20, choices=DIA_SEMANA_CHOICES, blank=True, null=True)
    dia_mes = models.PositiveIntegerField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='activa')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    # Socio encargado de gestionar la comanda
    socio_asignado = models.ForeignKey(
        Socio,
        on_delete=models.SET_NULL, # Cambiado de PROTECT a SET_NULL
        null=True, blank=True      # Añadido para hacerlo opcional
    )

    # Registro de la última generación de pedido (opcional)
    ultima_generacion = models.DateField(null=True, blank=True)

    def __str__(self):
        categoria_str = self.categoria.nombre if self.categoria else "Sin categoría"
        proveedor_str = self.proveedor.nombre if self.proveedor else "Sin proveedor"
        socio_str = self.socio_asignado.nombre if self.socio_asignado else "Sin responsable"
        return f"{categoria_str} - {proveedor_str} - {socio_str} - (comanda {self.get_frecuencia_display()})"

    class Meta:
        verbose_name = "Comanda Recurrent"
        verbose_name_plural = "Comandes recurrents"
        permissions = [
            ("puede_crear_comanda_esporadica", "Puede crear comandas recurrentes esporádicas"),
        ]

from django.conf import settings # Importar settings para User

class AnotacionStockConsumido(models.Model):
    """Modelo para registrar el stock consumido durante la recogida."""
    socio = models.ForeignKey(
        Socio,
        on_delete=models.SET_NULL, # Mantener registro si se borra el socio
        null=True,
        blank=True,
        help_text="Socio que retiró el stock."
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT, # Evitar borrar producto si hay anotaciones
        help_text="Producto de stock consumido."
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2, # Permitir decimales (ej. para kg)
        help_text="Cantidad consumida."
    )
    fecha_anotacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de la anotación."
    )
    anotado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Mantener registro si se borra el usuario admin/master
        null=True,
        blank=True,
        help_text="Usuario que realizó la anotación."
    )
    # Opcional: Campo de notas
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        socio_str = self.socio.nombre if self.socio else "Socio Desconocido"
        return f"{self.cantidad} x {self.producto.nombre} para {socio_str} el {self.fecha_anotacion.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-fecha_anotacion'] # Mostrar las más recientes primero
from django.contrib.auth import get_user_model
from django.db.models import JSONField

import json

class NotificacionRecepcionComanda(models.Model):
    pedido = models.ForeignKey(PedidoColectivo, on_delete=models.CASCADE, related_name='notificaciones_recepcion')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField(blank=True, null=True)
    cantidades_recibidas = models.TextField(help_text="JSON serializado: diccionario {producto_id: cantidad_recibida}")

    def __str__(self):
        return f"Notificación de recepción para pedido {self.pedido.id} por {self.usuario} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    def get_cantidades_dict(self):
        try:
            return json.loads(self.cantidades_recibidas)
        except Exception:
            return {}

# NUEVO MODELO: Propuesta de corrección de comanda
class PropuestaCorreccionComanda(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('validada', 'Validada'),
        ('rechazada', 'Rechazada'),
    ]
    comanda = models.ForeignKey(ComandaRecurrente, on_delete=models.CASCADE, related_name='propuestas_correccion')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    fecha_propuesta = models.DateTimeField(auto_now_add=True)
    cambios = models.TextField(help_text="JSON serializado: lista de cambios [{'socio_id': x, 'producto_id': y, 'cantidad': z}, ...]")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    usuario_validador = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='propuestas_validadas')

    def __str__(self):
        return f"Propuesta de corrección para comanda {self.comanda.id} ({self.get_estado_display()})"

    def get_cambios_list(self):
        import json
        try:
            return json.loads(self.cambios)
        except Exception:
            return []

    class Meta:
        verbose_name = "Proposta de Correcció de Comanda"
        verbose_name_plural = "Propostes de Correcció de Comandes"
