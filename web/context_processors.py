from django.core.cache import cache
from .models import ConfiguracioWeb

def configuracio_web(request):
    """Afegeix la configuració web a tots els templates amb cache optimitzat"""
    # Intentar obtenir configuració del cache primer
    config = cache.get('configuracio_web_cached')
    
    if config is None:
        # Si no està al cache, consultar BD i guardar al cache
        try:
            config = ConfiguracioWeb.objects.first()
            # Cache per 1 hora (3600 segons) - evita queries repetides
            cache.set('configuracio_web_cached', config, 3600)
        except ConfiguracioWeb.DoesNotExist:
            config = None
            # Cache també el valor None per evitar queries repetides quan no existeix
            cache.set('configuracio_web_cached', None, 300)  # 5 minuts per None
    
    return {
        'configuracio_web': config,
        'config': config  # També com a 'config' per compatibilitat amb templates
    }