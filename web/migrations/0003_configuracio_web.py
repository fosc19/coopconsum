# Generated manually for ConfiguracioWeb model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_galeriacategoria_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracioWeb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imatge_principal_home', models.ImageField(blank=True, help_text="Imatge principal que apareix a la pàgina d'inici (secció 'Qui som?')", null=True, upload_to='configuracio/')),
            ],
            options={
                'verbose_name': 'Configuració Web',
                'verbose_name_plural': 'Configuració Web',
            },
        ),
    ]