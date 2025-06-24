# stock/views.py
from django.shortcuts import render, get_object_or_404, redirect # Añadir redirect
from django.urls import reverse # Añadir reverse
from django.db.models import Count, Q, F
from django.db import transaction # Para transacciones atómicas
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test # Importar decoradores de autenticación/permisos
from django.core.exceptions import PermissionDenied # Para manejar el acceso denegado si es necesario
from productos.models import Producto, Categoria, Proveedor
from socios.models import Socio, RegistroCompraSocio, CuentaSocio, MovimientoCuenta # Importar modelos necesarios

# Vista para mostrar todos los productos de stock
def stock_todos_view(request):
    categoria_id = request.GET.get('categoria_id')
    proveedor_id = request.GET.get('proveedor_id')

    productos_stock = Producto.objects.filter(es_stock=True).select_related('categoria', 'proveedor').order_by('nombre')
    
    categoria_seleccionada = None
    proveedor_seleccionado = None

    if categoria_id:
        productos_stock = productos_stock.filter(categoria_id=categoria_id)
        try:
            categoria_seleccionada = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            pass # o manejar el error si es necesario
    elif proveedor_id: # Usamos elif para que solo un filtro esté activo a la vez
        productos_stock = productos_stock.filter(proveedor_id=proveedor_id)
        try:
            proveedor_seleccionado = Proveedor.objects.get(id=proveedor_id)
        except Proveedor.DoesNotExist:
            pass # o manejar el error

    # Obtener todas las categorías y proveedores que tienen productos de stock para los filtros
    # Optimizamos para obtener solo los que realmente tienen productos de stock
    categorias_con_stock = Categoria.objects.filter(producto__es_stock=True).distinct().order_by('nombre')
    proveedores_con_stock = Proveedor.objects.filter(producto__es_stock=True).distinct().order_by('nombre')

    context = {
        'productos_stock': productos_stock,
        'categorias': categorias_con_stock,
        'proveedores': proveedores_con_stock,
        'categoria_seleccionada': categoria_seleccionada,
        'proveedor_seleccionado': proveedor_seleccionado,
    }
    return render(request, 'stock/stock_todos.html', context)

# Vista para mostrar categorías con productos de stock
def stock_categorias_view(request):
    # Obtenemos categorías que tienen al menos un producto de stock asociado
    categorias_con_stock = Categoria.objects.filter(
        producto__es_stock=True
    ).annotate(
        num_productos_stock=Count('producto')
    ).filter(num_productos_stock__gt=0).order_by('nombre')
    return render(request, 'stock/stock_categorias.html', {'categorias': categorias_con_stock})

# Vista para mostrar proveedores con productos de stock
def stock_proveedores_view(request):
    # Obtenemos proveedores que tienen al menos un producto de stock asociado
    proveedores_con_stock = Proveedor.objects.filter(
        producto__es_stock=True
    ).annotate(
        num_productos_stock=Count('producto')
    ).filter(num_productos_stock__gt=0).order_by('nombre')
    return render(request, 'stock/stock_proveedores.html', {'proveedores': proveedores_con_stock})
# Vista para mostrar productos de stock filtrados por proveedor
from django.shortcuts import get_object_or_404

def stock_productos_de_proveedor_view(request, prov_id):
    """Muestra los productos de stock filtrados por proveedor"""
    proveedor = get_object_or_404(Proveedor, id=prov_id)
    productos = Producto.objects.filter(proveedor=proveedor, es_stock=True)
    return render(request, 'stock/stock_productos_de_proveedor.html', {
        'proveedor': proveedor,
        # 'categoria': categoria, # Parece un error, proveedor_view no tiene categoría directa
        'productos': productos,
    })

