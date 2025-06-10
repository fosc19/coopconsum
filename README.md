# 🤝 CoopConsum - Sistema de Gestió per Cooperatives

Sistema complet de gestió per cooperatives de consum responsable, desenvolupat amb Django. Inclou gestió de socis, comandes, proveïdors, productes i una API pública per compartir informació entre cooperatives.

## ✨ Característiques

- 👥 **Gestió de Socis**: Registre, perfils i administració de membres
- 📦 **Sistema de Comandes**: Comandes col·lectives
- 🏪 **Gestió de Proveïdors**: Catàleg de proveïdors locals i ecològics
- 🛒 **Catàleg de Productes**: Organització per categories amb preus
- 🌐 **Web Pública**: Lloc web amb informació i catàleg públic
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
git clone https://github.com/tu-usuario/coopconsum.git
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

## 🔧 Gestió amb Docker

### Verificar que tot funciona
```bash
# Veure l'estat dels contenidors
docker compose ps

# Veure logs del sistema
docker compose logs web

# Veure logs dels cron jobs
docker compose logs cron
```

### Verificar tasques automàtiques
```bash
# ❌ NO facis això (comando incorrecte):
cron -l  # Això donarà error de permisos

# ✅ SÍ fes això (comandos correctes):
# Verificar que el contenidor cron està funcionant
docker compose ps cron

# Veure els logs de les tasques automàtiques
docker compose logs cron

# Executar tasques manualment per provar
docker compose exec web python manage.py generar_pedidos
docker compose exec web python manage.py cerrar_pedidos
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

# Buscar productes ecològics
curl http://localhost:8000/api/productos/?search=ecològic
```

## 🛠️ Configuració

### Variables d'Entorn

Crea un arxiu `.env` o configura directament a `settings.py`:

```python
SECRET_KEY = 'la-teva-clau-secreta-aqui'
DEBUG = False  # Per producció
ALLOWED_HOSTS = ['el-teu-domini.cat']

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

- **Documentació**: [Wiki del projecte](https://github.com/tu-usuario/coopconsum/wiki)
- **Issues**: [Reportar problemes](https://github.com/tu-usuario/coopconsum/issues)
- **Discussions**: [Fòrum de la comunitat](https://github.com/tu-usuario/coopconsum/discussions)

## 🏆 Cooperatives que l'usen

- La Civada (Barcelona) - Cooperativa pionera en el desenvolupament

La teva cooperativa usa CoopConsum? Afegeix-te a la llista!

---

**Desenvolupat amb ❤️ per la comunitat cooperativa**
