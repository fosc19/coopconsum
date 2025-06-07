# stock/urls.py
from django.urls import path
from . import views

app_name = 'stock' # Definir el espacio de nombres de la aplicación

urlpatterns = [
    # Vista para la gestión de stock con filtros
    path('gestion/', views.gestion_stock_view, name='gestion_stock'),
    # Vista para mostrar todos los productos de stock (puede ser redundante o usarse para otra cosa)
    path('todos/', views.stock_todos_view, name='stock_todos'),
    # Vista para mostrar categorías con productos de stock
    path('categorias/', views.stock_categorias_view, name='stock_categorias'),
    # Vista para mostrar proveedores con productos de stock
    path('proveedores/', views.stock_proveedores_view, name='stock_proveedores'),
    path('categorias/<int:cat_id>/', views.stock_productos_de_categoria_view, name='stock_productos_de_categoria'),
    path('proveedores/<int:prov_id>/', views.stock_productos_de_proveedor_view, name='stock_productos_de_proveedor'),
    # URL para procesar la actualización de stock (solo POST)
    path('actualizar/', views.actualizar_stock_view, name='actualizar_stock'),
    # URL para validar un registro de compra (solo POST)
    path('validar-registro/<int:registro_id>/', views.validar_registro_compra_view, name='validar_registro_compra'),
]

