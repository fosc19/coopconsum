from django.contrib import admin
from django.urls import path, include
from coopconsum.views import panel_principal
from django.contrib.auth.views import LogoutView  # Importación para logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web pública (escaparate/tienda)
    path('', include('web.urls')),

    # Dashboard/intranet
    path('dashboard/', panel_principal, name='dashboard_principal'),

    # Login con plantilla personalizada
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout con nombre 'logout'
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Rutas de tus apps de intranet
    path('pedidos/', include('pedidos.urls')),
    path('socios/', include('socios.urls')),
    path('productos/', include('productos.urls')),
    path('stock/', include('stock.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
