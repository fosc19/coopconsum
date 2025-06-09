#!/bin/bash

# Script per provar la instal·lació Docker al VPS de test
# IP: 57.129.134.84
# Aquest script és segur i no modifica res existent

echo "=== PROVA D'INSTAL·LACIÓ DOCKER ==="
echo "VPS Test: 57.129.134.84"
echo "Data: $(date)"
echo ""

# Verificar connexió SSH
echo "1. Verificant connexió SSH..."
ssh -o StrictHostKeyChecking=no root@57.129.134.84 'echo "Connexió SSH OK"' || {
    echo "ERROR: No es pot connectar per SSH"
    exit 1
}

echo ""
echo "2. Verificant sistema operatiu..."
ssh root@57.129.134.84 'cat /etc/os-release | head -5'

echo ""
echo "3. Verificant serveis actius (per no trencar res)..."
ssh root@57.129.134.84 'systemctl list-units --type=service --state=running | grep -E "(nginx|apache|mysql|postgresql|docker)" || echo "Cap servei web/db detectat"'

echo ""
echo "4. Verificant si Docker ja està instal·lat..."
ssh root@57.129.134.84 'docker --version 2>/dev/null || echo "Docker no instal·lat"'

echo ""
echo "5. Verificant espai disponible..."
ssh root@57.129.134.84 'df -h /'

echo ""
echo "6. Verificant ports ocupats..."
ssh root@57.129.134.84 'netstat -tlnp | grep -E ":80|:443|:3000|:8000" || echo "Ports web lliures"'

echo ""
echo "=== ANÀLISI COMPLETAT ==="
echo "Si tot sembla segur, podem procedir amb la instal·lació Docker"