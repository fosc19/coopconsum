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
    
    # === PÀGINA QUI SOM ===
    pagina_qui_som_titol = models.CharField(
        max_length=100,
        default="Qui som",
        help_text="Títol principal de la pàgina 'Qui som'"
    )
    pagina_qui_som_introducció = models.TextField(
        default="La Civada és una cooperativa de consum ecològic de Sant Cugat del Vallès. Ens autogestionem amb l'objectiu d'accedir a productes ecològics, de proximitat i sense intermediaris. Cada setmana, els dimecres de 19.30 a 20.30 ens trobem al nostre local per recollir una cistella de verdures i fruites, a més d'altres productes.",
        help_text="Text d'introducció que apareix destacat a la part superior"
    )
    
    # Secció cistella
    qui_som_titol_cistella = models.CharField(
        max_length=100,
        default="La cistella",
        help_text="Títol de la secció sobre la cistella"
    )
    qui_som_text_cistella = models.TextField(
        default='Cada dimecres podem recollir una cistella de fruites i verdures que ens porta <a href="https://www.laruraldecollserola.com" target="_blank">La Rural de Collserola</a>, una cooperativa de pagesos que estan a Valldoreix i fan producció agroecològica. Cada família és sòcia de La Rural i fem la comanda directament al seu web.',
        help_text="Descripció de la cistella (permet HTML per enllaços)"
    )
    
    # Secció altres productes
    qui_som_titol_altres_productes = models.CharField(
        max_length=100,
        default="Altres productes",
        help_text="Títol de la secció sobre altres productes"
    )
    qui_som_text_altres_productes = models.TextField(
        default="Setmanalment: làctics (iogurts, formatges, quallades), pa, ous, fruits secs…\n\nPeriòdicament: comandes directes a proveïdors (vedella, pollastre, xai, peix, oli, vins, productes d'higiene...)\n\nPetit estoc al local: mel, arròs, llegums, cafè, te, sucre, pots de tomàquet, cigrons, llenties, olives, sucs, cerveses…",
        help_text="Descripció dels altres productes (separar categories amb doble salt de línia)"
    )
    qui_som_criteris_seleccio = models.TextField(
        default="Productes ecològics, sense químics, amb certificació CCPAE o relació de confiança.\n\nDe proximitat, per reduir transport i apropar consumidors i productors.\n\nPriorititzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.",
        help_text="Criteris de selecció dels productes (separar criteris amb doble salt de línia)"
    )
    
    # Secció ubicació
    qui_som_titol_ubicacio = models.CharField(
        max_length=100,
        default="On som",
        help_text="Títol de la secció d'ubicació"
    )
    qui_som_text_ubicacio = models.TextField(
        default="El nostre local es troba a Cal Temerari:\nCarrer Plana de l'Hospital 26, Carrer Sant Esteve 11, Sant Cugat del Vallès",
        help_text="Adreça del local (usar salt de línia per separar)"
    )
    
    # === PÀGINA COM APUNTAR-SE ===
    pagina_apuntarse_titol = models.CharField(
        max_length=100,
        default="Com apuntar-te",
        help_text="Títol principal de la pàgina 'Com apuntar-se'"
    )
    pagina_apuntarse_introducció = models.TextField(
        default="La Civada és una cooperativa autogestionada, i funciona gràcies a la implicació de tothom. Per tant, has de tenir present que formar-ne part equival a adquirir un compromís, que es tradueix en:",
        help_text="Text d'introducció sobre el compromís necessari"
    )
    
    # Secció compromís
    apuntarse_titol_compromis = models.CharField(
        max_length=100,
        default="Compromís",
        help_text="Títol de la secció sobre el compromís"
    )
    apuntarse_text_compromis = models.TextField(
        default="Participar en l'entrega de les cistelles de manera rotativa.\n\nAssistir a l'assemblea que es realitza periòdicament (cada dos mesos aproximadament).\n\nFormar part d'alguna de les comissions:",
        help_text="Descripció del compromís (separar punts amb doble salt de línia)"
    )
    
    # Secció comissions
    apuntarse_titol_comissions = models.CharField(
        max_length=100,
        default="Comissions",
        help_text="Títol de la secció sobre les comissions"
    )
    apuntarse_text_comissions = models.TextField(
        default="Comissió d'Economia: portar els comptes de la cooperativa.\n\nComissió de Benvinguda: informar i rebre els nous membres, gestionar les altes i baixes, controlar les quotes d'alta, lloguer i dipòsit.\n\nComissió de Compres: gestionar les comandes amb els proveïdors, mantenir l'estoc amb productes i passar factures a la comissió d'economia.\n\nComissió de Permanència (màsters): de manera rotativa, gestionar l'entrega de les cistelles.\n\nComissió de Difusió: gestionar la web i la presència de La Civada en les xarxes socials.",
        help_text="Descripció de les comissions (separar comissions amb doble salt de línia)"
    )
    
    # Secció formalització
    apuntarse_titol_formalitzacio = models.CharField(
        max_length=100,
        default="Formalitzar l'ingrés",
        help_text="Títol de la secció sobre la formalització"
    )
    apuntarse_text_formalitzacio = models.TextField(
        default="Per formalitzar el teu ingrés a La Civada, necessites:",
        help_text="Text introductori sobre els requisits"
    )
    apuntarse_requisits = models.TextField(
        default="Pagar un dipòsit de 50 euros (al cap de 2 mesos), que et serà retornat en cas de baixa.\n\nPagar 18 euros mensuals per unitat familiar en concepte de lloguer del local i col·laboració amb Cal Temerari (aquest preu varia en funció de les famílies sòcies, quant més famílies més baix serà).",
        help_text="Requisits per formalitzar l'ingrés (separar requisits amb doble salt de línia)"
    )
    
    # === PÀGINA CONTACTE ===
    pagina_contacte_titol = models.CharField(
        max_length=100,
        default="Contacte",
        help_text="Títol principal de la pàgina de contacte"
    )
    pagina_contacte_subtitol = models.TextField(
        default="Pots posar-te en contacte amb nosaltres per qualsevol dubte, suggeriment o col·laboració.",
        help_text="Subtítol explicatiu de la pàgina de contacte"
    )
    
    # Dades de contacte
    contacte_email = models.EmailField(
        default="info@civada.cat",
        help_text="Adreça de correu electrònic de contacte"
    )
    contacte_telefon = models.CharField(
        max_length=20,
        default="+34 600 000 000",
        help_text="Número de telèfon de contacte"
    )
    contacte_adreca = models.TextField(
        default="Carrer de l'Exemple, 123, 08000 Barcelona",
        help_text="Adreça física de la cooperativa"
    )

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