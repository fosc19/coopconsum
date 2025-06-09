# Script PowerShell per provar la instal·lació Docker al VPS de test
# IP: 57.129.134.84

Write-Host "=== PROVA D'INSTAL·LACIÓ DOCKER ===" -ForegroundColor Green
Write-Host "VPS Test: 57.129.134.84"
Write-Host "Data: $(Get-Date)"
Write-Host ""

# Verificar si ssh està disponible
try {
    Write-Host "1. Verificant connexió SSH..." -ForegroundColor Yellow
    $result = ssh -o StrictHostKeyChecking=no root@57.129.134.84 'echo "Connexió SSH OK"'
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "ERROR: No es pot connectar per SSH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. Verificant sistema operatiu..." -ForegroundColor Yellow
ssh root@57.129.134.84 'cat /etc/os-release | head -5'

Write-Host ""
Write-Host "3. Verificant serveis actius (per no trencar res)..." -ForegroundColor Yellow
ssh root@57.129.134.84 'systemctl list-units --type=service --state=running | grep -E "(nginx|apache|mysql|postgresql|docker)" || echo "Cap servei web/db detectat"'

Write-Host ""
Write-Host "4. Verificant si Docker ja està instal·lat..." -ForegroundColor Yellow
ssh root@57.129.134.84 'docker --version 2>/dev/null || echo "Docker no instal·lat"'

Write-Host ""
Write-Host "5. Verificant espai disponible..." -ForegroundColor Yellow
ssh root@57.129.134.84 'df -h /'

Write-Host ""
Write-Host "6. Verificant ports ocupats..." -ForegroundColor Yellow
ssh root@57.129.134.84 'netstat -tlnp | grep -E ":80|:443|:3000|:8000" || echo "Ports web lliures"'

Write-Host ""
Write-Host "=== ANÀLISI COMPLETAT ===" -ForegroundColor Green
Write-Host "Si tot sembla segur, podem procedir amb la instal·lació Docker"