# Función de comprobación de permisos
def puede_gestionar_stock(user):
    """Comprueba si el usuario es superusuario o el socio designado para gestionar stock."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        # Comprueba si el usuario está vinculado a un Socio y si ese Socio tiene el permiso
        return hasattr(user, 'socio') and user.socio is not None and user.socio.gestiona_stock
    except Socio.DoesNotExist: # El OneToOne puede no existir
        return False
    except AttributeError: # El usuario podría no tener el atributo 'socio'
        return False

# Nueva vista para la gestión de stock con filtros (protegida)
@login_required # Requiere que el usuario esté logueado
@user_passes_test(puede_gestionar_stock) # Requiere que pase la comprobación de permisos
def gestion_stock_view(request):
    """
    Muestra todos los productos de stock y permite filtrar por categoría y proveedor.
    Solo accesible por admin o socio gestor de stock.
    """
    # Obtener parámetros de filtro de la solicitud GET
    categoria_id = request.GET.get('categoria_id')
    proveedor_id = request.GET.get('proveedor_id')

    # Empezar con todos los productos de stock
    productos_list = Producto.objects.filter(es_stock=True).select_related('categoria', 'proveedor').order_by('nombre')

    # Aplicar filtros si se proporcionan
    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)
    if proveedor_id:
        productos_list = productos_list.filter(proveedor_id=proveedor_id)

    # Obtener todas las categorías y proveedores que tienen productos de stock para los filtros
    categorias_disponibles = Categoria.objects.filter(producto__es_stock=True).distinct().order_by('nombre')
    proveedores_disponibles = Proveedor.objects.filter(producto__es_stock=True).distinct().order_by('nombre')

    # Obtener los últimos registros de compras manuales para la segunda pestaña
    ultimos_registros_compras = RegistroCompraSocio.objects.select_related(
        'socio', 'producto', 'registrado_por'
    ).order_by('-fecha_registro')[:20] # Mostrar los últimos 20

    context = {
        'productos': productos_list,
        'categorias': categorias_disponibles,
        'proveedores': proveedores_disponibles,
        'selected_categoria': int(categoria_id) if categoria_id else None,
        'selected_proveedor': int(proveedor_id) if proveedor_id else None,
        'ultimos_registros_compras': ultimos_registros_compras, # Añadir registros al contexto
    }
    return render(request, 'stock/gestion_stock.html', context)

# Vista para mostrar productos de stock filtrados por categoría
from django.shortcuts import get_object_or_404

def stock_productos_de_categoria_view(request, cat_id):
    """Muestra los productos de stock filtrados por categoría"""
    categoria = get_object_or_404(Categoria, id=cat_id)
    productos = Producto.objects.filter(categoria=categoria, es_stock=True)
    return render(request, 'stock/stock_productos_de_categoria.html', {
        # 'categoria': categoria, # Línea duplicada, eliminar una
        'categoria': categoria,
        'productos': productos,
    })

@login_required # Requiere login
@user_passes_test(puede_gestionar_stock) # Requiere permisos
@require_POST # Asegura que esta vista solo acepta peticiones POST
def actualizar_stock_view(request):
    """
    Actualiza el stock de un producto específico basado en la cantidad enviada.
    Solo accesible por admin o socio gestor de stock.
    """
    producto_id = request.POST.get('producto_id')
    cantidad_str = request.POST.get('cantidad_cambio')
    categoria_id = request.POST.get('categoria_id') # Para mantener filtros
    proveedor_id = request.POST.get('proveedor_id') # Para mantener filtros

    # Construir la URL base de redirección con filtros
    redirect_url = reverse('stock:gestion_stock')
    query_params = {}
    if categoria_id:
        query_params['categoria_id'] = categoria_id
    if proveedor_id:
        query_params['proveedor_id'] = proveedor_id
    if query_params:
        redirect_url += '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])

    if not producto_id or cantidad_str is None:
        messages.error(request, "Manquen dades per actualitzar l'estoc.")
        return redirect(redirect_url) # Redirigir con filtros si es posible

    try:
        cantidad_cambio = int(cantidad_str)
        # Usamos select_for_update para bloquear la fila durante la transacción si es necesario,
        # aunque con F() no es estrictamente necesario para la suma atómica.
        # Lo dejamos fuera por simplicidad a menos que haya problemas de concurrencia complejos.
        producto = get_object_or_404(Producto, id=producto_id, es_stock=True)

        # Actualizar el stock usando F() para operaciones atómicas
        nuevo_stock_calculado = producto.stock + cantidad_cambio

        if nuevo_stock_calculado < 0:
             # Evitar stock negativo si es una regla de negocio
             messages.warning(request, f"Operació cancel·lada: L'estoc de '{producto.nombre}' no pot ser negatiu.")
        else:
            # Realizar la actualización atómica
            Producto.objects.filter(id=producto_id).update(stock=F('stock') + cantidad_cambio)
            # Refrescar el objeto para obtener el valor actualizado si se necesita mostrar
            # producto.refresh_from_db()
            messages.success(request, f"Estoc de '{producto.nombre}' actualitzat a {nuevo_stock_calculado}.")

    except ValueError:
        messages.error(request, "La quantitat introduïda ('{}') no és un número vàlid.".format(cantidad_str))
    except Producto.DoesNotExist:
         messages.error(request, "El producte que intentes actualitzar no existeix o no és gestionat com a estoc.")
    except Exception as e:
        # Captura genérica para otros posibles errores
        messages.error(request, f"Error inesperat en actualitzar l'estoc: {e}")

    # Redirigir siempre de vuelta a la página de gestión con los filtros aplicados
    return redirect(redirect_url)


@login_required
@user_passes_test(puede_gestionar_stock) # Solo usuarios con permiso
@require_POST # Solo aceptar POST
@transaction.atomic # Asegurar que la validación y el movimiento sean atómicos
def validar_registro_compra_view(request, registro_id):
    """
    Valida un registro de compra manual pendiente, calcula el costo
    y crea el movimiento correspondiente en la cuenta del socio.
    """
    # Obtener el registro o devolver 404
    registro = get_object_or_404(RegistroCompraSocio.objects.select_related('socio', 'producto'), id=registro_id)

    # Comprobar si ya está validado para evitar duplicados
    if registro.estado != 'pendiente':
        messages.warning(request, f"El registre de compra per a '{registro.socio}' ja ha estat processat.")
        return redirect('stock:gestion_stock') # Redirigir a la página principal de gestión

    try:
        # Obtener la cuenta del socio (crearla si no existe podría ser una opción, pero más seguro fallar si no existe)
        cuenta_socio = CuentaSocio.objects.get(socio=registro.socio)

        # Calcular el costo total y redondear a 2 decimales
        costo_total = round(registro.cantidad * registro.producto.precio, 2)

        # Crear el movimiento de cuenta (egreso = sortida de diners del compte)
        movimiento = MovimientoCuenta.objects.create(
            cuenta=cuenta_socio,
            tipo_movimiento='egreso', # Tipo vàlid segons el model
            monto=costo_total, # Monto positiu (egreso ja indica sortida)
            descripcion=f"Compra registrada #{registro.id}: {registro.cantidad} x {registro.producto.nombre}",
            estado='validado' # Asumimos que estos cargos son válidos directamente
        )

        # Actualizar el registro de compra
        registro.estado = 'validado'
        registro.costo_total_calculado = costo_total
        registro.movimiento_cuenta = movimiento # Enlazar con el movimiento creado
        registro.save()

        messages.success(request, f"Registre #{registro.id} validat. S'ha carregat {costo_total:.2f} € al compte de {registro.socio}.")

    except CuentaSocio.DoesNotExist:
        messages.error(request, f"Error: No s'ha trobat el compte per al soci {registro.socio}. No s'ha pogut validar el registre #{registro.id}.")
        # Opcionalmente, marcar el registro como 'error'
        # registro.estado = 'error'
        # registro.save()
    except Exception as e:
        messages.error(request, f"Error inesperat en validar el registre #{registro.id}: {e}")
        # Opcionalmente, marcar el registro como 'error'
        # registro.estado = 'error'
        # registro.save()

    # Redirigir siempre de vuelta a la página de gestión, anclando a la pestaña de registros
    redirect_url = reverse('stock:gestion_stock') + '#registros-compras-tab-pane'
    return redirect(redirect_url)
