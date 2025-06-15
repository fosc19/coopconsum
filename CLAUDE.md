# Projecte CoopConsum - Documentació Completa

## Resumen Ejecutivo

Sistema Django de gestió per cooperatives de consum responsable. Projecte principal **coopconsum** (genèric) amb instància específica de referència **lacivada**.

## Notas Importantes

⚠️ **Política de Commits**: No incluir marcas de agua automáticas en los commits. Los commits deben contener únicamente información relevante del proyecto sin referencias externas.

## 📍 Informació del servidor VPS
- **IP**: 57.129.134.84
- **Ubicació aplicació**: /var/www/coopconsum
- **Claude Code disponible**: Sí, es pot usar per diagnosticar problemes i executar comandes
- **Docker compose**: Gestiona contenidors web, db i cron

## 🔑 CREDENCIALS PER DEFECTE

### Accés admin automàtic
Quan s'executa Docker per primera vegada, es crea automàticament:
- **Usuari**: `admin`
- **Contrasenya**: `cooperativa2025`
- **Email**: `admin@cooperativa.local`
- **URL**: `http://57.129.134.84/admin/`

🔒 **IMPORTANT**: Canvia la contrasenya immediatament:
1. Accedeix a `/admin/`
2. Inicia sessió amb credencials anteriors  
3. Ves a "Usuaris" > "admin"
4. Canvia la contrasenya per una de segura

## Configuració logout
- **Admin logout**: `/admin/logout/` → redirigeix a `/admin/`
- **Intranet logout**: `/sortir/` → redirigeix a `/` (web pública)

## 🔐 CONFIGURACIÓ SSH CRÍTICA

### Clau SSH que funciona
- **Clau correcta**: `/tmp/claude_new_key` 
- **Usuari**: `ubuntu` (NO root!)
- **IP**: `57.129.134.84`

### Connexió SSH
```bash
# SEMPRE utilitzar aquesta clau específica
ssh -i /tmp/claude_new_key ubuntu@57.129.134.84

# Si la clau no existeix o dóna error "libcrypto":
ssh-keygen -t rsa -b 2048 -m PEM -f /tmp/claude_new_key -N ""
# Després cal afegir la clau pública al servidor via consola web
```

### ⚠️ PROBLEMES COMUNS SSH
- **Error "libcrypto"**: Clau en format OPENSSH, cal regenerar en format PEM
- **Permission denied**: Clau pública no està al servidor 
- **Clau incorrecta**: NO usar /tmp/claude_ssh_key ni /tmp/ssh_private_key (corruptes)

## 🐳 DOCKER TROUBLESHOOTING

### Problemes recurrents i solucions

#### 1. Imatges Docker amb codi antic
**Problema**: Els canvis de codi no es reflecteixen tot i haver fet git pull
**Solució**: Reconstruir amb --no-cache
```bash
ssh -i /tmp/claude_new_key ubuntu@57.129.134.84
cd /var/www/coopconsum
docker compose down
docker compose build --no-cache  # ⚠️ OBLIGATORI després de canvis de codi
docker compose up -d
```

#### 2. Media files retornen 404
**Problema**: Fitxers pujats via admin no es mostren a la web
**Causa**: Volum media no muntat correctament o fitxers no copiats
**Solució**:
```bash
# Verificar directori media dins contenidor
docker exec coopconsum-web-1 ls -la /app/media/

# Crear directoris si no existeixen
docker exec coopconsum-web-1 mkdir -p /app/media/galeria

# Copiar fitxers des del host si cal
docker cp galeria/cistella.jpg coopconsum-web-1:/app/media/galeria/

# Test d'accés
curl -I http://57.129.134.84/media/galeria/cistella.jpg
```

#### 3. Base de dades no sincronitzada
**Problema**: Migrations no aplicades després de canvis de models
**⚠️ CRÍTIC**: Pot causar error 500 si el codi espera columnes que no existeixen

