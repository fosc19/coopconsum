from django.contrib import admin
from django.urls import path, include

# Import directe de la vista de logout
def simple_logout_view(request):
    from django.contrib.auth import logout
    from django.http import HttpResponseRedirect
    logout(request)
    return HttpResponseRedirect('/')

# Vista logout específica per admin
def admin_logout_view(request):
    from django.contrib.auth import logout
    from django.http import HttpResponseRedirect
    logout(request)
    return HttpResponseRedirect('/admin/login/')

# Funcions wrapper per imports locals de vistes
def panel_principal_view(request):
    from coopconsum.views import panel_principal
    return panel_principal(request)

def master_control_wrapper(request):
    from coopconsum.views import master_control_view
    return master_control_view(request)

def registrar_compra_wrapper(request):
    from coopconsum.views import registrar_compra_socio_view
    return registrar_compra_socio_view(request)
from django.contrib.auth.views import LogoutView  # Importación para logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

urlpatterns = [
    # Logout funcional sense imports problemàtics - PRIMER per prioritat
    path('sortir/', simple_logout_view, name='logout'),
    # Test logout amb nom diferent
    path('test-logout-final/', simple_logout_view, name='test_logout_final'),
    
    # Logout específic per admin - ABANS d'admin/ per prioritat
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    
    # Ajuda específica per admin - ABANS d'admin/ per prioritat
    path('admin/ajuda/', lambda request: __import__('web.views', fromlist=['ajuda_admin']).ajuda_admin(request), name='admin_ajuda'),
    
    path('admin/', admin.site.urls),

    # Web pública (escaparate/tienda)
    path('', include('web.urls')),

    # Dashboard/intranet
    path('dashboard/', panel_principal_view, name='dashboard_principal'),

    # Rutas para la sección Master
    path('master/', master_control_wrapper, name='master_control'), # Vista principal de Master (redirige)
    path('master/registrar-compra/', registrar_compra_wrapper, name='registrar_compra_socio'), # Vista para registrar compra

    # Login con plantilla personalizada
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Rutas de autenticación de Django (password_change, password_reset, etc. SENSE logout)
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Rutas de tus apps de intranet
    path('pedidos/', include('pedidos.urls')),
    path('socios/', include('socios.urls')),
    path('productos/', include('productos.urls')),
    path('stock/', include('stock.urls')),
    # Rutas para la nueva app de eventos
    path('eventos/', include('eventos.urls')),
    
    # CKEditor URLs per editor WYSIWYG (temporalment comentat)
    # path('ckeditor/', include('ckeditor.urls')),
    
    # API para cooperativas
    path('api/', include('api.urls')),
]

# Configurar Django admin
admin.site.site_url = '/'

# Servir fitxers media tant en desenvolupament com en producció
# Necessari per imatges pujades via admin (productes, configuració web, etc.)
from django.views.static import serve
from django.urls import re_path
import os

# Afegir ruta per servir fitxers media
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
