# 🤝 CoopConsum - Sistema de Gestió per Cooperatives

[![Django Tests](https://github.com/fosc19/coopconsum/actions/workflows/django.yml/badge.svg)](https://github.com/fosc19/coopconsum/actions/workflows/django.yml)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Django Version](https://img.shields.io/badge/django-5.1.6-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Tests](https://img.shields.io/badge/tests-65%20passing-brightgreen)

Sistema complet de gestió per cooperatives de consum responsable, desenvolupat amb Django. Inclou gestió de socis, comandes, proveïdors, productes, configuració web dinàmica i una API pública per compartir informació entre cooperatives.

## 🧪 Testing & Quality

✅ **65 tests unitaris** cobreixen tota la funcionalitat core:
- 11 tests models socis (Socio, CuentaSocio, MovimientoCuenta)
- 22 tests workflow pedidos (PedidoColectivo, ComandaRecurrente, SeleccionSocio)  
- 22 tests catàleg productos (Categoria, Proveedor, Producto)
- 36 tests API REST (endpoints públics, seguretat, filtres)
- 14 tests esdeveniments (EventoCalendario, compartició API)

**Executar tests**:
```bash
# Tots els tests
python manage.py test --verbosity=2

# Per app específica
python manage.py test socios --verbosity=2
python manage.py test api --verbosity=2

# Amb coverage
coverage run --source='.' manage.py test
coverage report -m
```

## ✨ Característiques

- 👥 **Gestió de Socis**: Registre, perfils i administració de membres amb ingrés opcional de comentaris
- 📦 **Sistema de Comandes**: Comandes col·lectives amb seguiment automatitzat
- 🏪 **Gestió de Proveïdors**: Catàleg de proveïdors locals i ecològics
- 🛒 **Catàleg de Productes**: Organització per categories amb preus
- 🌐 **Web Pública**: Lloc web amb configuració dinàmica, xarxes socials i contacte
- 🔗 **API REST**: Intercanvi de dades entre cooperatives
- 📱 **Responsive**: Disseny adaptat a mòbils i tauletes

## 🚀 Instal·lació Ràpida

### Prerequisits

- Python 3.8 o superior
- pip (gestor de paquets de Python)
- Git

### Passos d'Instal·lació

1. **Clonar el repositori**
```bash
git clone https://github.com/fosc19/coopconsum.git
cd coopconsum
```

2. **Crear entorn virtual**
```bash
python -m venv venv
# A Windows:
venv\Scripts\activate
# A Linux/Mac:
source venv/bin/activate
```

3. **Instal·lar dependències**
```bash
pip install -r requirements.txt
```

4. **Configurar settings**
```bash
# Copiar l'arxiu de configuració d'exemple
cp coopconsum/settings_example.py coopconsum/settings.py
# Editar settings.py amb les teves configuracions específiques
```

5. **Configurar base de dades**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuari**
```bash
python manage.py createsuperuser
```

7. **Executar servidor de desenvolupament**
```bash
python manage.py runserver
```

Ja pots accedir a http://localhost:8000!

## 🚀 DEPLOYMENT AUTOMÀTIC AL VPS

### Opció 1: Instal·lació Automàtica amb Docker (Recomanada)

```bash
# Una sola comanda ho fa tot (instal·la Docker + CoopConsum + configuració)
curl -sSL https://github.com/fosc19/coopconsum/raw/master/install_docker.sh | bash
```

### Opció 2: Despliegue a VPS existent

Si ja tens un VPS amb Docker configurat:

```bash
# Clona el repositori
git clone https://github.com/fosc19/coopconsum.git
cd coopconsum

# Configura variables d'entorn
cp .env.example .env
# Edita .env amb les teves configuracions

# Llança els contenidors
docker compose up -d

# Accedeix a http://LA_TEVA_IP/admin/ 
# Usuari: admin | Contrasenya: cooperativa2025
```

## 🔧 Gestió amb Docker

### Verificar que tot funciona
```bash
# Veure l'estat dels contenidors
docker compose ps

# Veure logs del sistema
docker compose logs web

# Test de connectivitat
curl -I http://LA_TEVA_IP/  # Ha de retornar 200 OK
```

### Comandos de manteniment
```bash
# Actualitzar el codi
git pull origin master
docker compose down
docker compose build --no-cache  # Important per canvis de codi
docker compose up -d

# Migracions de base de dades
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Backup de base de dades
docker compose exec db pg_dump -U coopconsum_user coopconsum_db > backup.sql
```

### Comandos útiles para desarrollo

```bash
# Entorno de desarrollo
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Docker local
docker-compose up -d
docker-compose logs
docker-compose down

# VPS production (usa els scripts automatitzats de dalt)
./quick-deploy.sh  # Deploy complet
./diagnose-vps.sh  # Diagnòstic
```

## 📚 Documentació

### Estructura del Projecte

```
coopconsum/
├── socios/          # Gestió de socis i usuaris
├── pedidos/         # Sistema de comandes
├── web/             # Lloc web públic
├── api/             # API REST per cooperatives
├── templates/       # Plantilles HTML
├── static/          # Arxius CSS, JS, imatges
├── media/           # Arxius pujats per usuaris
└── coopconsum/      # Configuració principal
```

### API Pública

L'API permet a altres cooperatives accedir a informació pública:

- **Proveïdors**: `GET /api/proveedores/`
- **Productes**: `GET /api/productos/`
- **Categories**: `GET /api/categorias/`

Exemple d'ús:
```bash
# Obtenir llista de proveïdors
curl http://localhost:8000/api/proveedores/
curl http://57.129.134.84/api/proveedores/  # Exemple VPS

# Buscar productes ecològics
curl http://localhost:8000/api/productos/?search=ecològic
```

## 🛠️ Configuració

### Variables d'Entorn

Crea un arxiu `.env` o configura directament a `settings.py`:

```python
SECRET_KEY = 'la-teva-clau-secreta-aqui'
DEBUG = False  # Per producció
ALLOWED_HOSTS = ['57.129.134.84', 'localhost', 'el-teu-domini.cat']

# Base de dades (exemple PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopconsum_db',
        'USER': 'el_teu_usuari',
        'PASSWORD': 'la_teva_contrasenya',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### CORS per API

Per permetre accés des d'altres dominis:

```python
CORS_ALLOWED_ORIGINS = [
    "https://la-teva-cooperativa.cat",
    "https://altra-cooperativa.org",
]
```

## 🤝 Contribuir

Les contribucions són benvingudes! Si us plau:

1. Fes un fork del projecte
2. Crea una branca per la teva funcionalitat (`git checkout -b feature/nova-funcionalitat`)
3. Commit els teus canvis (`git commit -am 'Afegir nova funcionalitat'`)
4. Push a la branca (`git push origin feature/nova-funcionalitat`)
5. Obre un Pull Request

## 📄 Llicència

Aquest projecte està sota la Llicència MIT - veure l'arxiu [LICENSE](LICENSE) per més detalls.

## 🌱 Filosofia del Projecte

Aquest sistema neix de la necessitat de les cooperatives de consum de tenir eines digitals que respectin els seus valors:

- **Codi Obert**: Transparència total i possibilitat d'adaptació
- **Cooperació**: API per compartir informació entre cooperatives
- **Sostenibilitat**: Enfocament en productes locals i ecològics
- **Comunitat**: Desenvolupat per i per cooperatives

## 📞 Suport

- **Documentació**: [Wiki del projecte](https://github.com/fosc19/coopconsum/wiki)
- **Issues**: [Reportar problemes](https://github.com/fosc19/coopconsum/issues)
- **Discussions**: [Fòrum de la comunitat](https://github.com/fosc19/coopconsum/discussions)

## 🏆 Cooperatives que l'usen

- La Civada (Barcelona) - Cooperativa pionera en el desenvolupament

La teva cooperativa usa CoopConsum? Afegeix-te a la llista!

---

**Desenvolupat amb ❤️ per la comunitat cooperativa**
