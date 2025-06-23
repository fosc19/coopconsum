from django.shortcuts import render
from productos.models import Proveedor, Producto

def home(request):
    # Obtener los proveedores marcados como visibles en la página de inicio
    proveedores_destacados = Proveedor.objects.filter(visible_en_inicio=True).order_by('nombre')
    
    # Obtener los productos marcados como destacados en la página de inicio
    productos_destacados = Producto.objects.filter(destacado_en_inicio=True).order_by('nombre')
    
    # Opcional: obtener algunos productos de cada proveedor
    productos_por_proveedor = {}
    for proveedor in proveedores_destacados:
        productos_por_proveedor[proveedor.id] = Producto.objects.filter(proveedor=proveedor)[:3]  # Limitar a 3 productos por proveedor
    
    context = {
        'proveedores_destacados': proveedores_destacados,
        'productos_por_proveedor': productos_por_proveedor,
        'productos_destacados': productos_destacados
    }
    
    return render(request, 'web/home.html', context)

def quienes_somos(request):
    return render(request, 'web/quienes_somos.html')

from productos.models import Proveedor, Producto, Categoria # Añadir Categoria

def productores(request):
    categorias = Categoria.objects.all().order_by('nombre')
    productores_qs = Proveedor.objects.filter(visible_en_web=True)

    categoria_seleccionada_id = request.GET.get('categoria')
    categoria_seleccionada = None

    if categoria_seleccionada_id:
        try:
            categoria_seleccionada = Categoria.objects.get(id=categoria_seleccionada_id)
            # Filtrar productores que tienen al menos un producto en la categoría seleccionada
            productores_qs = productores_qs.filter(producto__categoria=categoria_seleccionada).distinct()
        except Categoria.DoesNotExist:
            # Si la categoría no existe, no se aplica filtro o se muestra un error (aquí no se aplica filtro)
            pass

    productores = productores_qs.order_by('nombre')
    
    # Opcional: productos por productor (podría optimizarse si solo se necesitan para la vista)
    productos_por_proveedor = {}
    for proveedor in productores:
        # Si hay una categoría seleccionada, podríamos querer mostrar solo productos de esa categoría para ese proveedor
        if categoria_seleccionada:
            productos_por_proveedor[proveedor.id] = Producto.objects.filter(proveedor=proveedor, categoria=categoria_seleccionada)
        else:
            productos_por_proveedor[proveedor.id] = Producto.objects.filter(proveedor=proveedor)
            
    context = {
        'productores': productores,
        'productos_por_proveedor': productos_por_proveedor,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada
    }
    return render(request, 'web/productores.html', context)

from productos.models import Categoria, Producto # Esta línea ya está, pero la lógica de arriba la usa

from productos.models import Categoria

def productos(request):
    categorias = Categoria.objects.all().order_by('nombre')
    categoria_id = request.GET.get('categoria')
    productos = Producto.objects.all().order_by('nombre')
    categoria_seleccionada = None
    if categoria_id:
        try:
            categoria_seleccionada = Categoria.objects.get(id=categoria_id)
            productos = productos.filter(categoria=categoria_seleccionada)
        except Categoria.DoesNotExist:
            categoria_seleccionada = None
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    }
    return render(request, 'web/productos.html', context)

def contacto(request):
    return render(request, 'web/contacto.html')

def com_apuntarse(request):
    """Vista para la página 'Com apuntar-te'."""
    return render(request, 'web/com_apuntarse.html')

from web.models import GaleriaCategoria, GaleriaImagen

def galeria(request):
    categorias = GaleriaCategoria.objects.all().order_by('-fecha_creacion', 'nombre')
    categoria_id = request.GET.get('categoria')
    imagenes = GaleriaImagen.objects.all().order_by('-fecha_subida')
    categoria_seleccionada = None
    if categoria_id:
        try:
            categoria_seleccionada = GaleriaCategoria.objects.get(id=categoria_id)
            imagenes = imagenes.filter(categoria=categoria_seleccionada)
        except GaleriaCategoria.DoesNotExist:
            categoria_seleccionada = None
    context = {
        'imagenes': imagenes,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    }
    return render(request, 'web/galeria.html', context)
def cooperatives(request):
    """Vista para la página de cooperativas - código abierto y API."""
    return render(request, 'web/cooperatives.html')

def ajuda(request):
    """Vista para la página de ayuda interactiva."""
    return render(request, 'web/ajuda.html')