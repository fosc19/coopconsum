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
                pagina_qui_som_introducció="La Civada és una cooperativa de consum ecològic de Sant Cugat del Vallès. Ens autogestionem amb l'objectiu d'accedir a productes ecològics, de proximitat i sense intermediaris. Cada setmana, els dimecres de 19.30 a 20.30 ens trobem al nostre local per recollir una cistella de verdures i fruites, a més d'altres productes.",
                qui_som_titol_cistella="La cistella",
                qui_som_text_cistella='Cada dimecres podem recollir una cistella de fruites i verdures que ens porta <a href="https://www.laruraldecollserola.com" target="_blank">La Rural de Collserola</a>, una cooperativa de pagesos que estan a Valldoreix i fan producció agroecològica. Cada família és sòcia de La Rural i fem la comanda directament al seu web.',
                qui_som_titol_altres_productes="Altres productes", 
                qui_som_text_altres_productes="<ul><li>Setmanalment: làctics (iogurts, formatges, quallades), pa, ous, fruits secs…</li><li>Periòdicament: comandes directes a proveïdors (vedella, pollastre, xai, peix, oli, vins, productes d'higiene...)</li><li>Petit estoc al local: mel, arròs, llegums, cafè, te, sucre, pots de tomàquet, cigrons, llenties, olives, sucs, cerveses…</li></ul>",
                qui_som_criteris_seleccio="<ul><li>Productes ecològics, sense químics, amb certificació CCPAE o relació de confiança.</li><li>De proximitat, per reduir transport i apropar consumidors i productors.</li><li>Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.</li></ul>",
                qui_som_titol_ubicacio="On som",
                qui_som_text_ubicacio="El nostre local es troba a Cal Temerari:\nCarrer Plana de l'Hospital 26, Carrer Sant Esteve 11, Sant Cugat del Vallès",
                # Camps pàgina apuntar-se
                pagina_apuntarse_titol="Com apuntar-se",
                pagina_apuntarse_introducció="La Civada és una cooperativa autogestionada, i funciona gràcies a la implicació de tothom. Per tant, has de tenir present que formar-ne part equival a adquirir un compromís, que es tradueix en:",
                apuntarse_titol_compromis="Compromís",
                apuntarse_text_compromis="<ul><li>Participar en l'entrega de les cistelles de manera rotativa.</li><li>Assistir a l'assemblea que es realitza periòdicament (cada dos mesos aproximadament).</li><li>Formar part d'alguna de les comissions:</li></ul>",
                apuntarse_titol_comissions="Comissions",
                apuntarse_text_comissions="<p><strong>Comissió d'Economia:</strong> portar els comptes de la cooperativa.</p><p><strong>Comissió de Benvinguda:</strong> informar i rebre els nous membres, gestionar les altes i baixes, controlar les quotes d'alta, lloguer i dipòsit.</p><p><strong>Comissió de Compres:</strong> gestionar les comandes amb els proveïdors, mantenir l'estoc amb productes i passar factures a la comissió d'economia.</p><p><strong>Comissió de Permanència (màsters):</strong> de manera rotativa, gestionar l'entrega de les cistelles.</p><p><strong>Comissió de Difusió:</strong> gestionar la web i la presència de La Civada en les xarxes socials.</p>",
                apuntarse_titol_formalitzacio="Formalitzar l'ingrés",
                apuntarse_text_formalitzacio="Per formalitzar el teu ingrés a La Civada, necessites:",
                apuntarse_requisits="<ul><li>Pagar un dipòsit de 50 euros (al cap de 2 mesos), que et serà retornat en cas de baixa.</li><li>Pagar 18 euros mensuals per unitat familiar en concepte de lloguer del local i col·laboració amb Cal Temerari (aquest preu varia en funció de les famílies sòcies, quant més famílies més baix serà).</li></ul>",
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