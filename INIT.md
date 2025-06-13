# Process per debugging Django amb VPS

## Workflow de desenvolupament
1. **Fer canvis en local** (aquest repositori)
2. **Commit i push** dels canvis
3. **Al VPS**: `git pull origin master && docker compose restart`
4. **Provar** les URLs/funcionalitats
5. **Si falla, repetir des del pas 1**

## SSH Access al VPS
- Server: `ubuntu@57.129.134.84`
- Key path: `/tmp/claude_new_key`
- Command: `ssh -i /tmp/claude_new_key ubuntu@57.129.134.84`

## Debugging URLs Django
```bash
# Test logout URL
curl -I http://57.129.134.84/sortir/

# Test Django URL loading
docker compose exec web python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coopconsum.settings')
django.setup()
from django.urls import reverse
print('Logout URL:', reverse('logout'))
"
```

## Problema actual: AppRegistryNotReady
- Django no pot carregar les URLs per imports problemàtics al views.py
- Cal moure tots els imports de models dins de les funcions
- Error específic: imports globals de socios.models causen problems