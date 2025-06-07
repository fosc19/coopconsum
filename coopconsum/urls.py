from django.contrib import admin
from django.urls import path, include
from coopconsum import views # Importar todas las vistas de coopconsum
from django.contrib.auth.views import LogoutView  # Importación para logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web pública (escaparate/tienda)
    path('', include('web.urls')),

    # Dashboard/intranet
    path('dashboard/', views.panel_principal, name='dashboard_principal'),

    # Rutas para la sección Master
    path('master/', views.master_control_view, name='master_control'), # Vista principal de Master (redirige)
    path('master/registrar-compra/', views.registrar_compra_socio_view, name='registrar_compra_socio'), # Vista para registrar compra

    # Login con plantilla personalizada
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout con nombre 'logout' - Usará LOGOUT_REDIRECT_URL de settings.py
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # Rutas de autenticación de Django (incluye password_change, password_reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Rutas de tus apps de intranet
    path('pedidos/', include('pedidos.urls')),
    path('socios/', include('socios.urls')),
    path('productos/', include('productos.urls')),
    path('stock/', include('stock.urls')),
    # Rutas para la nueva app de eventos
# API para cooperativas
    path('api/', include('api.urls')),
    path('eventos/', include('eventos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
