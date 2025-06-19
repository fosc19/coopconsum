#!/usr/bin/env python
"""
Script per actualitzar camps ConfiguracioWeb a format HTML per CKEditor
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/home/fosca/proyectos/coopconsum')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coopconsum.settings')
django.setup()

from web.models import ConfiguracioWeb

def actualitzar_config_html():
    """Actualitza els camps de text pla a format HTML"""
    try:
        config = ConfiguracioWeb.objects.first()
        if not config:
            print("❌ No s'ha trobat cap ConfiguracioWeb")
            return False

        print("📝 Actualitzant camps de ConfiguracioWeb a format HTML...")

        # qui_som_text_altres_productes
        if 'Setmanalment:' in config.qui_som_text_altres_productes and '<ul>' not in config.qui_som_text_altres_productes:
            config.qui_som_text_altres_productes = """<ul>
<li>Setmanalment: làctics (iogurts, formatges, quallades), pa, ous, fruits secs…</li>
<li>Periòdicament: comandes directes a proveïdors (vedella, pollastre, xai, peix, oli, vins, productes d'higiene...)</li>
<li>Petit estoc al local: mel, arròs, llegums, cafè, te, sucre, pots de tomàquet, cigrons, llenties, olives, sucs, cerveses…</li>
</ul>"""
            print("✅ qui_som_text_altres_productes actualitzat")

        # qui_som_criteris_seleccio
        if 'Productes ecològics' in config.qui_som_criteris_seleccio and '<ul>' not in config.qui_som_criteris_seleccio:
            config.qui_som_criteris_seleccio = """<ul>
<li>Productes ecològics, sense químics, amb certificació CCPAE o relació de confiança.</li>
<li>De proximitat, per reduir transport i apropar consumidors i productors.</li>
<li>Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d'exclusió, etc.</li>
</ul>"""
            print("✅ qui_som_criteris_seleccio actualitzat")

        # apuntarse_text_compromis
        if 'Participar en l' in config.apuntarse_text_compromis and '<ul>' not in config.apuntarse_text_compromis:
            config.apuntarse_text_compromis = """<ul>
<li>Participar en l'entrega de les cistelles de manera rotativa.</li>
<li>Assistir a l'assemblea que es realitza periòdicament (cada dos mesos aproximadament).</li>
<li>Formar part d'alguna de les comissions:</li>
</ul>"""
            print("✅ apuntarse_text_compromis actualitzat")

        # apuntarse_text_comissions
        if 'Comissió d' in config.apuntarse_text_comissions and '<p>' not in config.apuntarse_text_comissions:
            config.apuntarse_text_comissions = """<p><strong>Comissió d'Economia:</strong> portar els comptes de la cooperativa.</p>
<p><strong>Comissió de Benvinguda:</strong> informar i rebre els nous membres, gestionar les altes i baixes, controlar les quotes d'alta, lloguer i dipòsit.</p>
<p><strong>Comissió de Compres:</strong> gestionar les comandes amb els proveïdors, mantenir l'estoc amb productes i passar factures a la comissió d'economia.</p>
<p><strong>Comissió de Permanència (màsters):</strong> de manera rotativa, gestionar l'entrega de les cistelles.</p>
<p><strong>Comissió de Difusió:</strong> gestionar la web i la presència de La Civada en les xarxes socials.</p>"""
            print("✅ apuntarse_text_comissions actualitzat")

        # apuntarse_requisits  
        if 'Pagar un dipòsit' in config.apuntarse_requisits and '<ul>' not in config.apuntarse_requisits:
            config.apuntarse_requisits = """<ul>
<li>Pagar un dipòsit de 50 euros (al cap de 2 mesos), que et serà retornat en cas de baixa.</li>
<li>Pagar 18 euros mensuals per unitat familiar en concepte de lloguer del local i col·laboració amb Cal Temerari (aquest preu varia en funció de les famílies sòcies, quant més famílies més baix serà).</li>
</ul>"""
            print("✅ apuntarse_requisits actualitzat")

        config.save()
        print("🎉 ConfiguracioWeb actualitzada correctament amb format HTML!")
        return True

    except Exception as e:
        print(f"❌ Error actualitzant ConfiguracioWeb: {e}")
        return False

if __name__ == '__main__':
    actualitzar_config_html()