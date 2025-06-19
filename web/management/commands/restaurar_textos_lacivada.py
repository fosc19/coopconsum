from django.core.management.base import BaseCommand
from web.models import ConfiguracioWeb


class Command(BaseCommand):
    help = 'Restaura els textos originals de La Civada a ConfiguracioWeb'

    def handle(self, *args, **options):
        config = ConfiguracioWeb.objects.first()
        
        if not config:
            self.stdout.write(
                self.style.ERROR('❌ No hi ha ConfiguracioWeb. Executa primer crear_configuracio_inicial')
            )
            return
        
        self.stdout.write('🔄 Actualitzant textos originals de La Civada...')
        
        # ===== INFORMACIÓ BÀSICA =====
        config.nom_cooperativa = "La Civada"
        
        # ===== PÀGINA D'INICI =====
        # Hero section
        config.titol_hero = "Benvingut/da a {nom_cooperativa}"
        config.subtitol_hero = "Cooperativa de consum responsable. Productes locals, ecològics i de proximitat."
        
        # Secció Qui som (pàgina d'inici)
        config.titol_qui_som = "Qui som?"
        config.text_qui_som = "Som una cooperativa sense ànim de lucre formada per persones compromeses amb el consum responsable, la sostenibilitat i el suport als productors locals. El nostre objectiu és facilitar l'accés a productes ecològics i de qualitat, fomentant l'economia social i el respecte pel medi ambient."
        
        # Característiques
        config.titol_caracteristiques = "Per què escollir {nom_cooperativa}?"
        
        # Característica 1: Productes ecològics
        config.titol_caracteristica_1 = "Productes ecològics"
        config.text_caracteristica_1 = "Tots els nostres productes són ecològics, sense químics i amb certificació CCPAE o relació de confiança."
        config.icona_caracteristica_1 = "fas fa-leaf"
        
        # Característica 2: Proximitat
        config.titol_caracteristica_2 = "Proximitat"
        config.text_caracteristica_2 = "Apostem per productes de proximitat per reduir el transport i apropar consumidors i productors."
        config.icona_caracteristica_2 = "fas fa-map-marker-alt"
        
        # Característica 3: Benefici social
        config.titol_caracteristica_3 = "Benefici social"
        config.text_caracteristica_3 = "Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc."
        config.icona_caracteristica_3 = "fas fa-hands-helping"
        
        # Call to Action
        config.titol_cta = "Vols formar part de la nostra cooperativa?"
        config.text_cta = "Uneix-te a {nom_cooperativa} i gaudeix de productes ecològics, locals i de qualitat."
        config.text_boto_cta = "Apunta't ara"
        
        # ===== PÀGINA "QUI SOM" =====
        config.pagina_qui_som_titol = "Qui som"
        config.pagina_qui_som_introducció = "La Civada és una cooperativa de consum ecològic de Sant Cugat del Vallès. Ens autogestionem amb l'objectiu d'accedir a productes ecològics, de proximitat i sense intermediaris. Cada setmana, els dimecres de 19.30 a 20.30 ens trobem al nostre local per recollir una cistella de verdures i fruites, a més d'altres productes."
        
        # La cistella
        config.qui_som_titol_cistella = "La cistella"
        config.qui_som_text_cistella = "Cada dimecres podem recollir una cistella de fruites i verdures que ens porta La Rural de Collserola, una cooperativa de pagesos que estan a Valldoreix i fan producció agroecològica. Cada família és sòcia de La Rural i fem la comanda directament al seu web."
        
        # Altres productes
        config.qui_som_titol_altres_productes = "Altres productes"
        config.qui_som_text_altres_productes = "Setmanalment: làctics (iogurts, formatges, quallades), pa, ous, fruits secs…\n\nPeriòdicament: comandes directes a proveïdors (vedella, pollastre, xai, peix, oli, vins, productes d'higiene...)\n\nPetit estoc al local: mel, arròs, llegums, cafè, te, sucre, pots de tomàquet, cigrons, llenties, olives, sucs, cerveses…"
        config.qui_som_criteris_seleccio = "Productes ecològics, sense químics, amb certificació CCPAE o relació de confiança.\n\nDe proximitat, per reduir transport i apropar consumidors i productors.\n\nPriorititzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc."
        
        # Ubicació
        config.qui_som_titol_ubicacio = "On som"
        config.qui_som_text_ubicacio = "El nostre local es troba a Cal Temerari:\nCarrer Plana de l'Hospital 26, Carrer Sant Esteve 11, Sant Cugat del Vallès"
        
        # ===== PÀGINA "COM APUNTAR-SE" =====
        config.pagina_apuntarse_titol = "Com apuntar-te"
        config.pagina_apuntarse_introducció = "La Civada és una cooperativa autogestionada, i funciona gràcies a la implicació de tothom. Per tant, has de tenir present que formar-ne part equival a adquirir un compromís, que es tradueix en:"
        
        # Compromís
        config.apuntarse_titol_compromis = "Compromís"
        config.apuntarse_text_compromis = "Participar en l'entrega de les cistelles de manera rotativa.\n\nAssistir a l'assemblea que es realitza periòdicament (cada dos mesos aproximadament).\n\nFormar part d'alguna de les comissions:"
        
        # Comissions
        config.apuntarse_titol_comissions = "Comissions"
        config.apuntarse_text_comissions = "Comissió d'Economia: portar els comptes de la cooperativa.\n\nComissió de Benvinguda: informar i rebre els nous membres, gestionar les altes i baixes, controlar les quotes d'alta, lloguer i dipòsit.\n\nComissió de Compres: gestionar les comandes amb els proveïdors, mantenir l'estoc amb productes i passar factures a la comissió d'economia.\n\nComissió de Permanència (màsters): de manera rotativa, gestionar l'entrega de les cistelles.\n\nComissió de Difusió: gestionar la web i la presència de La Civada en les xarxes socials."
        
        # Formalització
        config.apuntarse_titol_formalitzacio = "Formalitzar l'ingrés"
        config.apuntarse_text_formalitzacio = "Per formalitzar el teu ingrés a La Civada, necessites:"
        config.apuntarse_requisits = "Pagar un dipòsit de 50 euros (al cap de 2 mesos), que et serà retornat en cas de baixa.\n\nPagar 18 euros mensuals per unitat familiar en concepte de lloguer del local i col·laboració amb Cal Temerari (aquest preu varia en funció de les famílies sòcies, quant més famílies més baix serà)."
        
        # ===== PÀGINA "CONTACTE" =====
        config.pagina_contacte_titol = "Contacte"
        config.pagina_contacte_subtitol = "Pots posar-te en contacte amb nosaltres per qualsevol dubte, suggeriment o col·laboració."
        
        # Dades de contacte reals de La Civada
        config.contacte_email = "info@civada.cat"
        config.contacte_telefon = "+34 654 321 098"
        config.contacte_adreca = "Cal Temerari\\nCarrer Plana de l'Hospital 26, Carrer Sant Esteve 11\\n08172 Sant Cugat del Vallès, Barcelona"
        
        # Guardar tots els canvis
        config.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Textos de La Civada restaurats correctament!')
        )
        self.stdout.write(f'📝 Cooperativa: {config.nom_cooperativa}')
        self.stdout.write(f'📧 Email: {config.contacte_email}')