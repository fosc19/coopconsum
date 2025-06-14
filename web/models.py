from django.db import models
from django.core.exceptions import ValidationError

class ConfiguracioWeb(models.Model):
    imatge_principal_home = models.ImageField(
        upload_to='configuracio/',
        blank=True, 
        null=True,
        help_text="Imatge principal que apareix a la pàgina d'inici (secció 'Qui som?')"
    )
    
    class Meta:
        verbose_name = "Configuració Web"
        verbose_name_plural = "Configuració Web"
    
    def __str__(self):
        return "Configuració de la Web"
    
    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracioWeb.objects.exists():
            raise ValidationError('Només pot existir una configuració web')
        super().save(*args, **kwargs)

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