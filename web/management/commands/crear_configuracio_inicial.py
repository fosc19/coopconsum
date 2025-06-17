from django.core.management.base import BaseCommand
from web.models import ConfiguracioWeb


class Command(BaseCommand):
    help = 'Crea configuració inicial per ConfiguracioWeb si no existeix'

    def handle(self, *args, **options):
        if ConfiguracioWeb.objects.count() == 0:
            self.stdout.write('Creant ConfiguracioWeb per defecte...')
            
            config = ConfiguracioWeb.objects.create(
                nom_cooperativa="cooperativa",
                titol_hero="Benvinguts a la nostra cooperativa",
                subtitol_hero="Consum responsable i sostenible per a tothom",
                titol_qui_som="Qui som",
                text_qui_som="Som una cooperativa de consum responsable dedicada a promoure l'economia social i el desenvolupament sostenible.",
                titol_caracteristiques="Les nostres característiques",
                titol_caracteristica_1="Productes locals",
                text_caracteristica_1="Treballem directament amb productors locals per garantir productes frescos i de qualitat.",
                icona_caracteristica_1="🌱",
                titol_caracteristica_2="Consum responsable", 
                text_caracteristica_2="Fomentem el consum sostenible i respectuós amb el medi ambient.",
                icona_caracteristica_2="♻️",
                titol_caracteristica_3="Economia social",
                text_caracteristica_3="Basem el nostre model en els principis del cooperativisme i l'economia solidària.",
                icona_caracteristica_3="🤝",
                titol_cta="Uneix-te a nosaltres",
                text_cta="Forma part de la nostra cooperativa i contribueix al canvi cap a un consum més responsable.",
                text_boto_cta="Contacta",
                contacte_email="admin@cooperativa.local",
                contacte_telefon="",
                contacte_adreca="",
                # Camps pàgina qui som
                pagina_qui_som_titol="Qui som",
                pagina_qui_som_introducció="Coneix la nostra cooperativa de consum responsable.",
                qui_som_titol_cistella="La nostra cistella",
                qui_som_text_cistella="Productes frescos i de temporada seleccionats amb cura.",
                qui_som_titol_altres_productes="Altres productes", 
                qui_som_text_altres_productes="Varietat de productes ecològics i locals.",
                qui_som_criteris_seleccio="Els nostres criteris de selecció es basen en la qualitat, proximitat i sostenibilitat.",
                qui_som_titol_ubicacio="On ens trobes",
                qui_som_text_ubicacio="Visita'ns al nostre local per conèixer tots els nostres productes.",
                # Camps pàgina apuntar-se
                pagina_apuntarse_titol="Com apuntar-se",
                pagina_apuntarse_introducció="Descobreix com formar part de la nostra cooperativa.",
                apuntarse_titol_compromis="Compromís",
                apuntarse_text_compromis="Compartim els valors del consum responsable i l'economia social.",
                apuntarse_titol_comissions="Comissions",
                apuntarse_text_comissions="Participa en les comissions de treball de la cooperativa.",
                apuntarse_titol_formalitzacio="Formalització",
                apuntarse_text_formalitzacio="Procés senzill per formalitzar la teva adhesió.",
                apuntarse_requisits="Requisits per ser soci de la cooperativa.",
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