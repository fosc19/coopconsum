from django.db import models
from productos.models import Producto
from socios.models import RegistroCompraSocio # Importar el modelo original

class StockLocal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(default=0)
    ubicacion = models.CharField(max_length=100, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_disponible}"

class MovimientoStock(models.Model):
    stock = models.ForeignKey(StockLocal, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=50)  # entrada, salida, ajuste
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} en {self.fecha}"

class RegistroCompraStockProxy(RegistroCompraSocio):
    class Meta:
        proxy = True
        verbose_name = "Registro de Compra Stock"
        verbose_name_plural = "Registres de Compres d'Estoc"
