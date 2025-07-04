# Generated by Django 3.2.21 on 2025-04-12 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_producto_unidad_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='descripcion_corta',
            field=models.CharField(blank=True, help_text='Descripción breve del proveedor para mostrar en la galería.', max_length=255),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='imagen',
            field=models.ImageField(blank=True, help_text='Imagen del proveedor para la galería.', null=True, upload_to='proveedores/'),
        ),
    ]
