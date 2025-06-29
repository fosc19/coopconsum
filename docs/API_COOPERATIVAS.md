# 🌐 API per Cooperatives - La Civada

## 📋 Descripció

API REST pública que permet a altres cooperatives accedir a informació sobre els nostres proveïdors, productes i esdeveniments. Dissenyada per facilitar l'intercanvi d'informació entre cooperatives de consum.

## 🚀 Endpoints Disponibles

### 📊 Informació General
```
GET /api/
```
Retorna informació bàsica de l'API i llista d'endpoints disponibles.

### 🏪 Proveïdors
```
GET /api/proveedores/
GET /api/proveedores/{id}/
```
**Filtres disponibles:**
- `visible_en_web`: true/false
- `visible_en_inicio`: true/false

**Cerca:**
- `search`: Cerca en nom i descripció

**Camps retornats:**
```json
{
  "id": 1,
  "nombre": "Nom del Proveïdor",
  "descripcion": "Descripció del proveïdor",
  "contacto": "info@proveedor.com",
  "imagen": "/media/proveedores/imagen.jpg",
  "visible_en_web": true,
  "visible_en_inicio": false
}
```

### 🛒 Productes
```
GET /api/productos/
GET /api/productos/{id}/
```
**Filtres disponibles:**
- `categoria`: ID de categoria
- `proveedor`: ID de proveïdor
- `es_stock`: true/false
- `destacado_en_inicio`: true/false

**Cerca:**
- `search`: Cerca en nom, descripció i nom del proveïdor

**Camps retornats:**
```json
{
  "id": 1,
  "nombre": "Nom del Producte",
  "descripcion": "Descripció del producte",
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
    "nombre": "Proveïdor Local"
  },
  "imagen": "/media/productos/imagen.jpg",
  "es_stock": false,
  "destacado_en_inicio": true
}
```

### 📂 Categories
```
GET /api/categorias/
GET /api/categorias/{id}/
```
**Cerca:**
- `search`: Cerca en nom i descripció

**Camps retornats:
```json
{
  "id": 1,
  "nombre": "Verduras",
  "descripcion": "Verdures fresques de temporada"
}
```

### 📅 Esdeveniments
```
GET /api/eventos/
GET /api/eventos/{id}/
```
**Filtres disponibles:**
- `publico`: true/false
- `todo_el_dia`: true/false
- `fecha_inicio`: YYYY-MM-DD
- `fecha_fin`: YYYY-MM-DD

**Cerca:**
- `search`: Cerca en títol i descripció

**Camps retornats:
```json
{
  "id": 1,
  "titulo": "Assemblea General",
  "descripcion": "Assemblea mensual de la cooperativa",
  "fecha_inicio": "2025-01-15T18:00:00Z",
  "fecha_fin": "2025-01-15T20:00:00Z",
  "todo_el_dia": false,
  "color": "#28a745",
  "publico": true
}
```

## 🔍 Exemples d'Ús

### Obtenir tots els proveïdors visibles
```bash
curl "http://civada.net/api/proveedores/?visible_en_web=true"
```

### Buscar productes d'una categoria específica
```bash
curl "http://civada.net/api/productos/?categoria=1"
```

### Buscar productes per text
```bash
curl "http://civada.net/api/productos/?search=tomàquet"
```

### Obtenir esdeveniments públics del proper mes
```bash
curl "http://civada.net/api/eventos/?publico=true&fecha_inicio=2025-01-01"
```

## 📄 Paginació

Tots els endpoints estan paginats amb 20 elements per pàgina:

```json
{
  "count": 45,
  "next": "http://civada.net/api/productos/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🔒 Autenticació

L'API és **pública** i no requereix autenticació. Només es mostren dades marcades com a públiques/visibles.

## 🌍 CORS

L'API permet peticions des de qualsevol origen per facilitar l'accés des d'altres cooperatives.

## 📊 Límits d'Ús

- **100 peticions per hora** per IP (configurable per cooperativa)
- Només dades públiques disponibles
- Sense accés a informació sensible (preus interns, dades de socis)

## 🔧 Integració amb Altres Cooperatives

### Exemple JavaScript
```javascript
// Obtenir proveïdors de La Civada
fetch('http://civada.net/api/proveedores/')
  .then(response => response.json())
  .then(data => {
    console.log('Proveïdors disponibles:', data.results);
  });
```

### Exemple Python
```python
import requests

# Obtenir productes destacats
response = requests.get('http://civada.net/api/productos/?destacado_en_inicio=true')
productos = response.json()

for producto in productos['results']:
    print(f"{producto['nombre']} - {producto['precio']}€")
```

## 🚀 Properes Funcionalitats

- [ ] Webhook per notificacions de nous productes
- [ ] API de disponibilitat d'estoc en temps real
- [ ] Integració amb sistema de comandes col·laboratives
- [ ] Xarxa federada de cooperatives

## 📞 Contacte

Per més informació sobre l'API o per afegir la teva cooperativa a la xarxa:
- Web: https://civada.net
- GitHub: https://github.com/fosc19/coopconsum