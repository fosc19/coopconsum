# productos/urls.py
from django.urls import path
from .views import (
    index, lista_categorias, productos_de_categoria,
    lista_proveedores, productos_de_proveedor,
    crear_producto, editar_producto # Añadir las nuevas vistas
    # , eliminar_producto # Descomentar si añades la vista de eliminar
)

app_name = 'productos' # Definir el namespace de la app

urlpatterns = [
    # URLs existentes
    path('', index, name='index'), # Cambiado a 'index' para coincidir con redirects
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categorias/<int:cat_id>/', productos_de_categoria, name='productos_de_categoria'),

    path('proveedores/', lista_proveedores, name='lista_proveedores'),
    path('proveedores/<int:prov_id>/', productos_de_proveedor, name='productos_de_proveedor'),

    # URLs para gestión de productos
    path('crear/', crear_producto, name='crear_producto'),
    path('editar/<int:prod_id>/', editar_producto, name='editar_producto'),
    # path('eliminar/<int:prod_id>/', eliminar_producto, name='eliminar_producto'), # Descomentar si añades la vista
]
