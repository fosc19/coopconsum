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
    
    print_success "Docker instal·lat correctament"
fi

# Verificar si Docker Compose està disponible
if command -v docker compose &> /dev/null; then
    print_success "Docker Compose disponible"
else
    print_error "Docker Compose no està disponible"
    exit 1
fi

# Instal·lar Nginx si no està instal·lat
if command -v nginx &> /dev/null; then
    print_success "Nginx ja està instal·lat"
else
    print_status "Instal·lant Nginx..."
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    print_success "Nginx instal·lat correctament"
fi

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
DJANGO_SECRET_KEY=$(openssl rand -base64 50)
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

# Executar migracions de la base de dades
print_status "Executant migracions de la base de dades..."
docker compose exec -T web python manage.py migrate

# Crear superusuari
print_status "Creant usuari administrador..."
docker compose exec -T web python manage.py shell << 'EOF'
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
docker compose exec -T web python manage.py collectstatic --noinput

# Configurar Nginx
print_status "Configurant Nginx..."
sudo tee /etc/nginx/sites-available/coopconsum > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    # Servir fitxers estàtics directament
    location /static/ {
        alias /var/www/coopconsum/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
        gzip on;
        gzip_types text/css application/javascript text/javascript application/json;
    }
    
    location /media/ {
        alias /var/www/coopconsum/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # Proxy per a l'aplicació Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
NGINX_EOF

# Habilitar el lloc
sudo ln -sf /etc/nginx/sites-available/coopconsum /etc/nginx/sites-enabled/

# Eliminar configuració per defecte si existeix
sudo rm -f /etc/nginx/sites-enabled/default

# Verificar configuració
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx

print_success "Nginx configurat correctament"

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
sudo crontab "$CRON_FILE"
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
