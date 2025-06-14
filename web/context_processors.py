from .models import ConfiguracioWeb

def configuracio_web(request):
    """Afegeix la configuració web a tots els templates"""
    try:
        config = ConfiguracioWeb.objects.first()
        return {
            'configuracio_web': config
        }
    except ConfiguracioWeb.DoesNotExist:
        return {
            'configuracio_web': None
        }