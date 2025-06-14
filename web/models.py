from django.db import models
from django.core.exceptions import ValidationError

class ConfiguracioWeb(models.Model):
    # Informació bàsica de la cooperativa
    nom_cooperativa = models.CharField(
        max_length=100, 
        default="La Civada",
        help_text="Nom de la cooperativa que apareixerà arreu de la web"
    )
    
    # Secció Hero (banner principal)
    titol_hero = models.CharField(
        max_length=200, 
        default="Benvingut/da a {nom_cooperativa}",
        help_text="Títol principal de la pàgina d'inici. Usa {nom_cooperativa} per inserir el nom automàticament"
    )
    subtitol_hero = models.TextField(
        default="Cooperativa de consum responsable. Productes locals, ecològics i de proximitat.",
        help_text="Text descriptiu sota el títol principal"
    )
    
    # Secció "Qui som"
    titol_qui_som = models.CharField(
        max_length=100, 
        default="Qui som?",
        help_text="Títol de la secció 'Qui som'"
    )
    text_qui_som = models.TextField(
        default="Som una cooperativa sense ànim de lucre formada per persones compromeses amb el consum responsable, la sostenibilitat i el suport als productors locals. El nostre objectiu és facilitar l'accés a productes ecològics i de qualitat, fomentant l'economia social i el respecte pel medi ambient.",
        help_text="Descripció detallada de la cooperativa"
    )
    
    # Imatge principal (ja existent)
    imatge_principal_home = models.ImageField(
        upload_to='configuracio/',
        blank=True, 
        null=True,
        help_text="Imatge principal que apareix a la pàgina d'inici (secció 'Qui som?')"
    )
    
    # Secció característiques/valors
    titol_caracteristiques = models.CharField(
        max_length=200, 
        default="Per què escollir {nom_cooperativa}?",
        help_text="Títol de la secció de característiques. Usa {nom_cooperativa} per inserir el nom automàticament"
    )
    
    # Característica 1
    titol_caracteristica_1 = models.CharField(
        max_length=100, 
        default="Productes ecològics",
        help_text="Títol de la primera característica"
    )
    text_caracteristica_1 = models.TextField(
        default="Tots els nostres productes són ecològics, sense químics i amb certificació CCPAE o relació de confiança.",
        help_text="Descripció de la primera característica"
    )
    icona_caracteristica_1 = models.CharField(
        max_length=50, 
        default="fas fa-leaf",
        help_text="Classe CSS de l'icona (Font Awesome). Ex: fas fa-leaf, fas fa-heart, etc."
    )
    
    # Característica 2
    titol_caracteristica_2 = models.CharField(
        max_length=100, 
        default="Proximitat",
        help_text="Títol de la segona característica"
    )
    text_caracteristica_2 = models.TextField(
        default="Apostem per productes de proximitat per reduir el transport i apropar consumidors i productors.",
        help_text="Descripció de la segona característica"
    )
    icona_caracteristica_2 = models.CharField(
        max_length=50, 
        default="fas fa-map-marker-alt",
        help_text="Classe CSS de l'icona (Font Awesome)"
    )
    
    # Característica 3
    titol_caracteristica_3 = models.CharField(
        max_length=100, 
        default="Benefici social",
        help_text="Títol de la tercera característica"
    )
    text_caracteristica_3 = models.TextField(
        default="Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.",
        help_text="Descripció de la tercera característica"
    )
    icona_caracteristica_3 = models.CharField(
        max_length=50, 
        default="fas fa-hands-helping",
        help_text="Classe CSS de l'icona (Font Awesome)"
    )
    
    # Call to Action final
    titol_cta = models.CharField(
        max_length=200, 
        default="Vols formar part de la nostra cooperativa?",
        help_text="Títol de la secció final d'inscripció"
    )
    text_cta = models.TextField(
        default="Uneix-te a {nom_cooperativa} i gaudeix de productes ecològics, locals i de qualitat.",
        help_text="Text descriptiu del call to action. Usa {nom_cooperativa} per inserir el nom automàticament"
    )
    text_boto_cta = models.CharField(
        max_length=50, 
        default="Apunta't ara",
        help_text="Text del botó de call to action"
    )
    
    class Meta:
        verbose_name = "Configuració Web"
        verbose_name_plural = "Configuració Web"
    
    def __str__(self):
        return f"Configuració Web - {self.nom_cooperativa}"
    
    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracioWeb.objects.exists():
            raise ValidationError('Només pot existir una configuració web')
        super().save(*args, **kwargs)
    
    def get_titol_hero_formatted(self):
        """Retorna el títol hero amb el nom de la cooperativa substituït"""
        return self.titol_hero.replace('{nom_cooperativa}', self.nom_cooperativa)
    
    def get_titol_caracteristiques_formatted(self):
        """Retorna el títol de característiques amb el nom de la cooperativa substituït"""
        return self.titol_caracteristiques.replace('{nom_cooperativa}', self.nom_cooperativa)
    
    def get_text_cta_formatted(self):
        """Retorna el text CTA amb el nom de la cooperativa substituït"""
        return self.text_cta.replace('{nom_cooperativa}', self.nom_cooperativa)

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