**Diagnòstic**:
```bash
# Verificar si hi ha migracions pendents
docker exec coopconsum-web-1 python manage.py showmigrations --plan

# Test ràpid del model principal
docker exec coopconsum-web-1 python manage.py shell -c "from web.models import ConfiguracioWeb; print(ConfiguracioWeb.objects.first())"
```

**Solució**:
```bash
# Crear migracions si hi ha canvis de models
docker exec coopconsum-web-1 python manage.py makemigrations

# Aplicar migracions
docker exec coopconsum-web-1 python manage.py migrate

# Si falla, possiblement cal fake + manual:
# docker exec coopconsum-web-1 python manage.py migrate app_name migration_number --fake
# docker exec coopconsum-db-1 psql -U cooperativa_user -d cooperativa_db -c "ALTER TABLE..."

docker compose restart web
```

## 🚀 SCRIPTS D'AUTOMATITZACIÓ

### Scripts disponibles per deployment
```bash
# Deploy automàtic complet (git push + docker rebuild + migrations)
./quick-deploy.sh

# Diagnòstic complet de problemes VPS
./diagnose-vps.sh

# Connexió SSH directa
ssh -i /tmp/claude_new_key ubuntu@57.129.134.84
```

### Què fan els scripts:
- **quick-deploy.sh**: Push a git → rebuild Docker → migrations → restart
- **diagnose-vps.sh**: Verifica SSH, Docker, DB, logs i connectivity

## Comandaments útils per VPS
```bash
cd /var/www/coopconsum
git pull origin master
docker compose restart
docker compose logs web --tail 20
curl -I http://57.129.134.84/sortir/

# Diagnòstic complet
docker compose ps
docker exec coopconsum-web-1 python manage.py check
docker exec coopconsum-web-1 ls -la /app/media/
```

## 🔄 WORKFLOW GIT AMB ACCÉS LOCAL + VPS

### ⚠️ CRITICAL WORKFLOW CHECKPOINTS

**PROBLEMA IDENTIFICAT**: Es poden fer canvis locals però oblidar el push, causant que el VPS tingui versió antiga.

**PROTOCOL OBLIGATORI**:
1. ✅ **SEMPRE** verificar què està al repositori abans que el VPS descarregui
2. ✅ **COMMIT + PUSH immediatament** després de fer canvis
3. ✅ **VERIFICAR al repositori** que els canvis són visibles abans de testar al VPS

### Workflow recomanat: Local → Git → VPS
```bash
# 1. LOCAL: Fer tots els canvis aquí
edit files...
git add -A
git commit -m "descripcio"

# ⚠️ OBLIGATORI: VERIFICAR QUE EL PUSH ES FA
git push origin master
echo "✅ PUSH COMPLETAT - els canvis són al repositori"

# ⚠️ VERIFICACIÓ FINAL: Confirmar que GitHub té els canvis
git log --oneline -1  # mostrar últim commit local
git ls-remote origin master  # verificar que remote té mateix commit

# 2. VPS: Actualitzar i provar (només després del push verificat)
ssh -i /tmp/claude_new_key ubuntu@57.129.134.84
cd /var/www/coopconsum
git reset --hard origin/master  # Descartar canvis locals VPS
git pull origin master

# ⚠️ OBLIGATORI DESPRÉS DE GIT PULL:
docker compose down
docker compose build --no-cache  # Rebuild si hi ha canvis de codi
docker compose up -d

# ⚠️ VERIFICAR MIGRACIONS DESPRÉS DE REBUILD:
docker exec coopconsum-web-1 python manage.py showmigrations --plan
docker exec coopconsum-web-1 python manage.py makemigrations
docker exec coopconsum-web-1 python manage.py migrate

# ⚠️ TEST CRÍTIC ABANS DE DECLARAR ÈXIT:
curl -I http://57.129.134.84/  # Ha de retornar 200 OK
curl -I http://57.129.134.84/admin/  # Ha de retornar 302 Found
docker exec coopconsum-web-1 python manage.py shell -c "from web.models import ConfiguracioWeb; print('DB OK:', ConfiguracioWeb.objects.first().nom_cooperativa)"
```

