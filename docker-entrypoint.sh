#!/bin/bash
set -e

# Esperar que la base de dades estigui disponible
echo "Esperant que la base de dades estigui disponible..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Base de dades no disponible, esperant..."
  sleep 2
done
echo "Base de dades disponible!"

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

# Iniciar servidor
echo "Iniciant servidor..."
exec gunicorn coopconsum.wsgi:application --bind 0.0.0.0:8000 --workers 3