# Projecte Coopconsum

## Descripció
Sistema de gestió cooperativa desenvolupat amb Django per gestionar socis, comandes, productes i stock.

## Informació del servidor VPS
- **IP**: 57.129.134.84
- **Ubicació aplicació**: /var/www/coopconsum
- **Claude Code disponible**: Sí, es pot usar per diagnosticar problemes i executar comandes
- **Docker compose**: Gestiona contenidors web, db i cron

## Configuració logout
- **Admin logout**: `/admin/logout/` → redirigeix a `/admin/`
- **Intranet logout**: `/sortir/` → redirigeix a `/` (web pública)

## Comandaments útils per VPS
```bash
cd /var/www/coopconsum
git pull origin master
docker compose restart
docker compose logs web --tail 20
curl -I http://57.129.134.84/sortir/
```

## Estructura aplicació
- `coopconsum/` - Configuració principal Django
- `web/` - Web pública/escaparate
- `socios/` - Gestió socis i comptes
- `pedidos/` - Sistema comandes
- `productos/` - Catàleg productes
- `stock/` - Gestió inventari

## Notes tècniques
- Cron job comandes: 23:58 diàriament per crear comandes esporàdiques
- Base dades: PostgreSQL
- Servidor web: Gunicorn + Docker