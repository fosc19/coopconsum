#!/usr/bin/env python
"""
Script de diagnóstico para verificar el funcionamiento del sistema de ingresos.
Ejecutar con: python manage.py shell < diagnostico_ingreso.py
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coopconsum.settings')
django.setup()

from django.contrib.auth.models import User
from socios.models import Socio, CuentaSocio, MovimientoCuenta
from django.db import connection

def diagnostico_completo():
    print("=== DIAGNÓSTICO DEL SISTEMA DE INGRESOS ===\n")
    
    # 1. Verificar configuración de base de datos
    print("1. CONFIGURACIÓN DE BASE DE DATOS:")
    print(f"   Motor: {connection.vendor}")
    print(f"   Base de datos: {connection.settings_dict.get('NAME', 'N/A')}")
    print(f"   Host: {connection.settings_dict.get('HOST', 'localhost')}")
    print(f"   Puerto: {connection.settings_dict.get('PORT', 'N/A')}")
    print()
    
    # 2. Verificar estructura de tablas
    print("2. VERIFICACIÓN DE TABLAS:")
    with connection.cursor() as cursor:
        # Verificar tabla MovimientoCuenta
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'socios_movimientocuenta'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        if columns:
            print("   Tabla socios_movimientocuenta:")
            for col in columns:
                print(f"     - {col[0]}: {col[1]} (NULL: {col[2]}, Default: {col[3]})")
        else:
            print("   ⚠️  Tabla socios_movimientocuenta no encontrada")
    print()
    
    # 3. Verificar usuarios y socios
    print("3. VERIFICACIÓN DE USUARIOS Y SOCIOS:")
    total_users = User.objects.count()
    total_socios = Socio.objects.count()
    users_with_socio = User.objects.filter(socio__isnull=False).count()
    
    print(f"   Total usuarios: {total_users}")
    print(f"   Total socios: {total_socios}")
    print(f"   Usuarios con perfil de socio: {users_with_socio}")
    
    # Verificar usuarios sin perfil de socio
    users_without_socio = User.objects.filter(socio__isnull=True)
    if users_without_socio.exists():
        print("   ⚠️  Usuarios sin perfil de socio:")
        for user in users_without_socio[:5]:  # Mostrar solo los primeros 5
            print(f"     - {user.username} ({user.email})")
    print()
    
    # 4. Verificar cuentas de socios
    print("4. VERIFICACIÓN DE CUENTAS:")
    total_cuentas = CuentaSocio.objects.count()
    socios_sin_cuenta = Socio.objects.filter(cuentasocio__isnull=True).count()
    
    print(f"   Total cuentas: {total_cuentas}")
    print(f"   Socios sin cuenta: {socios_sin_cuenta}")
    
    if socios_sin_cuenta > 0:
        print("   ⚠️  Socios sin cuenta (se crearán automáticamente al enviar ingreso):")
        socios_sin_cuenta_obj = Socio.objects.filter(cuentasocio__isnull=True)[:5]
        for socio in socios_sin_cuenta_obj:
            print(f"     - {socio.nombre} {socio.apellido}")
    print()
    
    # 5. Verificar movimientos recientes
    print("5. MOVIMIENTOS RECIENTES:")
    movimientos_recientes = MovimientoCuenta.objects.order_by('-fecha')[:10]
    
    if movimientos_recientes:
        print("   Últimos 10 movimientos:")
        for mov in movimientos_recientes:
            print(f"     - {mov.fecha.strftime('%Y-%m-%d %H:%M')} | {mov.tipo_movimiento} | {mov.monto}€ | {mov.estado}")
    else:
        print("   No hay movimientos registrados")
    print()
    
    # 6. Verificar movimientos pendientes
    print("6. MOVIMIENTOS PENDIENTES:")
    pendientes = MovimientoCuenta.objects.filter(estado='pendiente').count()
    print(f"   Total pendientes: {pendientes}")
    
    if pendientes > 0:
        movimientos_pendientes = MovimientoCuenta.objects.filter(estado='pendiente').order_by('-fecha')[:5]
        print("   Últimos 5 pendientes:")
        for mov in movimientos_pendientes:
            socio_nombre = f"{mov.cuenta.socio.nombre} {mov.cuenta.socio.apellido}"
            print(f"     - {mov.fecha.strftime('%Y-%m-%d %H:%M')} | {socio_nombre} | {mov.monto}€")
    print()
    
    # 7. Test de creación de movimiento
    print("7. TEST DE CREACIÓN DE MOVIMIENTO:")
    try:
        # Buscar un socio para hacer el test
        socio_test = Socio.objects.first()
        if socio_test:
            print(f"   Usando socio de prueba: {socio_test.nombre} {socio_test.apellido}")
            
            # Obtener o crear cuenta
            cuenta, created = CuentaSocio.objects.get_or_create(socio=socio_test)
            if created:
                print("   ✓ Cuenta creada automáticamente")
            else:
                print("   ✓ Cuenta ya existía")
            
            # Intentar crear un movimiento de prueba (sin guardarlo)
            movimiento_test = MovimientoCuenta(
                cuenta=cuenta,
                tipo_movimiento="test_ingreso",
                monto=Decimal('10.50'),
                descripcion="Test de diagnóstico - UF123",
                estado="pendiente"
            )
            
            # Validar sin guardar
            movimiento_test.full_clean()
            print("   ✓ Validación del movimiento exitosa")
            print("   ✓ El sistema puede crear movimientos correctamente")
            
        else:
            print("   ⚠️  No hay socios en el sistema para hacer el test")
            
    except Exception as e:
        print(f"   ❌ Error en test de creación: {e}")
    print()
    
    print("=== FIN DEL DIAGNÓSTICO ===")
    print("\nSi hay errores en el servidor VPS, revisa:")
    print("1. Los logs en /logs/django.log")
    print("2. La configuración de la base de datos")
    print("3. Los permisos de escritura en la base de datos")
    print("4. Las migraciones aplicadas")

if __name__ == "__main__":
    diagnostico_completo()