### CHECKLIST ABANS DE TESTING AL VPS:
- [ ] Commits locals fets
- [ ] Push executat sense errors  
- [ ] Verificat que GitHub mostra els últims canvis
- [ ] Només llavors → actualitzar VPS

### CHECKLIST DESPRÉS D'ACTUALITZAR VPS:
- [ ] `git pull` executat correctament
- [ ] `docker compose build --no-cache` completat
- [ ] `docker compose up -d` executat
- [ ] **CRÍTIC**: Migracions verificades i aplicades
- [ ] **CRÍTIC**: Test web principal retorna 200 OK
- [ ] **CRÍTIC**: Test admin retorna 302 Found  
- [ ] **CRÍTIC**: Model ConfiguracioWeb funciona sense errors
- [ ] Només llavors → declarar desplegament exitós

### 🛡️ EINA DE SEGURETAT: Script de verificació automàtica

```bash
# Utilitzar SEMPRE abans de fer push
cd /home/fosca/proyectos/coopconsum
./pre-push-check.sh
```

**Què fa aquest script:**
- ✅ Verifica que no hi ha canvis sense comittejar
- ✅ Mostra exactament què es pujarà
- ✅ Identifica fitxers crítics modificats (docker-entrypoint.sh, install_docker.sh, etc.)
- ✅ Fa el push i verifica sincronització
- ✅ Suggereix passos següents si hi ha canvis crítics

**REGLA D'OR: Mai fer `git push` directament. Sempre utilitzar `./pre-push-check.sh`**

### En cas d'emergència: Sincronitzar canvis del VPS
```bash
# 1. VPS: Pujar canvis temporals
git add . && git commit -m "temp VPS changes"

# 2. LOCAL: Baixar, netejar i arreglar
git pull origin master  # pot tenir conflictes
# resoldre conflictes o fer reset si cal
git add -A && git commit -m "fix proper"
git push origin master

# 3. VPS: Actualitzar net
git reset --hard origin/master
docker compose restart
```

## 🎨 SISTEMA DE CONFIGURACIÓ WEB DINÀMICA

### Funcionalitat ConfiguracioWeb
Sistema implementat per permetre edició no-tècnica del contingut web via admin Django.

#### Pàgines editables:
- **Pàgina d'inici**: Hero, característiques, call-to-action
- **Qui som**: Introducció, cistella, altres productes, ubicació  
- **Com apuntar-se**: Compromís, comissions, formalització
- **Contacte**: Títols, dades de contacte

#### Admin organitzat per pàgines:
- 🏢 **Informació General**
- 🏠 **PÀGINA D'INICI** (4 seccions)
- 👥 **PÀGINA "QUI SOM"** (4 seccions)
- 📝 **PÀGINA "COM APUNTAR-SE"** (4 seccions)
- 📞 **PÀGINA "CONTACTE"** (2 seccions)

#### Substitució automàtica:
- Usar `{nom_cooperativa}` en textos per substitució automàtica
- Suport HTML segur per enllaços amb `|safe`
- Formatat automàtic de paràgrafs amb `linebreaksbr`

#### Context processor:
```python
# web/context_processors.py
def configuracio_web(request):
    config = ConfiguracioWeb.objects.first()
    return {'config': config}
```

### URLs pàgines:
```
/                    # Pàgina principal
/qui-som/           # Qui som
/com-apuntar-se/    # Com apuntar-se  
/contacte/          # Contacte
/admin/             # Admin per editar contingut
```

## 🗂️ ESTRUCTURA DEL PROJECTE

### Apps Principales
| App | Propósito | Models Principals |
|-----|-----------|-------------------|
| **socios** | Gestión de miembros | `Socio`, `CuentaSocio`, `MovimientoCuenta` |
| **productos** | Catálogo y proveedores | `Producto`, `Categoria`, `Proveedor` |
| **pedidos** | Sistema comandas colectivas | `PedidoColectivo`, `ComandaRecurrente` |
| **stock** | Gestión inventario | `StockLocal`, `MovimientoStock` |
| **web** | Sitio web público + ConfiguracioWeb | `ConfiguracioWeb`, `GaleriaImagen` |
| **desitjos** | Sistema "cartas deseo" | `CartaDeseo`, `InteresSocioEnCarta` |
| **eventos** | Calendario eventos | `EventoCalendario` |

