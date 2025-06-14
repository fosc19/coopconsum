from .models import ConfiguracioWeb

def configuracio_web(request):
    """Afegeix la configuració web a tots els templates"""
    try:
        config = ConfiguracioWeb.objects.first()
        return {
            'config': config
        }
    except ConfiguracioWeb.DoesNotExist:
        return {
            'config': None
        }