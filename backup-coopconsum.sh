#!/bin/bash

# Script de backup complet per CoopConsum
# Crea backup de BD, media files i configuració
# Ús: ./backup-coopconsum.sh [directori_backup]

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

# Verificar que s'executa des del directori correcte
if [ ! -f "manage.py" ] || [ ! -f "docker-compose.yml" ]; then
    print_error "Aquest script s'ha d'executar des del directori arrel de CoopConsum"
    print_status "Directori actual: $(pwd)"
    exit 1
fi

# Configurar directori de backup
BACKUP_DIR="${1:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="coopconsum_backup_$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo "💾 Backup Complet CoopConsum"
echo "============================"
echo ""
print_status "Directori backup: $BACKUP_PATH"
print_status "Timestamp: $TIMESTAMP"
echo ""

# Crear directori de backup
print_section "PREPARACIÓ BACKUP"
mkdir -p "$BACKUP_PATH"
print_success "Directori backup creat: $BACKUP_PATH"

# 1. BACKUP BASE DE DADES
print_section "BACKUP BASE DE DADES"

print_status "Extraient variables d'entorn..."
if [ -f ".env" ]; then
    # Carregar variables d'entorn
    export $(grep -v '^#' .env | xargs)
    print_success "Variables d'entorn carregades des de .env"
else
    print_warning "Fitxer .env no trobat, usant valors per defecte"
    POSTGRES_DB=${POSTGRES_DB:-coopconsum_db}
    POSTGRES_USER=${POSTGRES_USER:-coopconsum_user}
fi

print_status "Base de dades: $POSTGRES_DB"
print_status "Usuari: $POSTGRES_USER"

# Verificar que els contenidors estan funcionant
if ! docker compose ps | grep -q "Up"; then
    print_error "Els contenidors Docker no estan funcionant"
    print_status "Inicia els contenidors amb: docker compose up -d"
    exit 1
fi

# Crear backup de la base de dades
print_status "Creant backup de PostgreSQL..."
DB_BACKUP_FILE="$BACKUP_PATH/database.sql"

if docker compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "$DB_BACKUP_FILE"; then
    DB_SIZE=$(du -h "$DB_BACKUP_FILE" | cut -f1)
    print_success "✅ Backup BD completat: $DB_SIZE"
else
    print_error "❌ Error creant backup de la base de dades"
    exit 1
fi

# 2. BACKUP MEDIA FILES
print_section "BACKUP MEDIA FILES"

print_status "Copiant fitxers media..."
MEDIA_BACKUP_DIR="$BACKUP_PATH/media"
mkdir -p "$MEDIA_BACKUP_DIR"

# Copiar media files des del contenidor
if docker compose exec -T web find /app/media -type f 2>/dev/null | grep -q "."; then
    print_status "Extraient media files del contenidor..."
    docker compose exec -T web tar -czf /tmp/media_backup.tar.gz -C /app media/ 2>/dev/null || true
    docker compose cp web:/tmp/media_backup.tar.gz "$BACKUP_PATH/media_files.tar.gz"
    docker compose exec -T web rm -f /tmp/media_backup.tar.gz
    
    # Extreure per verificació
    if [ -f "$BACKUP_PATH/media_files.tar.gz" ]; then
        cd "$BACKUP_PATH"
        tar -xzf media_files.tar.gz
        MEDIA_COUNT=$(find media -type f 2>/dev/null | wc -l)
        MEDIA_SIZE=$(du -sh media 2>/dev/null | cut -f1 || echo "0")
        print_success "✅ Media files copiats: $MEDIA_COUNT fitxers ($MEDIA_SIZE)"
        cd - >/dev/null
    fi
else
    print_warning "⚠️ No hi ha media files per fer backup"
    echo "No media files" > "$MEDIA_BACKUP_DIR/empty.txt"
fi

# 3. BACKUP CONFIGURACIÓ
print_section "BACKUP CONFIGURACIÓ"

print_status "Copiant fitxers de configuració..."
CONFIG_BACKUP_DIR="$BACKUP_PATH/config"
mkdir -p "$CONFIG_BACKUP_DIR"

# Llista de fitxers crítics de configuració
CONFIG_FILES=(
    ".env"
    "docker-compose.yml"
    "docker-entrypoint.sh"
    "requirements.txt"
    "coopconsum/settings_base.py"
)

CONFIG_COUNT=0
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        # Crear directoris necessaris
        mkdir -p "$CONFIG_BACKUP_DIR/$(dirname "$file")"
        cp "$file" "$CONFIG_BACKUP_DIR/$file"
        CONFIG_COUNT=$((CONFIG_COUNT + 1))
        print_status "  ✓ $file"
    else
        print_warning "  ⚠️ $file no trobat"
    fi
