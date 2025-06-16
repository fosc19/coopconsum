# Docker Setup - CoopConsum

## Fitxers Docker creats

- `Dockerfile` - Imatge Django personalitzada
- `docker-compose.yml` - Orquestració de serveis
- `docker-entrypoint.sh` - Script d'inicialització
- `.env` - Variables d'entorn
- `nginx/nginx.conf` - Configuració Nginx
- `coopconsum/local_settings_docker.py` - Settings per Docker
- `.dockerignore` - Fitxers a ignorar

## Serveis inclosos

- **db**: PostgreSQL 15 amb volum persistent
- **web**: Django + Gunicorn
- **nginx**: Proxy invers i fitxers estàtics

## Migració gradual

### 1. Provar Docker (sense afectar el sistema actual)
```bash
# Construir imatges
docker compose build

# Llançar només la base de dades per provar
docker compose up db -d

# Verificar que funciona
docker compose ps
```

### 2. Migració completa (quan estiguis llest)
```bash
# Aturar serveis actuals
sudo systemctl stop nginx
sudo systemctl stop gunicorn

# Backup de dades
pg_dump coopconsum_db > backup_pre_docker.sql

# Llançar Docker
docker compose up -d

# Verificar logs
docker compose logs -f
```

### 3. Rollback (si cal)
```bash
# Aturar Docker
docker compose down

# Restaurar serveis
sudo systemctl start gunicorn
sudo systemctl start nginx
```

## Gestió diària

```bash
# Veure estat
docker compose ps

# Logs
docker compose logs -f web

# Actualitzar codi
git pull origin master
docker compose restart web

# Migracions
docker compose exec web python manage.py migrate

# Backup
docker compose exec db pg_dump -U coopconsum_user coopconsum_db > backup.sql
```

## Avantatges

- ✅ Entorn aïllat i reproducible
- ✅ Fàcil escalabilitat
- ✅ Backup i restore senzill
- ✅ Actualitzacions sense downtime
- ✅ Monitorització integrada

## Credencials per defecte

Quan s'executa per primera vegada, el sistema crea automàticament un usuari administrador:

- **Usuari**: `admin`
- **Contrasenya**: `cooperativa2025`
- **Email**: `admin@cooperativa.local`

🔒 **IMPORTANT**: Canvia la contrasenya immediatament després del primer accés!

1. Accedeix a `/admin/`
2. Inicia sessió amb les credencials anteriors
3. Ves a "Usuaris" > "admin"
4. Canvia la contrasenya per una de segura

## Notes importants

- Les dades es guarden en volums Docker persistents
- La configuració actual es manté intacta
- Pots tornar al sistema anterior en qualsevol moment
- SSL/HTTPS es pot afegir més tard
- L'usuari administrador es crea automàticament només si no existeix cap superusuari

## Configuració de Cron Jobs (Comandes Recurrents)

Per activar la gestió automàtica de comandes recurrents, cal configurar els cron jobs al sistema host (fora dels contenidors Docker):

### 1. Instal·lar cron jobs
```bash
# Els cron jobs s'han de configurar manualment o usar el script d'instal·lació automàtica
# Consulta el fitxer install_docker.sh per veure com es configuren automàticament

# Verificar instal·lació
crontab -l
```

### 2. Funcionament automàtic
Els cron jobs executaran diàriament:

- **23:58** - Generar noves comandes recurrents
- **23:59** - Tancar comandes del dia
- **02:00** - Backup diari de la base de dades
- **03:00** - Neteja de logs (setmanal)

### 3. Logs de cron jobs
```bash
# Veure logs dels cron jobs
tail -f /var/log/coopconsum_docker_cron.log

# Verificar que els contenidors responen
docker compose exec web python manage.py help | grep -E '(generar_pedidos|cerrar_pedidos)'
```

### 4. Execució manual (per provar)
```bash
# Generar comandes manualment
docker compose exec web python manage.py generar_pedidos

# Tancar comandes manualment
docker compose exec web python manage.py cerrar_pedidos
```

**Important**: Els cron jobs són essencials per al funcionament de les comandes recurrents. Sense ells, les comandes no es generaran ni tancaran automàticament.
