# 🔧 Manual Tècnic d'Administració - CoopConsum

## 📋 Documentació Tècnica per Administradors

### 🛠️ Informació del Sistema

**Versió**: Django 5.1.6 + PostgreSQL + Docker  
**Repositori**: https://github.com/fosc19/coopconsum  
**VPS**: 57.129.134.84  
**Admin URL**: http://57.129.134.84/admin/

### 🔐 Credencials per Defecte

**Primera instal·lació**:
- **Usuari**: `admin`
- **Contrasenya**: `cooperativa2025`
- **Email**: `admin@cooperativa.local`

⚠️ **CANVIA LA CONTRASENYA** immediatament després del primer accés!

### 🐳 Gestió Docker al VPS

#### Comandes Essencials
```bash
# Estat dels contenidors
docker compose ps

# Logs de l'aplicació
docker compose logs -f web

# Reinici complet (SEMPRE necessari per canvis de codi)
docker compose down
docker compose build --no-cache
docker compose up -d

# Accés al contenidor web
docker exec -it coopconsum-web-1 bash

# Migració de base de dades
docker exec coopconsum-web-1 python manage.py migrate

# Crear superusuari
docker exec -it coopconsum-web-1 python manage.py createsuperuser
```

#### ⚠️ REGLA CRÍTICA: Cache Docker
Per **QUALSEVOL** canvi (CSS, Python, templates):
```bash
cd /var/www/coopconsum
git pull origin master
docker compose down
docker compose build --no-cache  # SEMPRE --no-cache
docker compose up -d
```

### 📊 Base de Dades

#### Backup Automàtic
- **Horari**: Cada dia a les 02:00
- **Localització**: Contenidor `db`
- **Retenció**: 7 dies

#### Backup Manual
```bash
docker exec coopconsum-db-1 pg_dump -U coopconsum coopconsum > backup_$(date +%Y%m%d).sql
```

### 🔄 Tasques Automàtiques (Cron)

#### Horaris del Sistema
- **23:58**: Generar noves comandes recurrents
- **23:59**: Tancar comandes del dia
- **02:00**: Backup automàtic de base de dades

#### Verificar Cron Jobs
```bash
docker exec coopconsum-cron-1 crontab -l
docker exec coopconsum-cron-1 ls -la /var/log/cron/
```

### 🗂️ Estructura de Fitxers

#### Directoris Importants
```
/var/www/coopconsum/
├── media/           # Fitxers pujats pels usuaris
├── static/          # Fitxers estàtics (CSS, JS, imatges)
├── templates/       # Templates HTML
├── docs/           # Documentació
└── logs/           # Logs de l'aplicació
```

#### Gestió de Media Files
```bash
# Verificar espai disc
df -h /var/www/coopconsum/media/

# Llistar fitxers grossos
find /var/www/coopconsum/media/ -size +10M -ls

# Permisos correctes
chown -R 1000:1000 /var/www/coopconsum/media/
```

### 🔍 Monitorització i Logs

#### Logs del Sistema
```bash
# Logs aplicació Django
docker compose logs -f web

# Logs base de dades
docker compose logs -f db

# Logs nginx (si està actiu)
docker compose logs -f nginx

# Logs sistema VPS
sudo journalctl -f
```

#### Indicadors de Salut
- **Memòria**: `free -h`
- **Disc**: `df -h`
- **CPU**: `htop`
- **Contenidors**: `docker ps`

### 🛠️ Resolució de Problemes

#### Error 500 - Pàgines no carreguen
1. Comprovar logs: `docker compose logs web`
2. Verificar migracions: `docker exec coopconsum-web-1 python manage.py showmigrations`
3. Comprovar ConfiguracioWeb: `docker exec coopconsum-web-1 python manage.py shell`

#### Base de Dades No Connecta
1. Verificar contenidor: `docker compose ps db`
2. Comprovar logs: `docker compose logs db`
3. Reiniciar servei: `docker compose restart db`

#### Fitxers Media No Es Veuen
1. Verificar permisos: `ls -la /var/www/coopconsum/media/`
2. Comprovar volum Docker: `docker volume ls`
3. Test d'accés: `curl -I http://57.129.134.84/media/test.jpg`

#### Comandes No Es Generen
1. Verificar cron: `docker compose logs cron`
2. Comprovar dates: Solapament entre comandes setmanals
3. Revisar comandes recurrents: Data de finalització buida

### 🔐 Seguretat

#### Credencials Segures
- Canviar contrasenyes per defecte
- Utilitzar contrasenyes fortes (>12 caràcters)
- Activar 2FA si es requereix

#### Backup i Recuperació
- Backup diari automàtic
- Test de restauració mensual
- Còpies externes recomanades

#### Actualitzacions
- Revisar updates de Django mensuals
- Actualitzar imatges Docker trimestrals
- Monitoritzar vulnerabilitats conegudes

### 📞 Contacte i Suport

#### Suport Tècnic
- **Email**: civada@gmail.com
- **GitHub Issues**: https://github.com/fosc19/coopconsum/issues

#### Documentació Addicional
- **Manual d'usuari**: `/docs/MANUAL_USUARI.md`
- **Guia Docker**: `/docs/DOCKER_README.md`
- **API Documentació**: `/docs/API_COOPERATIVAS.md`

#### Informació del Sistema
- **Versió Django**: 5.1.6
- **Versió Python**: 3.12
- **Versió PostgreSQL**: 15
- **Versió Bootstrap**: 5.3.0

---

*Manual actualitzat per la versió actual de CoopConsum*  
*Per suggeriments de millora, contacta amb l'equip tècnic*