# Generated by Django 3.2.21 on 2025-03-01 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='socio', to=settings.AUTH_USER_MODEL),
        ),
    ]
