#!/bin/bash
set -e

# Crear settings.py des de settings_base.py amb variables d'entorn
echo "Creant settings.py amb variables d'entorn..."
cat > /app/coopconsum/settings.py << EOF
import os
from .settings_base import *

# Configuració de seguretat
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Configuració de base de dades
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'coopconsum_db'),
        'USER': os.environ.get('POSTGRES_USER', 'coopconsum_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Configuració CORS i CSRF
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
EOF

# Esperar que la base de dades estigui disponible
echo "Esperant que la base de dades estigui disponible..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Base de dades no disponible, esperant..."
  sleep 2
done
echo "Base de dades disponible!"

# Generar migracions si hi ha canvis de models
echo "Generant migracions si cal..."
python manage.py makemigrations --noinput

# Executar migracions
echo "Executant migracions..."
python manage.py migrate --noinput

# Crear superusuari si no existeix
echo "Creant superusuari..."
python manage.py shell << EOF
from django.contrib.auth.models import User
import os

username = 'admin'
email = os.environ.get('COOP_EMAIL', 'admin@cooperativa.local')
password = 'cooperativa2025'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superusuari '{username}' creat correctament")
else:
    print(f"Superusuari '{username}' ja existeix")
EOF

# Col·lectar fitxers estàtics
echo "Col·lectant fitxers estàtics..."
python manage.py collectstatic --noinput

# Crear configuració inicial de la web si no existeix
echo "Creant configuració inicial de la web..."
python manage.py crear_configuracio_inicial

# Copiar imatges essencials al directori media
echo "Creant directoris media i copiant imatges essencials..."
mkdir -p /app/media/galeria
if [ -f "/app/coopconsum/galeria/cistella.jpg" ]; then
    cp /app/coopconsum/galeria/cistella.jpg /app/media/galeria/cistella.jpg
    echo "✅ Imatge cistella.jpg copiada"
else
    echo "⚠️ No s'ha trobat coopconsum/galeria/cistella.jpg"
fi

# Iniciar servidor amb configuració optimitzada
echo "Iniciant servidor amb configuració optimitzada..."
exec gunicorn coopconsum.wsgi:application --config gunicorn.conf.py