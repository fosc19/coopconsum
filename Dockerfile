# Dockerfile per Django - La Civada
FROM python:3.12-slim

# Variables d'entorn
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Instal·lar dependències del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Crear usuari per l'aplicació
RUN groupadd -r django && useradd -r -g django django

# Crear directori de treball
WORKDIR /app

# Copiar requirements i instal·lar dependències Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codi de l'aplicació
COPY . .

# Copiar configuració optimitzada de Gunicorn
COPY gunicorn.conf.py .

# Crear directoris necessaris
RUN mkdir -p /app/staticfiles /app/media

# Configurar permisos
RUN chmod +x /app/docker-entrypoint.sh
RUN chown -R django:django /app

# Canviar a usuari django
USER django

# Exposar port
EXPOSE 8000

# Punt d'entrada
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "coopconsum.wsgi:application", "--config", "gunicorn.conf.py"]
