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

# Variable per controlar si Docker s'ha instal·lat en aquesta execució
DOCKER_JUST_INSTALLED=false

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

# Funció per executar comandos Docker amb permisos adequats
run_docker_command() {
    if [ "$DOCKER_JUST_INSTALLED" = true ]; then
        # Si acabem d'instal·lar Docker, usar sudo temporalment
        sudo docker "$@"
    else
        # Docker ja estava instal·lat, usar normalment
        docker "$@"
    fi
}

# Verificar que s'executa amb permisos adequats
if [[ $EUID -eq 0 ]]; then
   print_error "Aquest script no s'ha d'executar com a root"
   print_status "Executa'l com a usuari normal. El script demanarà sudo quan sigui necessari."
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
    sudo apt-get update
    
    # Instal·lar dependències
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Afegir clau GPG oficial de Docker
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Afegir repositori Docker
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Instal·lar Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Afegir usuari al grup docker
    sudo usermod -aG docker $USER
    
    # Iniciar Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Marcar que Docker s'ha instal·lat en aquesta execució
    DOCKER_JUST_INSTALLED=true
    
    print_success "Docker instal·lat correctament"
    print_warning "NOTA: S'està usant sudo per Docker temporalment. Després de la instal·lació, reinicia la sessió per usar Docker sense sudo."
fi

# Verificar si Docker Compose està disponible
if run_docker_command compose version &> /dev/null; then
    print_success "Docker Compose disponible"
else
    print_error "Docker Compose no està disponible"
    exit 1
fi

# No necessitem Nginx - Django servirà directament al port 80
print_status "Configurant accés directe al port 80..."

# Crear directori de treball
INSTALL_DIR="/var/www/coopconsum"
print_status "Creant directori d'instal·lació: $INSTALL_DIR"

if [[ -d "$INSTALL_DIR" ]]; then
    print_warning "El directori ja existeix. Fent backup..."
    sudo mv "$INSTALL_DIR" "${INSTALL_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

sudo mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Descarregar el projecte
print_status "Descarregant CoopConsum..."
sudo git clone https://github.com/fosc19/coopconsum.git .

# Canviar propietari al usuari actual
sudo chown -R $USER:$USER .

# Demanar informació de la cooperativa
echo ""
print_status "Configuració de la cooperativa"
echo "=============================="

# Verificar si estem en mode interactiu
if [[ -t 0 ]]; then
    # Mode interactiu
    read -p "Nom de la cooperativa: " COOP_NAME
    read -p "Email de contacte: " COOP_EMAIL
else
    # Mode no interactiu (curl | bash)
    print_warning "Mode no interactiu detectat. Usant valors per defecte."
    COOP_NAME="cooperativa"
    COOP_EMAIL="admin@cooperativa.local"
    print_status "Nom de cooperativa: $COOP_NAME"
    print_status "Email de contacte: $COOP_EMAIL"
fi

# Validar que les variables no estiguin buides
if [[ -z "$COOP_NAME" ]]; then
    COOP_NAME="cooperativa"
fi

if [[ -z "$COOP_EMAIL" ]]; then
    COOP_EMAIL="admin@cooperativa.local"
fi

# Generar contrasenya segura per la base de dades
DB_PASSWORD=$(openssl rand -base64 32)

# Crear fitxer .env
print_status "Configurant variables d'entorn..."

