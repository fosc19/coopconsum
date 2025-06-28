# Generated manually to add social media fields to ConfiguracioWeb

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_configuracioweb_apuntarse_requisits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracioweb',
            name='mostrar_facebook',
            field=models.BooleanField(default=False, help_text='Mostrar enllaç de Facebook al footer i pàgines'),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='facebook_url',
            field=models.URLField(blank=True, default='', help_text='URL completa de la pàgina de Facebook (ex: https://facebook.com/nomcooperativa)'),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='mostrar_instagram',
            field=models.BooleanField(default=False, help_text="Mostrar enllaç d'Instagram al footer i pàgines"),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='instagram_url',
            field=models.URLField(blank=True, default='', help_text="URL completa del perfil d'Instagram (ex: https://instagram.com/nomcooperativa)"),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='mostrar_twitter',
            field=models.BooleanField(default=False, help_text='Mostrar enllaç de Twitter al footer i pàgines'),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='twitter_url',
            field=models.URLField(blank=True, default='', help_text='URL completa del perfil de Twitter (ex: https://twitter.com/nomcooperativa)'),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='mostrar_whatsapp',
            field=models.BooleanField(default=False, help_text='Mostrar enllaç de WhatsApp al footer i pàgines'),
        ),
        migrations.AddField(
            model_name='configuracioweb',
            name='whatsapp_telefon',
            field=models.CharField(blank=True, default='', help_text='Número de WhatsApp sense espais (ex: 34600000000)', max_length=20),
        ),
    ]