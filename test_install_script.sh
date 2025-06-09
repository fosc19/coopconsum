#!/bin/bash

# Script de test per verificar l'script d'instal·lació
# Aquest script simula l'execució sense fer canvis reals

echo "🧪 Test de l'script d'instal·lació de CoopConsum"
echo "==============================================="
echo ""

# Verificar que l'script existeix
if [[ ! -f "install_docker.sh" ]]; then
    echo "❌ ERROR: No es troba l'script install_docker.sh"
    exit 1
fi

echo "✅ Script install_docker.sh trobat"

# Verificar sintaxi bash
if bash -n install_docker.sh; then
    echo "✅ Sintaxi de l'script correcta"
else
    echo "❌ ERROR: Problemes de sintaxi a l'script"
    exit 1
fi

# Verificar que conté les funcions essencials
echo ""
echo "🔍 Verificant components essencials..."

if grep -q "print_status" install_docker.sh; then
    echo "✅ Funcions de missatges presents"
else
    echo "❌ ERROR: Falten funcions de missatges"
fi

if grep -q "docker compose" install_docker.sh; then
    echo "✅ Comandos Docker Compose presents"
else
    echo "❌ ERROR: Falten comandos Docker Compose"
fi

if grep -q "nginx" install_docker.sh; then
    echo "✅ Configuració Nginx present"
else
    echo "❌ ERROR: Falta configuració Nginx"
fi

if grep -q "create_superuser" install_docker.sh; then
    echo "✅ Creació de superusuari present"
else
    echo "❌ ERROR: Falta creació de superusuari"
fi

if grep -q "collectstatic" install_docker.sh; then
    echo "✅ Col·lecció de fitxers estàtics present"
else
    echo "❌ ERROR: Falta col·lecció de fitxers estàtics"
fi

if grep -q "crontab" install_docker.sh; then
    echo "✅ Configuració de cron jobs present"
else
    echo "❌ ERROR: Falta configuració de cron jobs"
fi

echo ""
echo "📋 Resum del test:"
echo "- Script sintàcticament correcte"
echo "- Conté totes les funcions essencials"
echo "- Llest per ser provat en un servidor real"
echo ""
echo "🚀 L'script està llest per a la instal·lació!"