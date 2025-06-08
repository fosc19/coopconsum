#!/bin/bash

# Script d'instal·lació automàtica de CoopConsum amb Docker
# Per a cooperatives sense coneixements tècnics

set -e

echo "🤝 Instal·lació automàtica de CoopConsum"
echo "========================================"
echo ""

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

# Verificar que s'executa com a root o amb sudo
if [[ $EUID -ne 0 ]]; then
   print_error "Aquest script necessita permisos d'administrador"
   echo "Executa: sudo bash install_docker.sh"
   exit 1
fi

# Detectar sistema operatiu
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    print_error "No es pot detectar el sistema operatiu"
    exit 1
fi

print_status "Sistema detectat: $OS $VER"

# Verificar si Docker ja està instal·lat
if command -v docker &> /dev/null; then
    print_success "Docker ja està instal·lat"
else
    print_status "Instal·lant Docker..."
    
    # Actualitzar paquets
    apt-get update
    
    # Instal·lar dependències
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Afegir clau GPG oficial de Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Afegir repositori Docker
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Instal·lar Docker
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Iniciar Docker
    systemctl start docker
    systemctl enable docker
    
    print_success "Docker instal·lat correctament"
fi

# Verificar si Docker Compose està disponible
if command -v docker compose &> /dev/null; then
    print_success "Docker Compose disponible"
else
    print_error "Docker Compose no està disponible"
    exit 1
fi

# Demanar informació de la cooperativa
echo ""
print_status "Configuració de la cooperativa"
echo "=============================="

read -p "Nom de la cooperativa: " COOP_NAME
read -p "Email de contacte: " COOP_EMAIL

# Generar contrasenya segura per la base de dades
DB_PASSWORD=$(openssl rand -base64 32)

# Crear directori de treball
INSTALL_DIR="/var/www/coopconsum"
print_status "Creant directori d'instal·lació: $INSTALL_DIR"

if [[ -d "$INSTALL_DIR" ]]; then
    print_warning "El directori ja existeix. Fent backup..."
    mv "$INSTALL_DIR" "${INSTALL_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Descarregar el projecte
print_status "Descarregant CoopConsum..."
git clone https://github.com/fosc19/coopconsum.git .

# Crear fitxer .env
print_status "Configurant variables d'entorn..."
cat > .env << EOF
# Variables d'entorn per Docker Compose - $COOP_NAME
# Generat automàticament per install_docker.sh

# Django
DJANGO_SECRET_KEY=$(openssl rand -base64 50)
DEBUG=False

# Base de dades PostgreSQL
POSTGRES_DB=${COOP_NAME,,}_db
POSTGRES_USER=${COOP_NAME,,}_user
POSTGRES_PASSWORD=$DB_PASSWORD
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Hosts permesos (afegeix el teu domini aquí)
ALLOWED_HOSTS=localhost,127.0.0.1,$(hostname -I | awk '{print $1}')

# CORS (afegeix el teu domini aquí)
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://$(hostname -I | awk '{print $1}')

# CSRF (afegeix el teu domini aquí)
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1,http://$(hostname -I | awk '{print $1}')

# Informació de la cooperativa
COOP_NAME=$COOP_NAME
COOP_EMAIL=$COOP_EMAIL
EOF

# Construir i llançar contenidors
print_status "Construint i llançant contenidors Docker..."
docker compose build
docker compose up -d

# Esperar que els serveis estiguin llests
print_status "Esperant que els serveis estiguin llests..."
sleep 30

# Verificar que els contenidors estan funcionant
if docker compose ps | grep -q "Up"; then
    print_success "Contenidors Docker funcionant correctament"
else
    print_error "Hi ha problemes amb els contenidors Docker"
    docker compose logs
    exit 1
fi

# Configurar cron jobs automàticament
print_status "Configurant tasques automàtiques (cron jobs)..."

# Crear fitxer temporal de crontab
CRON_FILE="/tmp/coopconsum_cron"
cat > "$CRON_FILE" << EOF
# Cronjobs per CoopConsum - Gestió automàtica de comandes
# Instal·lat automàticament per install_docker.sh

# Generar noves comandes diàriament a les 23:58
58 23 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py generar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Tancar comandes diàriament a les 23:59
59 23 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py cerrar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Backup diari de la base de dades a les 02:00
0 2 * * * cd $INSTALL_DIR && docker compose exec -T db pg_dump -U ${COOP_NAME,,}_user ${COOP_NAME,,}_db > ~/backup_coopconsum_\$(date +\\%Y\\%m\\%d).sql && find ~/backup_coopconsum_*.sql -mtime +7 -delete

# Neteja de logs setmanal (diumenge a les 03:00)
0 3 * * 0 find /var/log/coopconsum_cron.log -size +10M -exec truncate -s 0 {} \\;
EOF

# Instal·lar crontab
crontab "$CRON_FILE"
rm "$CRON_FILE"

print_success "Cron jobs configurats correctament"

# Obtenir IP del servidor
SERVER_IP=$(hostname -I | awk '{print $1}')

# Mostrar informació final
echo ""
echo "🎉 Instal·lació completada amb èxit!"
echo "===================================="
echo ""
print_success "CoopConsum està funcionant a:"
echo "  📱 Web pública: http://$SERVER_IP"
echo "  🔧 Panell admin: http://$SERVER_IP/admin/"
echo ""
print_success "Credencials d'administrador:"
echo "  👤 Usuari: admin"
echo "  🔑 Contrasenya: cooperativa2025"
echo ""
print_warning "IMPORTANT: Canvia la contrasenya immediatament!"
echo "  1. Accedeix a http://$SERVER_IP/admin/"
echo "  2. Inicia sessió amb les credencials anteriors"
echo "  3. Ves a 'Usuaris' > 'admin' i canvia la contrasenya"
echo ""
print_status "Tasques automàtiques configurades:"
echo "  ⏰ Generació de comandes: cada dia a les 23:58"
echo "  🔒 Tancament de comandes: cada dia a les 23:59"
echo "  💾 Backup automàtic: cada dia a les 02:00"
echo ""
print_status "Comandos útils:"
echo "  📊 Veure estat: cd $INSTALL_DIR && docker compose ps"
echo "  📝 Veure logs: cd $INSTALL_DIR && docker compose logs -f"
echo "  🔄 Reiniciar: cd $INSTALL_DIR && docker compose restart"
echo "  🛑 Aturar: cd $INSTALL_DIR && docker compose down"
echo ""
print_success "La teva cooperativa ja està llesta per funcionar! 🚀"
