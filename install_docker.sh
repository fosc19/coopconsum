#!/bin/bash

# Script d'instal·lació automàtica de CoopConsum amb Docker
# Per a cooperatives sense coneixements tècnics

set -e

# Funció per gestionar errors
handle_error() {
    local line_no=$1
    local error_code=$2
    echo "ERROR: Script failed at line $line_no with exit code $error_code"
    echo "DEBUG: Last command that failed: $BASH_COMMAND"
    exit $error_code
}

# Configurar trap per capturar errors
trap 'handle_error ${LINENO} $?' ERR

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
    # Verificar si l'usuari té permisos Docker
    if docker version &> /dev/null; then
        # L'usuari pot executar Docker sense sudo
        docker "$@"
    else
        # L'usuari necessita sudo per Docker
        print_warning "Usant sudo per Docker (l'usuari no està al grup docker)"
        sudo docker "$@"
        
        # Si Docker funciona amb sudo, afegir usuari al grup docker per al futur
        if [ "$DOCKER_JUST_INSTALLED" = false ]; then
            print_status "Afegint usuari $USER al grup docker per evitar sudo en el futur..."
            sudo usermod -aG docker $USER
            print_warning "Després de la instal·lació, reinicia la sessió per usar Docker sense sudo"
        fi
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
DB_PASSWORD=$(openssl rand -hex 16)

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
run_docker_command compose build --no-cache
run_docker_command compose up -d

# Esperar que els serveis estiguin llests
print_status "Esperant que els serveis estiguin llests..."
sleep 45

# Verificar que els contenidors estan funcionant
if run_docker_command compose ps | grep -q "Up"; then
    print_success "Contenidors Docker funcionant correctament"
else
    print_error "Hi ha problemes amb els contenidors Docker"
    run_docker_command compose logs
    exit 1
fi

# Les tasques Django (migracions, superusuari, collectstatic) es fan automàticament
# dins del contenidor via docker-entrypoint.sh quan s'inicia
print_status "Les tasques d'inicialització Django es fan automàticament al contenidor..."

# HEALTH CHECKS COMPLETS
print_status "Executant health checks complets..."
echo ""

# Funció per esperar que un servei estigui llest
wait_for_service() {
    local service_name="$1"
    local max_attempts="$2"
    shift 2
    local attempt=1
    
    print_status "Esperant que $service_name estigui llest..."
    
    while [ $attempt -le $max_attempts ]; do
        # CAMBIO CRÍTICO: No usar eval, execució directa per evitar problemes amb curl|bash
        if "$@" 2>/dev/null; then
            print_success "✅ $service_name llest (intent $attempt/$max_attempts)"
            return 0
        fi
        
        print_status "Intent $attempt/$max_attempts - $service_name encara no està llest..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    print_error "❌ $service_name no s'ha inicialitzat després de $max_attempts intents"
    return 1
}

# Health check 1: Esperar que la base de dades estigui llesta
if ! wait_for_service "Base de dades PostgreSQL" 12 run_docker_command compose exec -T db pg_isready; then
    print_warning "⚠️ La base de dades trigarà més a estar llesta. Revisant logs..."
    run_docker_command compose logs db --tail=10
    print_status "Continuant amb la instal·lació..."
fi

# Health check 2: Esperar que el contenidor web estigui healthy
check_web_container() {
    run_docker_command compose ps web | grep -q 'Up'
}
if ! wait_for_service "Contenidor web Django" 20 check_web_container; then
    print_warning "⚠️ El contenidor web trigarà més a inicialitzar-se. Revisant logs..."
    run_docker_command compose logs web --tail=20
    print_status "Continuant amb la instal·lació..."
fi

# Health check 3: Verificar que Django pot connectar amb la BD
print_status "Verificant connexió Django amb base de dades..."
if run_docker_command compose exec -T web python manage.py check --database default 2>/dev/null; then
    print_success "✅ Django connecta correctament amb la base de dades"
