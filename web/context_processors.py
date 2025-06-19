from .models import ConfiguracioWeb

def configuracio_web(request):
    """Afegeix la configuració web a tots els templates"""
    try:
        config = ConfiguracioWeb.objects.first()
        return {
            'configuracio_web': config,
            'config': config  # També com a 'config' per compatibilitat amb templates
        }
    except ConfiguracioWeb.DoesNotExist:
        return {
            'configuracio_web': None,
            'config': None
        }