### Context Processors Actius
```python
# settings_base.py TEMPLATES.context_processors
'pedidos.context_processors.pedidos_info_processor',  # Info pedidos global
'stock.context_processors.registros_compra_pendientes_processor',  # Compras pendientes  
'web.context_processors.configuracio_web',  # ⭐ ConfiguracioWeb dinàmica
```

### Dependències principals
```python
Django==5.1.6
django-adminlte3==0.1.6           # Tema admin
djangorestframework==3.16.0       # API REST
django-cors-headers==4.3.1        # CORS para API
psycopg2-binary==2.9.10          # PostgreSQL
pillow==11.1.0                    # Imatges
whitenoise==6.6.0                 # Fitxers estàtics
gunicorn==21.2.0                  # Servidor WSGI
```

## ⏰ CRON JOBS AUTOMÀTICS

### Horaris configurats al VPS
Els cron jobs s'executen automàticament cada dia:
- **23:58** - Generar noves comandes recurrents 
- **23:59** - Tancar comandes del dia
- **02:00** - Backup diari de la base de dades
- **03:00** - Neteja de logs (setmanal)

### Verificar cron jobs
```bash
# Veure cron jobs configurats
crontab -l

# Veure logs de les tasques automàtiques  
tail -f /var/log/coopconsum_cron.log

# Verificar que contenidors responen
docker compose exec web python manage.py help | grep -E '(generar_pedidos|cerrar_pedidos)'
```

## 🔧 COMANDOS DE GESTIÓ

### Comandos automatizados (cronjobs)
```bash
# management/commands/ en app pedidos
docker exec coopconsum-web-1 python manage.py cerrar_pedidos     # Cierre automático
docker exec coopconsum-web-1 python manage.py generar_pedidos    # Generación automática

# Execució manual per testing
docker exec coopconsum-web-1 python manage.py generar_pedidos_test
```

### Testing local
```bash
python manage.py runserver 8000
python manage.py shell
python manage.py makemigrations
python manage.py migrate
```

### Verificacions de salut
```bash
# Dins del contenidor
docker exec coopconsum-web-1 python manage.py check
docker exec coopconsum-web-1 python manage.py showmigrations

# Estat general
docker compose ps
docker compose logs web --tail 20
```

## 🌐 VARIABLES D'ENTORN ESSENCIALS

### Arxiu .env per Docker
```bash
# Configuració crítica per seguretat
DJANGO_SECRET_KEY=kVg+uJuoW9)Nd+KE4lr6maWY-aRePTmT8CQ4gO4FVTQ3Z&Rz)b
DEBUG=False
POSTGRES_DB=coopconsum_db  
POSTGRES_USER=coopconsum_user
POSTGRES_PASSWORD=$2jxTDreU4UBuoLD$g@v
ALLOWED_HOSTS=57.129.134.84,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://57.129.134.84,http://localhost,http://127.0.0.1
CSRF_TRUSTED_ORIGINS=http://57.129.134.84,http://localhost,http://127.0.0.1
COOP_NAME=La Civada
COOP_EMAIL=info@lacivada.org
```

### Verificar variables carregades
```bash
# Comprovar variables dins del contenidor
docker compose exec web env | grep -E "(SECRET|PASSWORD|DEBUG)"
```

## 📱 API REST PÚBLICA

### Estat actual: ✅ FUNCIONANT
L'API està operativa amb dades de prova:
- **4 proveïdors**: Aresta, Complet, La Rural, Pollatre Moli
- **7 productes**: Pa (5), Pollastre (1), altres
- **3 categories**: Pa, Alvocats, Pollastre

### Endpoints principals
```
GET /api/proveedores/     # Lista proveedores públicos
GET /api/productos/       # Lista productos con filtros  
GET /api/categorias/      # Lista categorías
GET /api/eventos/         # Lista eventos calendario
```

