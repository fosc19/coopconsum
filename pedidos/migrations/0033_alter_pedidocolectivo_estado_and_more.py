# Generated by Django 4.2.20 on 2025-04-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0032_remove_seleccionsocio_estado_validacion_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidocolectivo',
            name='estado',
            field=models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado'), ('pendiente', 'Pendent'), ('inactivo', 'Inactivo')], default='abierto', max_length=20),
        ),
        migrations.AlterField(
            model_name='propuestacorreccioncomanda',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendent'), ('validada', 'Validada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=20),
        ),
    ]
