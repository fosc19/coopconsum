#!/bin/bash

# Script per instal·lar Docker al VPS de test de forma segura
# IP: 57.129.134.84
# Executa aquest script després de connectar-te per SSH

echo "=== INSTAL·LACIÓ DOCKER AL VPS DE TEST ==="
echo "Data: $(date)"
echo ""

# 1. Verificar sistema
echo "1. Verificant sistema operatiu..."
cat /etc/os-release | head -3
echo ""

# 2. Verificar serveis existents (per no trencar res)
echo "2. Verificant serveis actius..."
systemctl list-units --type=service --state=running | grep -E "(nginx|apache|mysql|postgresql|docker)" || echo "Cap servei web/db detectat"
echo ""

# 3. Verificar ports ocupats
echo "3. Verificant ports ocupats..."
netstat -tlnp | grep -E ":80|:443|:3000|:8000" || echo "Ports web lliures"
echo ""

# 4. Verificar espai disponible
echo "4. Verificant espai disponible..."
df -h /
echo ""

# 5. Crear directori de test en ubicació segura
echo "5. Creant directori de test..."
mkdir -p /tmp/docker_test
cd /tmp/docker_test

# 6. Clonar repositori públic
echo "6. Clonant repositori públic..."
git clone https://github.com/fosc19/coopconsum.git
cd coopconsum

# 7. Verificar fitxers Docker
echo "7. Verificant fitxers Docker..."
ls -la | grep -E "(Dockerfile|docker-compose|\.env)"

# 8. Instal·lar Docker si no està instal·lat
if ! command -v docker &> /dev/null; then
    echo "8. Instal·lant Docker..."
    ./install_docker.sh
else
    echo "8. Docker ja està instal·lat:"
    docker --version
fi

# 9. Configurar .env de test
echo "9. Configurant .env de test..."
cp .env.example .env
sed -i 's/el_teu_domini.com/57.129.134.84/g' .env
sed -i 's/canvia_aquesta_contrasenya/test_password_123/g' .env
sed -i 's/canvia_aquesta_clau_secreta_django/test-secret-key-123456789/g' .env

# 10. Mostrar configuració
echo "10. Configuració .env:"
cat .env

echo ""
echo "=== PREPARAT PER PROVAR DOCKER ==="
echo "Per iniciar Docker:"
echo "cd /tmp/docker_test/coopconsum"
echo "docker compose up -d"
echo ""
echo "Per aturar Docker:"
echo "docker compose down"
echo ""
echo "Per veure logs:"
echo "docker compose logs"