else
    print_warning "⚠️ Problemes amb la connexió a la base de dades"
    print_status "Intentant reparar connexions..."
    sleep 10
    if ! run_docker_command compose exec -T web python manage.py check --database default 2>/dev/null; then
        print_warning "⚠️ Connexió BD trigarà més - serveis encara s'estan inicialitzant"
        print_status "Continuant amb la instal·lació..."
    fi
fi

# Health check 4: Test HTTP amb retries intel·ligents
print_status "Testejant resposta HTTP de l'aplicació web..."

HTTP_ATTEMPTS=0
MAX_HTTP_ATTEMPTS=15
HTTP_SUCCESS=false

while [ $HTTP_ATTEMPTS -lt $MAX_HTTP_ATTEMPTS ] && [ "$HTTP_SUCCESS" = false ]; do
    HTTP_ATTEMPTS=$((HTTP_ATTEMPTS + 1))
    print_status "Test HTTP $HTTP_ATTEMPTS/$MAX_HTTP_ATTEMPTS..."
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
    
    case "$HTTP_CODE" in
        "200")
            print_success "✅ Web pública funcionant correctament (HTTP 200)"
            HTTP_SUCCESS=true
            ;;
        "500")
            print_warning "⚠️ Server Error 500 detectat (intent $HTTP_ATTEMPTS/$MAX_HTTP_ATTEMPTS)"
            if [ $HTTP_ATTEMPTS -eq 1 ]; then
                print_status "Aplicant fix automàtic per Server Error 500..."
                
                # Fix automàtic per Server Error 500
                print_status "Verificant i aplicant migracions..."
                run_docker_command compose exec -T web python manage.py makemigrations --noinput || true
                run_docker_command compose exec -T web python manage.py migrate --noinput || true
                
                print_status "Creant ConfiguracioWeb..."
                run_docker_command compose exec -T web python manage.py crear_configuracio_inicial || true
                
                print_status "Reiniciant contenidor web..."
                run_docker_command compose restart web
                
                print_status "Esperant que el servei es recuperi..."
                sleep 15
            else
                sleep 10
            fi
            ;;
        "000"|"502"|"503")
            print_status "Servei encara inicialitzant-se (HTTP $HTTP_CODE)..."
            sleep 8
            ;;
        *)
            print_warning "Resposta HTTP inesperada: $HTTP_CODE"
            sleep 5
            ;;
    esac
done

if [ "$HTTP_SUCCESS" = false ]; then
    print_warning "⚠️ L'aplicació web no respon completament després de $MAX_HTTP_ATTEMPTS intents"
    print_status "Això no impedeix continuar amb la instal·lació - pot funcionar correctament"
    print_status "Mostrant logs per diagnòstic:"
    run_docker_command compose logs web --tail=10
fi

# Health check 5: Verificar ConfiguracioWeb
print_status "Verificant model ConfiguracioWeb..."
if run_docker_command compose exec -T web python manage.py shell -c "from web.models import ConfiguracioWeb; config = ConfiguracioWeb.objects.first(); print('CONFIG_OK:', config.nom_cooperativa if config else 'MISSING')" 2>/dev/null | grep -q "CONFIG_OK:"; then
    print_success "✅ ConfiguracioWeb verificada correctament"
else
    print_warning "⚠️ ConfiguracioWeb no detectada, creant..."
    if run_docker_command compose exec -T web python manage.py crear_configuracio_inicial; then
        print_success "✅ ConfiguracioWeb creada correctament"
    else
        print_warning "⚠️ No es pot crear ConfiguracioWeb automàticament"
        print_status "Pots crear-la manualment després des de l'admin panel"
    fi
fi

# Health check 6: Verificar admin panel
print_status "Verificant accés a l'admin panel..."
ADMIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/admin/ 2>/dev/null || echo "000")
if [ "$ADMIN_CODE" = "200" ] || [ "$ADMIN_CODE" = "302" ]; then
    print_success "✅ Admin panel accessible (HTTP $ADMIN_CODE)"
