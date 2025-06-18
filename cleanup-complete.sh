#!/bin/bash

# Script de neteja completa per CoopConsum
# Elimina tots els rastres: Docker, aplicació, configuració, logs, etc.
# Ús: ./cleanup-complete.sh

set -e

echo "🧹 NETEJA TOTAL CoopConsum - Eliminant tot rastre..."
echo "================================================="
echo ""

# Colors per a la sortida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVÍS]${NC} $1"
}

# Advertència de seguretat
print_warning "⚠️ ATENCIÓ: Aquest script eliminarà COMPLETAMENT:"
echo "  • Tots els contenidors i imatges Docker"
echo "  • Tota l'aplicació CoopConsum"
echo "  • Totes les dades de la base de dades"
echo "  • Tots els media files"
echo "  • Tota la configuració"
echo "  • Docker completament"
echo ""
read -p "Confirma que vols continuar [y/N]: " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Neteja cancel·lada per l'usuari"
    exit 0
fi

echo ""
echo "🔥 Iniciant neteja completa..."
echo ""

# 1. Parar i eliminar contenidors Docker
print_status "📦 Eliminant contenidors Docker..."
if command -v docker &> /dev/null; then
    # Parar tots els contenidors
    if [ -n "$(sudo docker ps -q)" ]; then
        sudo docker stop $(sudo docker ps -q) 2>/dev/null || true
        print_success "Contenidors parats"
    fi
    
    # Eliminar tots els contenidors
    if [ -n "$(sudo docker ps -aq)" ]; then
        sudo docker rm $(sudo docker ps -aq) 2>/dev/null || true
        print_success "Contenidors eliminats"
    fi
else
    print_warning "Docker no està instal·lat"
fi

# 2. Eliminar imatges Docker
print_status "🖼️ Eliminant imatges Docker..."
if command -v docker &> /dev/null; then
    if [ -n "$(sudo docker images -q)" ]; then
        sudo docker rmi $(sudo docker images -q) --force 2>/dev/null || true
        print_success "Imatges Docker eliminades"
    else
        print_warning "No hi ha imatges Docker per eliminar"
    fi
fi

# 3. Eliminar volums Docker
print_status "💾 Eliminant volums Docker..."
if command -v docker &> /dev/null; then
    if [ -n "$(sudo docker volume ls -q)" ]; then
        sudo docker volume rm $(sudo docker volume ls -q) 2>/dev/null || true
        print_success "Volums Docker eliminats"
    else
        print_warning "No hi ha volums Docker per eliminar"
    fi
fi

# 4. Neteja sistema Docker complet
print_status "🔄 Neteja profunda Docker..."
if command -v docker &> /dev/null; then
    sudo docker system prune -af --volumes 2>/dev/null || true
    print_success "Sistema Docker netejat"
fi

# 5. Eliminar directori CoopConsum
print_status "🗂️ Eliminant instal·lació CoopConsum..."
if [ -d "/var/www/coopconsum" ]; then
    sudo rm -rf /var/www/coopconsum
    print_success "Directori CoopConsum eliminat"
else
    print_warning "Directori CoopConsum no existeix"
fi

# 6. Eliminar crontabs relacionats
print_status "⏰ Eliminant crontabs..."
# Eliminar crontabs de l'usuari actual
if crontab -l 2>/dev/null | grep -q "coopconsum\|docker"; then
    # Backup crontab existent sense les línies de CoopConsum
    crontab -l 2>/dev/null | grep -v "coopconsum\|docker" | crontab - 2>/dev/null || crontab -r 2>/dev/null
    print_success "Crontabs CoopConsum eliminats"
else
    print_warning "No hi ha crontabs CoopConsum per eliminar"
fi

# 7. Eliminar arxius de log
print_status "📝 Eliminant logs..."
sudo rm -f /var/log/coopconsum_cron.log
sudo rm -f ~/backup_coopconsum_*.sql
find . -name "coopconsum_backup_*.tar.gz" -delete 2>/dev/null || true
print_success "Logs eliminats"

# 8. Desinstal·lar Docker completament
print_status "❌ Desinstal·lant Docker..."
if command -v docker &> /dev/null; then
    # Eliminar usuari del grup docker primer
    sudo deluser $USER docker 2>/dev/null || true
    
    # Desinstal·lar paquets Docker
    sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-buildx-plugin docker-ce-rootless-extras 2>/dev/null || true
    sudo apt-get autoremove -y --purge 2>/dev/null || true
    
    print_success "Docker desinstal·lat"
else
    print_warning "Docker ja no està instal·lat"
fi

# 9. Eliminar directoris Docker
print_status "📁 Eliminant directoris Docker..."
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker
sudo rm -rf ~/.docker
print_success "Directoris Docker eliminats"

# 10. Eliminar grup docker
print_status "👥 Eliminant grup docker..."
sudo groupdel docker 2>/dev/null || true
print_success "Grup docker eliminat"

# 11. Eliminar repositoris Docker
print_status "📋 Netejant repositoris..."
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/keyrings/docker.gpg
print_success "Repositoris Docker eliminats"

# 12. Neteja cache del sistema
print_status "🧽 Netejant cache del sistema..."
sudo apt-get autoremove -y
sudo apt-get autoclean
sudo apt-get clean
print_success "Cache sistema netejat"

# 13. Verificacions finals
echo ""
echo "🔍 VERIFICACIONS FINALS:"
echo "========================================"

verification_passed=true

# Verificar Docker
if command -v docker &> /dev/null; then
    print_warning "⚠️ Docker ENCARA està instal·lat"
    verification_passed=false
else
    print_success "✅ Docker eliminat correctament"
fi

# Verificar directori
if [ -d "/var/www/coopconsum" ]; then
    print_warning "⚠️ Directori CoopConsum ENCARA existeix"
    verification_passed=false
else
    print_success "✅ Directori CoopConsum eliminat"
fi

# Verificar crontab
if crontab -l 2>/dev/null | grep -q "coopconsum\|docker"; then
    print_warning "⚠️ Crontabs CoopConsum ENCARA existeixen"
    verification_passed=false
else
    print_success "✅ Crontabs eliminats"
fi

# Verificar grup docker
if getent group docker >/dev/null 2>&1; then
    print_warning "⚠️ Grup docker ENCARA existeix"
    verification_passed=false
else
    print_success "✅ Grup docker eliminat"
fi

# Verificar directoris Docker
if [ -d "/var/lib/docker" ] || [ -d "/etc/docker" ]; then
    print_warning "⚠️ Directoris Docker ENCARA existeixen"
    verification_passed=false
else
    print_success "✅ Directoris Docker eliminats"
fi

echo ""
if [ "$verification_passed" = true ]; then
    echo "🎯 SERVIDOR COMPLETAMENT NET"
    echo "========================================"
    print_success "✅ Neteja completada amb èxit!"
    echo ""
    echo "🚀 Llest per nova instal·lació amb:"
    echo "curl -sSL https://github.com/fosc19/coopconsum/raw/master/install_docker.sh | bash"
else
    echo "⚠️ NETEJA PARCIAL"
    echo "========================================"
    print_warning "Alguns elements no s'han pogut eliminar completament"
    print_status "Pots executar el script altra vegada o eliminar manualment els elements restants"
fi

echo ""