# Generated by Django 4.2.20 on 2025-06-07 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0020_alter_cuentasocio_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movimientocuenta',
            options={'ordering': ['-fecha'], 'verbose_name': 'Movimiento de Cuenta', 'verbose_name_plural': 'Moviments de comptes'},
        ),
    ]
