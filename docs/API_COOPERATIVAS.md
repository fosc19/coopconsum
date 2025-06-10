# 🌐 API para Cooperativas - La Civada

## 📋 Descripción

API REST pública que permite a otras cooperativas acceder a información sobre nuestros proveedores, productos y eventos. Diseñada para facilitar el intercambio de información entre cooperativas de consumo.

## 🚀 Endpoints Disponibles

### 📊 Información General
```
GET /api/
```
Devuelve información básica de la API y lista de endpoints disponibles.

### 🏪 Proveedores
```
GET /api/proveedores/
GET /api/proveedores/{id}/
```
**Filtros disponibles:**
- `visible_en_web`: true/false
- `visible_en_inicio`: true/false

**Búsqueda:**
- `search`: Busca en nombre y descripción

**Campos devueltos:**
```json
{
  "id": 1,
  "nombre": "Nombre del Proveedor",
  "descripcion": "Descripción del proveedor",
  "contacto": "info@proveedor.com",
  "imagen": "/media/proveedores/imagen.jpg",
  "visible_en_web": true,
  "visible_en_inicio": false
}
```

### 🛒 Productos
```
GET /api/productos/
GET /api/productos/{id}/
```
**Filtros disponibles:**
- `categoria`: ID de categoría
- `proveedor`: ID de proveedor
- `es_stock`: true/false
- `destacado_en_inicio`: true/false

**Búsqueda:**
- `search`: Busca en nombre, descripción y nombre del proveedor

**Campos devueltos:**
```json
{
  "id": 1,
  "nombre": "Nombre del Producto",
  "descripcion": "Descripción del producto",
  "precio": "12.50",
  "unidad_venta": "kg",
  "unidad_venta_display": "Kilogramo",
  "categoria": {
    "id": 1,
    "nombre": "Verduras",
    "descripcion": "Verduras frescas"
  },
  "proveedor": {
    "id": 1,
    "nombre": "Proveedor Local"
  },
  "imagen": "/media/productos/imagen.jpg",
  "es_stock": false,
  "destacado_en_inicio": true
}
```

### 📂 Categorías
```
GET /api/categorias/
GET /api/categorias/{id}/
```
**Búsqueda:**
- `search`: Busca en nombre y descripción

**Campos devueltos:**
```json
{
  "id": 1,
  "nombre": "Verduras",
  "descripcion": "Verduras frescas de temporada"
}
```

### 📅 Eventos
```
GET /api/eventos/
GET /api/eventos/{id}/
```
**Filtros disponibles:**
- `publico`: true/false
- `todo_el_dia`: true/false
- `fecha_inicio`: YYYY-MM-DD
- `fecha_fin`: YYYY-MM-DD

**Búsqueda:**
- `search`: Busca en título y descripción

**Campos devueltos:**
```json
{
  "id": 1,
  "titulo": "Asamblea General",
  "descripcion": "Asamblea mensual de la cooperativa",
  "fecha_inicio": "2025-01-15T18:00:00Z",
  "fecha_fin": "2025-01-15T20:00:00Z",
  "todo_el_dia": false,
  "color": "#28a745",
  "publico": true
}
```

## 🔍 Ejemplos de Uso

### Obtener todos los proveedores visibles
```bash
curl "http://lacivada.com/api/proveedores/?visible_en_web=true"
```

### Buscar productos de una categoría específica
```bash
curl "http://lacivada.com/api/productos/?categoria=1"
```

### Buscar productos por texto
```bash
curl "http://lacivada.com/api/productos/?search=tomate"
```

### Obtener eventos públicos del próximo mes
```bash
curl "http://lacivada.com/api/eventos/?publico=true&fecha_inicio=2025-01-01"
```

## 📄 Paginación

Todos los endpoints están paginados con 20 elementos por página:

```json
{
  "count": 45,
  "next": "http://lacivada.com/api/productos/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🔒 Autenticación

La API es **pública** y no requiere autenticación. Solo se muestran datos marcados como públicos/visibles.

## 🌍 CORS

La API permite peticiones desde cualquier origen para facilitar el acceso desde otras cooperativas.

## 📊 Límites de Uso

- **100 peticiones por hora** por IP
- Solo datos públicos disponibles
- Sin acceso a información sensible

## 🔧 Integración con Otras Cooperativas

### Ejemplo JavaScript
```javascript
// Obtener proveedores de La Civada
fetch('http://lacivada.com/api/proveedores/')
  .then(response => response.json())
  .then(data => {
    console.log('Proveedores disponibles:', data.results);
  });
```

### Ejemplo Python
```python
import requests

# Obtener productos destacados
response = requests.get('http://lacivada.com/api/productos/?destacado_en_inicio=true')
productos = response.json()

for producto in productos['results']:
    print(f"{producto['nombre']} - {producto['precio']}€")
```

## 🚀 Próximas Funcionalidades

- [ ] Webhook para notificaciones de nuevos productos
- [ ] API de disponibilidad de stock en tiempo real
- [ ] Integración con sistema de pedidos colaborativos
- [ ] Red federada de cooperativas

## 📞 Contacto

Para más información sobre la API o para añadir tu cooperativa a la red:
- Email: api@lacivada.com
- Web: https://lacivada.com
- GitHub: https://github.com/fosc19/lacivada