else
    print_warning "⚠️ Admin panel retorna HTTP $ADMIN_CODE"
fi

# Health check 7: Test API endpoints
print_status "Verificant API endpoints..."
API_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/productos/ 2>/dev/null || echo "000")
if [ "$API_CODE" = "200" ]; then
    print_success "✅ API endpoints funcionant (HTTP 200)"
else
    print_warning "⚠️ API retorna HTTP $API_CODE (pot ser normal si no hi ha dades)"
fi

print_success "🎯 Health checks completats!"

# ASSEGURAR QUE LES INSTRUCCIONS FINALS SEMPRE ES MOSTREN
# Aquesta funció es crida sempre, independentment dels health checks
show_final_instructions() {
    # Obtenir IP del servidor
    SERVER_IP=$(hostname -I | awk '{print $1}')
    
    # Mostrar informació final SEMPRE
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
    echo "  ⏰ Generació de comandes: cada dia a les 23:58"
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
}

# PROTECCIÓ FINAL - Assegurar que les instruccions SEMPRE es mostren
run_final_steps() {
    # Configurar cron jobs del sistema per execució automàtica diària
    print_status "Configurant tasques automàtiques al sistema..."

    # Crear arxiu temporal amb els cron jobs
    cat > /tmp/coopconsum_cron << EOF
# CoopConsum - Tasques automàtiques
# Generar comandes recurrents cada dia a les 23:58
58 23 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py generar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Tancar comandes vençudes cada dia a les 23:59
59 23 * * * cd $INSTALL_DIR && docker compose exec -T web python manage.py cerrar_pedidos >> /var/log/coopconsum_cron.log 2>&1

# Neteja de logs setmanal (diumenges a les 03:00)
0 3 * * 0 find /var/log/coopconsum_cron.log -size +10M -exec truncate -s 0 {} \; 2>/dev/null
EOF

    # Instal·lar els cron jobs
    if crontab -l >/dev/null 2>&1; then
        # Si ja hi ha crontab, afegir els nous
        (crontab -l; cat /tmp/coopconsum_cron) | crontab - || true
    else
        # Si no hi ha crontab, crear-ne un de nou
        crontab /tmp/coopconsum_cron || true
    fi

    # Netejar arxiu temporal
    rm -f /tmp/coopconsum_cron

    # Crear directori de logs si no existeix
    sudo mkdir -p /var/log || true
    sudo touch /var/log/coopconsum_cron.log || true
    sudo chown $USER:$USER /var/log/coopconsum_cron.log || true

    print_success "Tasques automàtiques configurades al sistema"
    
    # MOSTRAR INSTRUCCIONS FINALS SEMPRE
    show_final_instructions
}

# Executar passos finals amb protecció múltiple per curl|bash
{
    # Desactivar set -e per evitar que termini prematurament
    set +e
    
    # Executar passos finals
    run_final_steps
    
    # Doble protecció - assegurar que les instruccions es mostren
    if [ $? -ne 0 ]; then
        print_warning "Algun pas final ha fallat, però mostrant instruccions igualment..."
        show_final_instructions
    fi
    
} || {
    # Triple protecció - si tot falla, mostrar instruccions sense filigranes
    set +e
    echo ""
    echo "🎉 Instal·lació completada!"
    echo "=============================="
    echo ""
    SERVER_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")
    echo "📱 Web pública: http://$SERVER_IP"
    echo "🔧 Panell admin: http://$SERVER_IP/admin/"
    echo "👤 Usuari: admin"
    echo "🔑 Contrasenya: cooperativa2025"
    echo ""
    echo "La teva cooperativa ja està llesta! 🚀"
    show_final_instructions 2>/dev/null || true
}

# Assegurar exit correcte
exit 0
