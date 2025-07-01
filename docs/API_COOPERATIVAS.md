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
GET /api/proveidors/
GET /api/proveidors/{id}/
```
**Cerca:**
- `search`: Cerca en nom i descripció

**Camps retornats:**
```json
{
  "id": 1,
  "nom": "La Rural de Collserola",
  "descripcio_curta": "Cooperativa agroecològica",
  "contacte": "info@larural.com",
  "email": "info@larural.com",
  "direccio": "Valldoreix, Barcelona",
  "imatge": "/media/proveedores/larural.jpg"
}
```

### 🛒 Productes
```
GET /api/productes/
GET /api/productes/{id}/
```
**Filtres disponibles:**
- `categoria`: ID de categoria
- `proveedor`: ID de proveïdor

**Cerca:**
- `search`: Cerca en nom, descripció i nom del proveïdor

**Camps retornats:**
```json
{
  "id": 1,
  "nom": "Pa integral",
  "descripcio": "Pa ecològic de farina integral de proximitat",
  "categoria": {
    "id": 1,
    "nom": "Pa",
    "descripcio": "Pans ecològics"
  },
  "proveidor": {
    "id": 1,
    "nom": "La Rural de Collserola",
    "descripcio_curta": "Cooperativa agroecològica",
    "contacte": "info@larural.com",
    "email": "info@larural.com",
    "direccio": "Valldoreix, Barcelona",
    "imatge": "/media/proveedores/larural.jpg"
  },
  "imatge": "/media/productos/pa_integral.jpg"
}
```

### 📂 Categories
```
GET /api/categories/
GET /api/categories/{id}/
```
**Cerca:**
- `search`: Cerca en nom i descripció

**Camps retornats:**
```json
{
  "id": 1,
  "nom": "Pa",
  "descripcio": "Pans ecològics de temporada"
}
```

### 📅 Esdeveniments
```
GET /api/esdeveniments/
GET /api/esdeveniments/{id}/
```
**Cerca:**
- `search`: Cerca en títol i descripció

**Camps retornats:**
```json
{
  "id": 1,
  "titol": "Assemblea General",
  "descripcio": "Reunió mensual de la cooperativa",
  "data": "2025-01-15"
}
```

## 🔍 Exemples d'Ús

### Obtenir tots els proveïdors
```bash
curl "http://civada.net/api/proveidors/"
```

### Buscar productes d'una categoria específica
```bash
curl "http://civada.net/api/productes/?categoria=1"
```

### Buscar productes per text
```bash
curl "http://civada.net/api/productes/?search=tomàquet"
```

### Obtenir esdeveniments del calendari
```bash
curl "http://civada.net/api/esdeveniments/"
```

## 📄 Paginació

Tots els endpoints estan paginats amb 20 elements per pàgina:

```json
{
  "count": 45,
  "next": "http://civada.net/api/productes/?page=2",
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
fetch('http://civada.net/api/proveidors/')
  .then(response => response.json())
  .then(data => {
    console.log('Proveïdors disponibles:', data.results);
    data.results.forEach(proveidor => {
      console.log(`${proveidor.nom} - ${proveidor.contacte}`);
    });
  });
```

### Exemple Python
```python
import requests

# Obtenir tots els productes
response = requests.get('http://civada.net/api/productes/')
productes = response.json()

for producte in productes['results']:
    print(f"{producte['nom']} de {producte['proveidor']['nom']}")
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