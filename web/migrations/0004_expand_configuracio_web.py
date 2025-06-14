# Generated manually for expanded ConfiguracioWeb model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_configuracio_web'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracioWeb',
            name='nom_cooperativa',
            field=models.CharField(default='La Civada', help_text='Nom de la cooperativa que apareixerà arreu de la web', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_hero',
            field=models.CharField(default='Benvingut/da a {nom_cooperativa}', help_text='Títol principal de la pàgina d\'inici. Usa {nom_cooperativa} per inserir el nom automàticament', max_length=200),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='subtitol_hero',
            field=models.TextField(default='Cooperativa de consum responsable. Productes locals, ecològics i de proximitat.', help_text='Text descriptiu sota el títol principal'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_qui_som',
            field=models.CharField(default='Qui som?', help_text='Títol de la secció \'Qui som\'', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_qui_som',
            field=models.TextField(default='Som una cooperativa sense ànim de lucre formada per persones compromeses amb el consum responsable, la sostenibilitat i el suport als productors locals. El nostre objectiu és facilitar l\'accés a productes ecològics i de qualitat, fomentant l\'economia social i el respecte pel medi ambient.', help_text='Descripció detallada de la cooperativa'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_caracteristiques',
            field=models.CharField(default='Per què escollir {nom_cooperativa}?', help_text='Títol de la secció de característiques. Usa {nom_cooperativa} per inserir el nom automàticament', max_length=200),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_caracteristica_1',
            field=models.CharField(default='Productes ecològics', help_text='Títol de la primera característica', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_caracteristica_1',
            field=models.TextField(default='Tots els nostres productes són ecològics, sense químics i amb certificació CCPAE o relació de confiança.', help_text='Descripció de la primera característica'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='icona_caracteristica_1',
            field=models.CharField(default='fas fa-leaf', help_text='Classe CSS de l\'icona (Font Awesome). Ex: fas fa-leaf, fas fa-heart, etc.', max_length=50),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_caracteristica_2',
            field=models.CharField(default='Proximitat', help_text='Títol de la segona característica', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_caracteristica_2',
            field=models.TextField(default='Apostem per productes de proximitat per reduir el transport i apropar consumidors i productors.', help_text='Descripció de la segona característica'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='icona_caracteristica_2',
            field=models.CharField(default='fas fa-map-marker-alt', help_text='Classe CSS de l\'icona (Font Awesome)', max_length=50),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_caracteristica_3',
            field=models.CharField(default='Benefici social', help_text='Títol de la tercera característica', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_caracteristica_3',
            field=models.TextField(default='Prioritzem productes amb benefici social: comerç just, elaborats per persones en risc d\'exclusió, etc.', help_text='Descripció de la tercera característica'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='icona_caracteristica_3',
            field=models.CharField(default='fas fa-hands-helping', help_text='Classe CSS de l\'icona (Font Awesome)', max_length=50),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='titol_cta',
            field=models.CharField(default='Vols formar part de la nostra cooperativa?', help_text='Títol de la secció final d\'inscripció', max_length=200),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_cta',
            field=models.TextField(default='Uneix-te a {nom_cooperativa} i gaudeix de productes ecològics, locals i de qualitat.', help_text='Text descriptiu del call to action. Usa {nom_cooperativa} per inserir el nom automàticament'),
        ),
        migrations.AddField(
            model_name='configuracioWeb',
            name='text_boto_cta',
            field=models.CharField(default='Apunta\'t ara', help_text='Text del botó de call to action', max_length=50),
        ),
        migrations.AlterModelOptions(
            name='configuracioWeb',
            options={'verbose_name': 'Configuració Web', 'verbose_name_plural': 'Configuració Web'},
        ),
    ]