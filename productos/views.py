# productos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden # Para devolver error si no tiene permisos
from .models import Producto, Categoria, Proveedor
from .forms import ProductoForm
from socios.models import Socio # Necesitamos Socio para comprobar permisos

# --- Comprobación de permisos ---
def puede_gestionar_productos(user):
    """Comprueba si el usuario puede gestionar productos."""
    if user.is_superuser:
        return True
    try:
        # Comprueba si el usuario tiene un perfil de socio asociado
        # y si ese socio tiene el permiso gestiona_productos
        return user.socio.gestiona_productos
    except Socio.DoesNotExist:
        # Si el usuario no tiene perfil de socio, no puede gestionar productos
        # (a menos que sea superusuario, ya comprobado arriba)
        return False
    except AttributeError:
         # Si el usuario no está logueado o no tiene el atributo 'socio'
         return False


def index(request):
    """ Muestra los productos, opcionalmente filtrados por categoría o proveedor. """
    productos = Producto.objects.select_related('categoria', 'proveedor').all() # Optimizar consulta
    categorias = Categoria.objects.order_by('nombre')
    proveedores = Proveedor.objects.order_by('nombre')

    categoria_seleccionada = None
    proveedor_seleccionado = None

    # Obtener IDs de los parámetros GET
    categoria_id = request.GET.get('categoria_id')
    proveedor_id = request.GET.get('proveedor_id')

    # Aplicar filtro de categoría si se proporciona
    if categoria_id:
        try:
            categoria_id = int(categoria_id)
            productos = productos.filter(categoria_id=categoria_id)
            categoria_seleccionada = Categoria.objects.get(id=categoria_id) # Para mostrar en la plantilla
        except (ValueError, Categoria.DoesNotExist):
            # Ignorar ID inválido o no encontrado, mostrar todos
            pass

    # Aplicar filtro de proveedor si se proporciona
    elif proveedor_id: # Usamos elif para que no se apliquen ambos filtros a la vez (decisión de diseño, se podría cambiar)
        try:
            proveedor_id = int(proveedor_id)
            productos = productos.filter(proveedor_id=proveedor_id)
            proveedor_seleccionado = Proveedor.objects.get(id=proveedor_id) # Para mostrar en la plantilla
        except (ValueError, Proveedor.DoesNotExist):
            # Ignorar ID inválido o no encontrado, mostrar todos
            pass

    context = {
        'productos': productos,
        'categorias': categorias,
        'proveedores': proveedores,
        'categoria_seleccionada': categoria_seleccionada,
        'proveedor_seleccionado': proveedor_seleccionado,
    }
    return render(request, 'productos/index.html', context)

def lista_categorias(request):
    """ Muestra todas las categorías """
    categorias = Categoria.objects.all()
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

def productos_de_categoria(request, cat_id):
    """ Muestra los productos filtrados por categoría """
    categoria = get_object_or_404(Categoria, id=cat_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos/productos_de_categoria.html', {
        'categoria': categoria,
        'productos': productos,
    })

# --- Vistas de Gestión de Productos ---

@login_required
@user_passes_test(puede_gestionar_productos, login_url='/login/', redirect_field_name=None) # Redirige a login si no cumple
def crear_producto(request):
    """ Vista para crear un nuevo producto """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirigir a la lista de productos o a donde sea apropiado
            return redirect('productos:index') # Asumiendo que tienes una URL nombrada 'index' en tu app productos
    else:
        form = ProductoForm()
    return render(request, 'productos/gestion_form_producto.html', {'form': form, 'titulo': 'Crear Nuevo Producto'})

@login_required
@user_passes_test(puede_gestionar_productos, login_url='/login/', redirect_field_name=None)
def editar_producto(request, prod_id):
    """ Vista para editar un producto existente """
    producto = get_object_or_404(Producto, id=prod_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:index') # O redirigir a la vista detalle del producto si existe
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/gestion_form_producto.html', {'form': form, 'titulo': f'Editar {producto.nombre}', 'producto': producto})

# Podrías añadir una vista para eliminar productos también si es necesario
# @login_required
# @user_passes_test(puede_gestionar_productos)
# def eliminar_producto(request, prod_id):
#     producto = get_object_or_404(Producto, id=prod_id)
#     if request.method == 'POST': # Confirmación de eliminación
#         producto.delete()
#         return redirect('productos:index')
#     # Considera añadir una plantilla de confirmación
#     return render(request, 'productos/confirmar_eliminar_producto.html', {'producto': producto})

def lista_proveedores(request):
    """ Muestra todos los proveedores (sin datos de contacto) """
    proveedores = Proveedor.objects.all()
    return render(request, 'productos/lista_proveedores.html', {'proveedores': proveedores})

def productos_de_proveedor(request, prov_id):
    """ Muestra los productos de un proveedor concreto """
    proveedor = get_object_or_404(Proveedor, id=prov_id)
    productos = Producto.objects.filter(proveedor=proveedor)
    return render(request, 'productos/productos_de_proveedor.html', {
        'proveedor': proveedor,
        'productos': productos,
    })