# Netejar nom de cooperativa per usar com a nom de base de dades
CLEAN_COOP_NAME=$(echo "$COOP_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')

cat > .env << EOF
# Variables d'entorn per Docker Compose - $COOP_NAME
# Generat automàticament per install_docker.sh

# Django
DJANGO_SECRET_KEY=$(openssl rand -hex 25)
DEBUG=False

# Base de dades PostgreSQL
POSTGRES_DB=${CLEAN_COOP_NAME}_db
POSTGRES_USER=${CLEAN_COOP_NAME}_user
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
run_docker_command compose build
run_docker_command compose up -d

# Esperar que els serveis estiguin llests
print_status "Esperant que els serveis estiguin llests..."
sleep 30

# Verificar que els contenidors estan funcionant
if run_docker_command compose ps | grep -q "Up"; then
    print_success "Contenidors Docker funcionant correctament"
else
    print_error "Hi ha problemes amb els contenidors Docker"
    run_docker_command compose logs
    exit 1
fi

# Executar migracions de la base de dades
print_status "Executant migracions de la base de dades..."
run_docker_command compose exec -T web python manage.py migrate

# Crear superusuari
print_status "Creant usuari administrador..."
run_docker_command compose exec -T web python manage.py shell << 'EOF'
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
print_status "Col·lectant fitxers estàtics..."
run_docker_command compose exec -T web python manage.py collectstatic --noinput

print_success "Aplicació configurada per servir directament al port 80"

# Configurar cron jobs del sistema per execució automàtica diària
print_status "Configurant tasques automàtiques al sistema..."

# Crear arxiu temporal amb els cron jobs
cat > /tmp/coopconsum_cron << EOF
# CoopConsum - Tasques automàtiques
# Generar comandes recurrents cada dia a les 00:30
30 0 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py generar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Tancar comandes vençudes cada dia a les 23:59
59 23 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py cerrar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Neteja de logs setmanal (diumenges a les 03:00)
0 3 * * 0 find /var/log/coopconsum_cron.log -size +10M -exec truncate -s 0 {} \; 2>/dev/null
EOF

# Instal·lar els cron jobs
if crontab -l >/dev/null 2>&1; then
    # Si ja hi ha crontab, afegir els nous
    (crontab -l; cat /tmp/coopconsum_cron) | crontab -
else
    # Si no hi ha crontab, crear-ne un de nou
    crontab /tmp/coopconsum_cron
fi

# Netejar arxiu temporal
rm -f /tmp/coopconsum_cron

# Crear directori de logs si no existeix
sudo mkdir -p /var/log
sudo touch /var/log/coopconsum_cron.log
sudo chown $USER:$USER /var/log/coopconsum_cron.log

print_success "Tasques automàtiques configurades al sistema"

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
print_status "Tasques automàtiques configurades (cron del sistema):"
echo "  ⏰ Generació de comandes: cada dia a les 00:30"
echo "  🔒 Tancament de comandes: cada dia a les 23:59"
echo "  🧹 Neteja de logs: cada diumenge a les 03:00"
echo "  📝 Logs disponibles a: /var/log/coopconsum_cron.log"
echo ""
print_success "💾 Backup automàtic: Configurat al proveïdor VPS (recomanat)"
echo ""
print_status "Comandos útils:"
echo "  📊 Veure estat: cd $INSTALL_DIR && docker compose ps"
echo "  📝 Veure logs: cd $INSTALL_DIR && docker compose logs -f"
echo "  🔄 Reiniciar: cd $INSTALL_DIR && docker compose restart"
echo "  🛑 Aturar: cd $INSTALL_DIR && docker compose down"
echo ""
print_status "Verificar tasques automàtiques:"
echo "  ✅ Veure cron jobs: crontab -l"
echo "  📋 Veure logs: tail -f /var/log/coopconsum_cron.log"
echo "  🧪 Provar manualment: cd $INSTALL_DIR && docker compose exec web python manage.py generar_pedidos_test"
echo ""
if [ "$DOCKER_JUST_INSTALLED" = true ]; then
    echo ""
    print_warning "IMPORTANT: Docker s'ha instal·lat durant aquesta execució."
    print_status "Per a futures operacions de Docker sense sudo, executa:"
    echo "  🔄 newgrp docker"
    echo "  o bé reinicia la sessió SSH"
    echo ""
fi

print_success "La teva cooperativa ja està llesta per funcionar! 🚀"
