from django.core.management.base import BaseCommand
from web.models import ConfiguracioWeb


class Command(BaseCommand):
    help = 'Crea configuració inicial per ConfiguracioWeb si no existeix'

    def handle(self, *args, **options):
        if ConfiguracioWeb.objects.count() == 0:
            self.stdout.write('Creant ConfiguracioWeb per defecte...')
            
            config = ConfiguracioWeb.objects.create(
                nom_cooperativa="cooperativa",
                titol_hero="Benvinguts a {nom_cooperativa}",
                subtitol_hero="Cooperativa de consum responsable. Productes locals, ecològics i de proximitat.",
                titol_qui_som="Qui som?",
                text_qui_som="Som una cooperativa de consum responsable formada per persones compromeses amb la sostenibilitat i el suport als productors locals. El nostre objectiu és facilitar l'accés a productes ecològics i de qualitat, fomentant l'economia social i el respecte pel medi ambient.",
                titol_caracteristiques="Per què escollir {nom_cooperativa}?",
                titol_caracteristica_1="Productes ecològics",
                text_caracteristica_1="Tots els nostres productes són ecològics, sense químics i amb certificació o relació de confiança.",
                icona_caracteristica_1="fa-leaf",
                titol_caracteristica_2="Proximitat", 
                text_caracteristica_2="Apostem per productes de proximitat per reduir el transport i apropar consumidors i productors.",
                icona_caracteristica_2="fa-map-marker-alt",
                titol_caracteristica_3="Benefici social",
                text_caracteristica_3="Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.",
                icona_caracteristica_3="fa-hands-helping",
                titol_cta="Vols formar part de la nostra cooperativa?",
                text_cta="Uneix-te a {nom_cooperativa} i gaudeix de productes ecològics, locals i de qualitat.",
                text_boto_cta="Apunta't ara",
                contacte_email="admin@cooperativa.local",
                contacte_telefon="+34 600 000 000",
                contacte_adreca="Carrer de l'Exemple, 123, 08000 Barcelona",
                # Camps pàgina qui som
                pagina_qui_som_titol="Qui som",
                pagina_qui_som_introducció="{nom_cooperativa} és una cooperativa de consum responsable que s'autogestiona amb l'objectiu d'accedir a productes ecològics, de proximitat i sense intermediaris. Ens trobem regularment al nostre local per recollir una cistella de verdures i fruites, a més d'altres productes.",
                qui_som_titol_cistella="La nostra cistella",
                qui_som_text_cistella="Setmanalment podem recollir una cistella de fruites i verdures que ens porten productors locals amb producció ecològica. Cada família fa la comanda directament als productors.",
                qui_som_titol_altres_productes="Altres productes", 
                qui_som_text_altres_productes="Setmanalment: làctics (iogurts, formatges), pa, ous, fruits secs… Periòdicament: comandes directes a proveïdors (carn, peix, oli, vins, productes d'higiene...). Petit estoc al local: mel, arròs, llegums, cafè, te, conserves…",
                qui_som_criteris_seleccio="Productes ecològics, sense químics, amb certificació o relació de confiança. De proximitat, per reduir transport i apropar consumidors i productors. Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió.",
                qui_som_titol_ubicacio="On ens trobes",
                qui_som_text_ubicacio="El nostre local es troba a [adreça del local]. Consulta els horaris de recollida i contacta'ns per més informació.",
                # Camps pàgina apuntar-se
                pagina_apuntarse_titol="Com apuntar-se",
                pagina_apuntarse_introducció="{nom_cooperativa} és una cooperativa autogestionada que funciona gràcies a la implicació de tothom. Per tant, has de tenir present que formar-ne part equival a adquirir un compromís que es tradueix en:",
                apuntarse_titol_compromis="Compromís",
                apuntarse_text_compromis="Participar en l'entrega dels productes de manera rotativa. Assistir a l'assemblea que es realitza periòdicament. Formar part d'alguna de les comissions de treball.",
                apuntarse_titol_comissions="Comissions",
                apuntarse_text_comissions="Comissió d'Economia: portar els comptes de la cooperativa. Comissió de Benvinguda: informar i rebre els nous membres. Comissió de Compres: gestionar les comandes amb els proveïdors. Comissió de Distribució: gestionar l'entrega dels productes. Comissió de Difusió: gestionar comunicació i presència web.",
                apuntarse_titol_formalitzacio="Formalitzar l'ingrés",
                apuntarse_text_formalitzacio="Per formalitzar el teu ingrés a {nom_cooperativa}, necessites complir els requisits establerts per l'assemblea: quota d'entrada, quotes mensuals i participació en les tasques cooperatives.",
                apuntarse_requisits="Compromís amb els valors del consum responsable, la sostenibilitat i l'economia social. Participació activa en les tasques de la cooperativa.",
                # Camps pàgina contacte
                pagina_contacte_titol="Contacte",
                pagina_contacte_subtitol="Posa't en contacte amb nosaltres"
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ ConfiguracioWeb creada amb èxit: {config.nom_cooperativa}')
            )
        else:
            config = ConfiguracioWeb.objects.first()
            self.stdout.write(
                self.style.WARNING(f'✅ ConfiguracioWeb ja existeix: {config.nom_cooperativa}')
            )