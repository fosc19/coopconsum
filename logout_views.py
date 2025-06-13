# Vista de logout simple sense imports problemàtics
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def simple_logout(request):
    """Vista de logout que accepta GET i POST requests sense CSRF"""
    # Import local per evitar AppRegistryNotReady
    from django.contrib.auth import logout
    
    logout(request)
    return HttpResponseRedirect('/')