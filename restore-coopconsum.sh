#!/bin/bash

# Script de restore complet per CoopConsum
# Restaura backup de BD, media files i configuració
# Ús: ./restore-coopconsum.sh [arxiu_backup.tar.gz]

set -e

# Colors per a la sortida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funció per mostrar missatges
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVÍS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo ""
    echo -e "${BLUE}==== $1 ====${NC}"
    echo ""
}

# Verificar paràmetres
if [ $# -eq 0 ]; then
    echo "🔄 Restore Complet CoopConsum"
    echo "============================="
    echo ""
    print_error "Cal especificar l'arxiu de backup"
    echo ""
    echo "Ús: $0 [arxiu_backup.tar.gz]"
    echo ""
    echo "Exemples:"
    echo "  $0 ./backups/coopconsum_backup_20250618_143022.tar.gz"
    echo "  $0 /path/to/backup.tar.gz"
    echo ""
    echo "📁 Backups disponibles:"
    find . -name "coopconsum_backup_*.tar.gz" -exec ls -lh {} \; 2>/dev/null | head -5 || echo "  No hi ha backups al directori actual"
    exit 1
fi

BACKUP_FILE="$1"

# Verificar que l'arxiu de backup existeix
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "Arxiu de backup no trobat: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Restore Complet CoopConsum"
echo "============================="
echo ""
print_status "Arxiu backup: $BACKUP_FILE"
print_status "Mida: $(du -h "$BACKUP_FILE" | cut -f1)"
echo ""

# Verificar que s'executa des del directori correcte
if [ ! -f "manage.py" ] || [ ! -f "docker-compose.yml" ]; then
    print_error "Aquest script s'ha d'executar des del directori arrel de CoopConsum"
    print_status "Directori actual: $(pwd)"
    exit 1
fi

# ADVERTÈNCIA DE SEGURETAT
print_section "ADVERTÈNCIA DE SEGURETAT"
print_warning "⚠️ ATENCIÓ: Aquest procés sobreescriurà les dades actuals"
echo ""
echo "El restore eliminarà:"
echo "  • Totes les dades de la base de dades actual"
echo "  • Tots els media files actuals"
echo "  • Algunes configuracions"
echo ""
echo "Assegura't de tenir un backup de les dades actuals si són importants!"
echo ""

read -p "Confirma que vols continuar amb el restore [y/N]: " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Restore cancel·lat per l'usuari"
    exit 0
fi

# 1. PREPARACIÓ
print_section "PREPARACIÓ RESTORE"

# Crear directori temporal per extreure backup
TEMP_DIR="/tmp/coopconsum_restore_$$"
mkdir -p "$TEMP_DIR"
print_status "Directori temporal creat: $TEMP_DIR"

# Extreure backup
print_status "Extraient arxiu de backup..."
cd "$TEMP_DIR"
if tar -xzf "$BACKUP_FILE"; then
    print_success "✅ Backup extret correctament"
else
    print_error "❌ Error extraient el backup"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Buscar directori del backup
BACKUP_CONTENT_DIR=$(find . -maxdepth 1 -type d -name "coopconsum_backup_*" | head -1)
if [ -z "$BACKUP_CONTENT_DIR" ]; then
    print_error "❌ Estructura de backup no vàlida"
    rm -rf "$TEMP_DIR"
    exit 1
fi

cd "$BACKUP_CONTENT_DIR"
print_success "✅ Contingut backup trobat: $BACKUP_CONTENT_DIR"

# Verificar contingut del backup
print_status "Verificant contingut del backup..."
if [ -f "database.sql" ]; then
    print_success "  ✓ Base de dades trobada"
else
    print_error "  ❌ Base de dades no trobada"
    rm -rf "$TEMP_DIR"
    exit 1
fi

if [ -d "media" ] || [ -f "media_files.tar.gz" ]; then
    print_success "  ✓ Media files trobats"
else
    print_warning "  ⚠️ Media files no trobats"
fi

if [ -d "config" ]; then
    print_success "  ✓ Configuració trobada"
else
    print_warning "  ⚠️ Configuració no trobada"
fi

# Tornar al directori original
cd - >/dev/null

# 2. ATURAR SERVEIS
print_section "ATURANT SERVEIS"

print_status "Aturant contenidors Docker..."
if docker compose down; then
    print_success "✅ Contenidors aturats"
else
    print_warning "⚠️ Alguns contenidors poden no s'haver aturat correctament"
fi

# 3. RESTORE BASE DE DADES
print_section "RESTORE BASE DE DADES"

print_status "Iniciant només el servei de base de dades..."
if docker compose up -d db; then
    print_success "✅ Servei BD iniciat"
else
    print_error "❌ No es pot iniciar el servei de BD"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Esperar que la BD estigui llesta
print_status "Esperant que la base de dades estigui llesta..."
sleep 10
MAX_ATTEMPTS=30
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    if docker compose exec -T db pg_isready 2>/dev/null; then
        print_success "✅ Base de dades llesta"
        break
    fi
    print_status "Intent $ATTEMPT/$MAX_ATTEMPTS - esperant BD..."
    sleep 2
    ATTEMPT=$((ATTEMPT + 1))
done

if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
    print_error "❌ La base de dades no respon"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Carregar variables d'entorn
if [ -f "$TEMP_DIR/$BACKUP_CONTENT_DIR/config/.env" ]; then
    print_status "Carregant variables d'entorn del backup..."
    export $(grep -v '^#' "$TEMP_DIR/$BACKUP_CONTENT_DIR/config/.env" | xargs)
elif [ -f ".env" ]; then
    print_status "Carregant variables d'entorn actuals..."
    export $(grep -v '^#' .env | xargs)
else
    print_warning "No es troben variables d'entorn, usant valors per defecte"
    POSTGRES_DB=${POSTGRES_DB:-coopconsum_db}
    POSTGRES_USER=${POSTGRES_USER:-coopconsum_user}
fi

# Eliminar base de dades existent i crear-ne una de nova
print_status "Recreant base de dades..."
docker compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
docker compose exec -T db psql -U postgres -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"
print_success "✅ Base de dades recreada"

# Restaurar backup de la BD
print_status "Restaurant backup de la base de dades..."
if docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$TEMP_DIR/$BACKUP_CONTENT_DIR/database.sql"; then
    print_success "✅ Base de dades restaurada correctament"
else
    print_error "❌ Error restaurant la base de dades"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 4. RESTORE MEDIA FILES
print_section "RESTORE MEDIA FILES"

print_status "Iniciant contenidor web temporalment per restore media..."
docker compose up -d web
sleep 15

# Netejar media actuals
print_status "Netejant media files actuals..."
docker compose exec -T web rm -rf /app/media/* 2>/dev/null || true

# Restaurar media files
if [ -f "$TEMP_DIR/$BACKUP_CONTENT_DIR/media_files.tar.gz" ]; then
    print_status "Restaurant media files des de l'arxiu comprimit..."
    docker compose cp "$TEMP_DIR/$BACKUP_CONTENT_DIR/media_files.tar.gz" web:/tmp/
    docker compose exec -T web tar -xzf /tmp/media_files.tar.gz -C /app/
    docker compose exec -T web rm -f /tmp/media_files.tar.gz
    print_success "✅ Media files restaurats des de l'arxiu"
elif [ -d "$TEMP_DIR/$BACKUP_CONTENT_DIR/media" ]; then
    print_status "Restaurant media files des del directori..."
    docker compose cp "$TEMP_DIR/$BACKUP_CONTENT_DIR/media/." web:/app/media/
    print_success "✅ Media files restaurats des del directori"
else
    print_warning "⚠️ No hi ha media files per restaurar"
fi

# Verificar media files
MEDIA_COUNT=$(docker compose exec -T web find /app/media -type f 2>/dev/null | wc -l || echo "0")
print_status "Media files restaurats: $MEDIA_COUNT fitxers"

# 5. RESTORE CONFIGURACIÓ
print_section "RESTORE CONFIGURACIÓ"

if [ -d "$TEMP_DIR/$BACKUP_CONTENT_DIR/config" ]; then
    print_status "Restaurant fitxers de configuració..."
    
    # Llista de fitxers de configuració per restaurar
    CONFIG_FILES=(".env" "docker-compose.yml")
    
    for file in "${CONFIG_FILES[@]}"; do
        if [ -f "$TEMP_DIR/$BACKUP_CONTENT_DIR/config/$file" ]; then
            # Fer backup de la configuració actual
            if [ -f "$file" ]; then
                cp "$file" "$file.backup.$(date +%Y%m%d_%H%M%S)"
                print_status "Backup de $file creat"
            fi
            
            # Restaurar configuració
            cp "$TEMP_DIR/$BACKUP_CONTENT_DIR/config/$file" "$file"
            print_success "  ✓ $file restaurat"
        fi
    done
else
    print_warning "⚠️ No hi ha configuració per restaurar"
fi

# 6. REINICIAR SERVEIS
print_section "REINICIANT SERVEIS"

print_status "Aturant serveis temporals..."
docker compose down

print_status "Iniciant tots els serveis amb la configuració restaurada..."
if docker compose up -d; then
    print_success "✅ Serveis iniciats"
else
    print_error "❌ Error iniciant serveis"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Esperar que els serveis estiguin llests
print_status "Esperant que els serveis estiguin llests..."
sleep 20

# 7. VERIFICACIÓ RESTORE
print_section "VERIFICACIÓ RESTORE"

print_status "Verificant que els serveis funcionen..."

# Test BD
if docker compose exec -T db pg_isready 2>/dev/null; then
    print_success "✅ Base de dades: OK"
else
    print_error "❌ Base de dades: FALLIT"
fi

# Test web
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    print_success "✅ Aplicació web: OK (HTTP 200)"
elif [ "$HTTP_CODE" = "500" ]; then
    print_warning "⚠️ Aplicació web: Server Error 500"
    print_status "Pot necessitar migracions addicionals"
else
    print_warning "⚠️ Aplicació web: HTTP $HTTP_CODE"
fi

# Test ConfiguracioWeb
if docker compose exec -T web python manage.py shell -c "from web.models import ConfiguracioWeb; print('CONFIG_OK' if ConfiguracioWeb.objects.exists() else 'CONFIG_MISSING')" 2>/dev/null | grep -q "CONFIG_OK"; then
    print_success "✅ ConfiguracioWeb: OK"
else
    print_warning "⚠️ ConfiguracioWeb: Pot necessitar recreació"
fi

# 8. NETEJA
print_section "NETEJA"

print_status "Eliminant fitxers temporals..."
rm -rf "$TEMP_DIR"
print_success "✅ Fitxers temporals eliminats"

# 9. RESUM FINAL
print_section "RESUM RESTORE"

print_success "🎉 Restore completat!"
echo ""
echo "📋 Dades restaurades:"
echo "   • Base de dades PostgreSQL"
echo "   • Media files ($MEDIA_COUNT fitxers)"
echo "   • Configuració bàsica"
echo ""
echo "🔍 Verificació recomanada:"
echo "   • Web pública: http://localhost/"
echo "   • Admin panel: http://localhost/admin/"
echo "   • Credencials admin: admin / cooperativa2025"
echo ""
echo "📝 Passos addicionals si cal:"
echo "   • Executar migracions: docker compose exec web python manage.py migrate"
echo "   • Recrear ConfiguracioWeb: docker compose exec web python manage.py crear_configuracio_inicial"
echo "   • Reiniciar serveis: docker compose restart"
echo ""

print_success "🔄 Restore process finished!"
echo "========================="