from django.db import models

class GaleriaCategoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría de galería"
        verbose_name_plural = "Categories de galeria"
        ordering = ['-fecha_creacion', 'nombre']

    def __str__(self):
        return self.nombre

class GaleriaImagen(models.Model):
    categoria = models.ForeignKey(GaleriaCategoria, on_delete=models.CASCADE, related_name='imagenes')
    titulo = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='galeria/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Imatges de galeria"
        ordering = ['-fecha_subida', 'titulo']

    def __str__(self):
        return self.titulo or f"Imagen {self.id}"