from django.core.management.base import BaseCommand
from web.models import ConfiguracioWeb


class Command(BaseCommand):
    help = 'Crea configuració inicial per ConfiguracioWeb si no existeix'

    def handle(self, *args, **options):
        if ConfiguracioWeb.objects.count() == 0:
            self.stdout.write('Creant ConfiguracioWeb per defecte...')
            
            config = ConfiguracioWeb.objects.create(
                nom_cooperativa="La Civada",
                titol_hero="Benvingut/da a La Civada",
                subtitol_hero="Cooperativa de consum responsable. Productes locals, ecològics i de proximitat.",
                titol_qui_som="Qui som?",
                text_qui_som="Som una cooperativa sense ànim de lucre formada per persones compromeses amb el consum responsable, la sostenibilitat i el suport als productors locals. El nostre objectiu és facilitar l'accés a productes ecològics i de qualitat, fomentant l'economia social i el respecte pel medi ambient.",
                titol_caracteristiques="Per què escollir La Civada?",
                titol_caracteristica_1="Productes ecològics",
                text_caracteristica_1="Tots els nostres productes són ecològics, sense químics i amb certificació CCPAE o relació de confiança.",
                icona_caracteristica_1="🌱",
                titol_caracteristica_2="Proximitat", 
                text_caracteristica_2="Apostem per productes de proximitat per reduir el transport i apropar consumidors i productors.",
                icona_caracteristica_2="🗺️",
                titol_caracteristica_3="Benefici social",
                text_caracteristica_3="Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.",
                icona_caracteristica_3="🤝",
                titol_cta="Vols formar part de la nostra cooperativa?",
                text_cta="Uneix-te a Civada i gaudeix de productes ecològics, locals i de qualitat.",
                text_boto_cta="Apunta't ara",
                contacte_email="info@civada.cat",
                contacte_telefon="+34 600 000 000",
                contacte_adreca="Carrer Plana de l'Hospital 26, Carrer Sant Esteve 11, Sant Cugat del Vallès",
                # Camps pàgina qui som
                pagina_qui_som_titol="Qui som",
                pagina_qui_som_introducció="La Civada és una cooperativa de consum ecològic de Sant Cugat del Vallès. Ens autogestionem amb l'objectiu d'accedir a productes ecològics, de proximitat i sense intermediaris. Cada setmana, els dimecres de 19.30 a 20.30 ens trobem al nostre local per recollir una cistella de verdures i fruites, a més d'altres productes.",
                qui_som_titol_cistella="La cistella",
                qui_som_text_cistella="Cada dimecres podem recollir una cistella de fruites i verdures que ens porta La Rural de Collserola, una cooperativa de pagesos que estan a Valldoreix i fan producció agroecològica. Cada família és sòcia de La Rural i fem la comanda directament al seu web.",
                qui_som_titol_altres_productes="Altres productes", 
                qui_som_text_altres_productes="Setmanalment: làctics (iogurts, formatges, quallades), pa, ous, fruits secs… Periòdicament: comandes directes a proveïdors (vedella, pollastre, xai, peix, oli, vins, productes d'higiene...). Petit estoc al local: mel, arròs, llegums, cafè, te, sucre, pots de tomàquet, cigrons, llenties, olives, sucs, cerveses…",
                qui_som_criteris_seleccio="Productes ecològics, sense químics, amb certificació CCPAE o relació de confiança. De proximitat, per reduir transport i apropar consumidors i productors. Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.",
                qui_som_titol_ubicacio="On som",
                qui_som_text_ubicacio="El nostre local es troba a Cal Temerari: Carrer Plana de l'Hospital 26, Carrer Sant Esteve 11, Sant Cugat del Vallès",
                # Camps pàgina apuntar-se
                pagina_apuntarse_titol="Com apuntar-te",
                pagina_apuntarse_introducció="La Civada és una cooperativa autogestionada, i funciona gràcies a la implicació de tothom. Per tant, has de tenir present que formar-ne part equival a adquirir un compromís, que es tradueix en:",
                apuntarse_titol_compromis="Compromís",
                apuntarse_text_compromis="Participar en l'entrega de les cistelles de manera rotativa. Assistir a l'assemblea que es realitza periòdicament (cada dos mesos aproximadament). Formar part d'alguna de les comissions.",
                apuntarse_titol_comissions="Comissions",
                apuntarse_text_comissions="Comissió d'Economia: portar els comptes de la cooperativa. Comissió de Benvinguda: informar i rebre els nous membres. Comissió de Compres: gestionar les comandes amb els proveïdors. Comissió de Permanència (màsters): gestionar l'entrega de les cistelles. Comissió de Difusió: gestionar la web i xarxes socials.",
                apuntarse_titol_formalitzacio="Formalitzar l'ingrés",
                apuntarse_text_formalitzacio="Per formalitzar el teu ingrés a La Civada, necessites: Pagar un dipòsit de 50 euros (al cap de 2 mesos), que et serà retornat en cas de baixa. Pagar 18 euros mensuals per unitat familiar en concepte de lloguer del local i col·laboració amb Cal Temerari.",
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