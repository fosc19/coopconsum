#!/usr/bin/env python
"""
Script para instalar datos de ejemplo en CoopConsum
Ejecutar después de las migraciones iniciales
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coopconsum.settings')
django.setup()

from django.contrib.auth.models import User
from socios.models import Socio, Proveedor, Categoria, Producto

def create_sample_data():
    """Crear datos de ejemplo para demostración"""
    
    print("🚀 Instalando datos de ejemplo...")
    
    # Crear categorías de ejemplo
    categorias = [
        {'nombre': 'Frutas y Verduras', 'descripcion': 'Productos frescos de temporada'},
        {'nombre': 'Panadería', 'descripcion': 'Pan artesanal y productos de horno'},
        {'nombre': 'Lácteos', 'descripcion': 'Productos lácteos ecológicos'},
    ]
    
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        if created:
            print(f"✅ Categoría creada: {categoria.nombre}")
    
    # Crear proveedores de ejemplo
    proveedores = [
        {
            'nombre': 'Huerta Ecológica Local',
            'contacto': 'info@huertaecologica.com',
            'telefono': '93 123 45 67',
            'descripcion': 'Productor local de frutas y verduras ecológicas'
        },
        {
            'nombre': 'Panadería Artesanal',
            'contacto': 'hola@panaderia.com', 
            'telefono': '93 234 56 78',
            'descripcion': 'Pan artesanal con harinas ecológicas'
        }
    ]
    
    for prov_data in proveedores:
        proveedor, created = Proveedor.objects.get_or_create(
            nombre=prov_data['nombre'],
            defaults=prov_data
        )
        if created:
            print(f"✅ Proveedor creado: {proveedor.nombre}")
    
    # Crear productos de ejemplo
    productos = [
        {
            'nombre': 'Tomates ecológicos',
            'descripcion': 'Tomates de temporada cultivados sin pesticidas',
            'precio': 3.50,
            'categoria': 'Frutas y Verduras',
            'proveedor': 'Huerta Ecológica Local'
        },
        {
            'nombre': 'Pan integral',
            'descripcion': 'Pan integral con semillas, masa madre',
            'precio': 2.80,
            'categoria': 'Panadería', 
            'proveedor': 'Panadería Artesanal'
        },
        {
            'nombre': 'Lechuga ecológica',
            'descripcion': 'Lechuga fresca de cultivo ecológico',
            'precio': 1.50,
            'categoria': 'Frutas y Verduras',
            'proveedor': 'Huerta Ecológica Local'
        }
    ]
    
    for prod_data in productos:
        try:
            categoria = Categoria.objects.get(nombre=prod_data['categoria'])
            proveedor = Proveedor.objects.get(nombre=prod_data['proveedor'])
            
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'descripcion': prod_data['descripcion'],
                    'precio': prod_data['precio'],
                    'categoria': categoria,
                    'proveedor': proveedor,
                    'disponible': True
                }
            )
            if created:
                print(f"✅ Producto creado: {producto.nombre}")
        except Exception as e:
            print(f"❌ Error creando producto {prod_data['nombre']}: {e}")
    
    print("\n🎉 ¡Datos de ejemplo instalados correctamente!")
    print("📝 Puedes acceder al admin en: http://localhost:8000/admin/")
    print("🌐 Web pública en: http://localhost:8000/")
    print("🔗 API en: http://localhost:8000/api/")

if __name__ == '__main__':
    create_sample_data()