done

print_success "✅ Configuració copiada: $CONFIG_COUNT fitxers"

# 4. BACKUP INFORMACIÓ SISTEMA
print_section "BACKUP INFORMACIÓ SISTEMA"

print_status "Recopilant informació del sistema..."
INFO_FILE="$BACKUP_PATH/system_info.txt"

cat > "$INFO_FILE" << EOF
CoopConsum Backup Information
============================
Date: $(date)
Hostname: $(hostname)
User: $(whoami)
Backup Directory: $BACKUP_PATH

Docker Information:
------------------
$(docker --version)
$(docker compose version)

Container Status:
----------------
$(docker compose ps)

Database Information:
--------------------
Database: $POSTGRES_DB
User: $POSTGRES_USER

Git Information:
---------------
$(git branch --show-current 2>/dev/null || echo "Not a git repository")
$(git log --oneline -5 2>/dev/null || echo "No git history")

System Resources:
----------------
Disk Space: $(df -h .)
Memory: $(free -h | grep "Mem:")
EOF

print_success "✅ Informació sistema guardada"

# 5. VERIFICACIÓ BACKUP
print_section "VERIFICACIÓ BACKUP"

print_status "Verificant integritat del backup..."

# Verificar que tots els components estan presents
VERIFICATION_OK=true

# Verificar BD
if [ -f "$DB_BACKUP_FILE" ] && [ -s "$DB_BACKUP_FILE" ]; then
    print_success "✅ Backup base de dades: OK"
else
    print_error "❌ Backup base de dades: FALLIT"
    VERIFICATION_OK=false
fi

# Verificar media
if [ -d "$BACKUP_PATH/media" ] || [ -f "$BACKUP_PATH/media_files.tar.gz" ]; then
    print_success "✅ Backup media files: OK"
else
    print_warning "⚠️ Backup media files: BUIT"
fi

# Verificar configuració
if [ -d "$CONFIG_BACKUP_DIR" ] && [ $CONFIG_COUNT -gt 0 ]; then
    print_success "✅ Backup configuració: OK"
else
    print_error "❌ Backup configuració: FALLIT"
    VERIFICATION_OK=false
fi

# Verificar informació sistema
if [ -f "$INFO_FILE" ] && [ -s "$INFO_FILE" ]; then
    print_success "✅ Informació sistema: OK"
else
    print_error "❌ Informació sistema: FALLIT"
    VERIFICATION_OK=false
fi

# 6. CREAR ARXIU COMPLET
print_section "COMPRESSIÓ FINAL"

print_status "Creant arxiu comprimit del backup..."
cd "$BACKUP_DIR"
COMPRESSED_BACKUP="$BACKUP_NAME.tar.gz"

if tar -czf "$COMPRESSED_BACKUP" "$BACKUP_NAME/"; then
    BACKUP_SIZE=$(du -h "$COMPRESSED_BACKUP" | cut -f1)
    print_success "✅ Backup comprimit creat: $COMPRESSED_BACKUP ($BACKUP_SIZE)"
    
    # Opcional: eliminar directori no comprimit
    read -p "Eliminar directori backup no comprimit? [y/N]: " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$BACKUP_NAME"
        print_status "Directori no comprimit eliminat"
    fi
else
    print_error "❌ Error creant arxiu comprimit"
    VERIFICATION_OK=false
fi

cd - >/dev/null

# 7. RESUM FINAL
print_section "RESUM BACKUP"

if [ "$VERIFICATION_OK" = true ]; then
    print_success "🎉 Backup completat amb èxit!"
    echo ""
    echo "📁 Ubicació backup:"
    echo "   Directori: $BACKUP_PATH"
    if [ -f "$BACKUP_DIR/$COMPRESSED_BACKUP" ]; then
        echo "   Arxiu: $BACKUP_DIR/$COMPRESSED_BACKUP ($BACKUP_SIZE)"
    fi
    echo ""
    echo "📋 Contingut backup:"
    echo "   • Base de dades PostgreSQL"
    echo "   • Media files (imatges, documents)"
    echo "   • Fitxers de configuració"
    echo "   • Informació del sistema"
    echo ""
    echo "🔄 Per restaurar aquest backup:"
    echo "   ./restore-coopconsum.sh $BACKUP_DIR/$COMPRESSED_BACKUP"
    echo ""
else
    print_error "❌ Backup completat amb errors"
    print_status "Revisa els missatges anteriors per identificar els problemes"
    exit 1
fi

print_success "💾 Backup process finished!"
echo "=========================="