### Exemples d'ús
```bash
# Obtenir proveïdors visibles
curl "http://57.129.134.84/api/proveedores/?visible_en_web=true"

# Buscar productes destacats
curl "http://57.129.134.84/api/productos/?destacado_en_inicio=true"
```

### Configuración CORS
Permite intercambio entre cooperativas configurando dominis a `settings_base.py`.

## 🚀 DESPLEGAMENT I ACTUALITZACIONS

### Workflow desplegament
1. **Desenvolupament local** amb configuració de test
2. **Push a GitHub** amb verificació
3. **Actualització VPS** amb git pull + Docker rebuild
4. **Verificació funcionament** de totes les URLs

### Backups automàtics (referència lacivada)
- **Base de dades**: Backup diari PostgreSQL
- **Media files**: Sincronització fitxers pujats
- **Codi**: Git com a backup automàtic

## 🔍 TROUBLESHOOTING COMÚ

### Error 500 en pàgines
**Causa més freqüent**: Base de dades dessincronitzada amb el codi

**Diagnòstic ràpid**:
```bash
# Test del model principal
docker exec coopconsum-web-1 python manage.py shell -c "from web.models import ConfiguracioWeb; print(ConfiguracioWeb.objects.first())"

# Si error "column does not exist" → problema de migració
docker exec coopconsum-web-1 python manage.py showmigrations --plan
```

**Solucions per ordre de prioritat**:
1. Verificar context processor `configuracio_web` actiu
2. **CRÍTIC**: Comprovar migracions amb `showmigrations --plan`
3. Aplicar migracions pendents amb `makemigrations` + `migrate`
4. Comprovar que existeix `ConfiguracioWeb.objects.first()`
5. Revisar templates per filtres Django vàlids (no usar `split`)

### Media files 404
1. Verificar volum Docker media muntat
2. Comprovar permisos directoris
3. Test directe: `curl -I http://IP/media/path/file.jpg`

### Docker cache problems
```bash
# Reset complet
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 🔒 VERIFICACIONS DE SEGURETAT

### Comandos per verificar configuració
```bash
# Verificar dependencies actualitzades
pip-audit --requirement requirements.txt

# Verificar configuració Django segura
python manage.py check --deploy

# Verificar Docker configurat correctament
docker compose config --quiet && echo "Configuració vàlida"
```

### ⚠️ PROBLEMA COMÚ: Migració fake sense columna real
**Què passa**: Migració marcada com a aplicada però la columna no existeix a la BD
**Error típic**: `column "logo_principal" does not exist`

**Solució d'emergència**:
```bash
# Afegir columna manualment a la BD
docker exec coopconsum-db-1 psql -U cooperativa_user -d cooperativa_db -c "ALTER TABLE web_configuracioweb ADD COLUMN logo_principal VARCHAR(100);"

# Verificar que funciona
docker exec coopconsum-web-1 python manage.py shell -c "from web.models import ConfiguracioWeb; print('Fix OK:', ConfiguracioWeb.objects.first().nom_cooperativa)"
```

**Prevenció**: Sempre seguir el workflow complet amb verificacions de BD

### Referències documentació especialitzada
- **API completa**: `docs/API_COOPERATIVAS.md`
- **Auditoria seguretat**: `AUDITORIA_SEGURETAT_DETALLADA.md`
- **Estratègia backup**: `BACKUP_STRATEGY_TODO.md`
- **GitHub públic**: `docs/GUIA_GITHUB_PUBLICO.md`

## 📚 DOCUMENTACIÓ DE REFERÈNCIA

### Projectes relacionats
- **coopconsum**: Projecte principal (aquest)
- **lacivada**: Instància específica amb configuració avançada (referència)

### Fitxers de configuració clau
- `settings_base.py`: Configuració Django principal
- `docker-compose.yml`: Configuració contenidors
- `requirements.txt`: Dependències Python
- `web/context_processors.py`: Context processor ConfiguracioWeb

Aquest document centralitza tota la informació necessària per treballar amb el projecte CoopConsum.