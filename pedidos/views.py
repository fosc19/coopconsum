from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.db.models import Sum, Q, F, ExpressionWrapper, FloatField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Importar Paginator
from django import forms
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect # Importar más
from django.urls import reverse # Para reverse
from django.contrib import messages # Para mensajes flash

from pedidos.models import (
    PedidoColectivo, SeleccionSocio, DetalleSeleccion, ComandaRecurrente, AnotacionStockConsumido # Importar nuevo modelo
)
from productos.models import Producto

# Formulario para cada detalle de selección
class DetalleSeleccionForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        widget=forms.HiddenInput()
    )
    # Cambiado a DecimalField para permitir decimales en kg/g
    cantidad = forms.DecimalField(
        min_value=0,
        initial=0,
        max_digits=10,
        decimal_places=3, # Permitir hasta gramos (0.001 kg)
        widget=forms.NumberInput(attrs={'step': 'any'}) # Permitir cualquier decimal por defecto
    )

    # Ajustar el step dinámicamente según la unidad del producto
    def __init__(self, *args, **kwargs):
        # Obtener el producto si se pasa como initial data o instance
        producto = kwargs.get('initial', {}).get('producto')
        if isinstance(producto, int): # Si es ID, obtener el objeto
             try:
                 producto = Producto.objects.get(pk=producto)
             except Producto.DoesNotExist:
                 producto = None
        elif isinstance(kwargs.get('instance'), DetalleSeleccion): # Si es una instancia
             producto = kwargs.get('instance').producto

        super().__init__(*args, **kwargs)

        if producto:
            # Si es por unidad, forzar step=1 y 0 decimales
            if producto.unidad_venta == 'ud':
                self.fields['cantidad'].decimal_places = 0
                self.fields['cantidad'].widget.attrs['step'] = '1'
            # Si es kg o g, permitir decimales (ya está por defecto con 'any')
            # Podríamos ajustar decimal_places si quisiéramos limitar a 2 para kg, 0 para g, etc.
            # else: # kg o g
            #     self.fields['cantidad'].decimal_places = 3 # ej. 0.500 kg
            #     self.fields['cantidad'].widget.attrs['step'] = '0.001' # ej. para gramos

@login_required
def seleccionar_pedido(request, pedido_id):
    """
    Vista para que el socio seleccione productos en un pedido ya existente.
    Si el pedido es esporádico y no tiene socio asignado, se asigna el usuario actual.
    """
    # Solo permitir seleccionar pedidos que están estrictamente 'abiertos'
    pedido = get_object_or_404(PedidoColectivo, id=pedido_id, estado='abierto')

    # --- Comprobación de fecha_inicio_pedidos ---
    from django.utils import timezone # Asegurar que timezone está importado
    ahora = timezone.now()
    if pedido.fecha_inicio_pedidos and ahora < pedido.fecha_inicio_pedidos:
        messages.error(request, f"Los pedidos para esta comanda se abrirán el {pedido.fecha_inicio_pedidos.strftime('%d/%m/%Y a las %H:%M')}.")
        # Redirigir a una página donde el socio pueda ver otros pedidos o su panel
        # Por ejemplo, a la lista de pedidos abiertos o al panel de socios
        return redirect('pedidos_abiertos') # O 'socios_home' o la que consideres mejor
    # --- Fin comprobación de fecha_inicio_pedidos ---

    # --- Comprobación de perfil de socio ---
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Tu usuario no tiene un perfil de socio asociado. No puedes seleccionar productos.")
        # Redirigir a una página adecuada, por ejemplo, el dashboard principal
        return redirect('dashboard_principal') # O a la URL que consideres apropiada
    # --- Fin comprobación ---

    # Para pedidos esporádicos, si no hay socio, lo asignamos
    if pedido.tipo == 'esporadico' and not pedido.socio:
        pedido.socio = request.user.socio # Ahora sabemos que request.user.socio existe
        pedido.save()

    # Filtrar productos según categoría/proveedor
    if pedido.categoria and pedido.proveedor:
        productos = Producto.objects.filter(categoria=pedido.categoria, proveedor=pedido.proveedor)
    elif pedido.categoria:
        productos = Producto.objects.filter(categoria=pedido.categoria)
    elif pedido.proveedor:
        productos = Producto.objects.filter(proveedor=pedido.proveedor)
    else:
        productos = Producto.objects.all()

    DetalleFormSet = formset_factory(DetalleSeleccionForm, extra=0)
    initial_data = [{'producto': p.id, 'cantidad': 0} for p in productos]

    if request.method == 'POST':
        formset = DetalleFormSet(request.POST)
        for form in formset:
            form.fields['producto'].queryset = productos
        if formset.is_valid():
            # SeleccionSocio
            # Ya hemos comprobado que request.user.socio existe
            seleccion, created = SeleccionSocio.objects.get_or_create(
                pedido=pedido,
                socio=request.user.socio
            )
            # Crear DetalleSeleccion
            for form in formset:
                producto = form.cleaned_data.get('producto')
                cantidad = form.cleaned_data.get('cantidad')

                if not producto:
                    continue

                detalle, created = DetalleSeleccion.objects.get_or_create(
                    seleccion=seleccion,
                    producto=producto,
                    defaults={'cantidad': cantidad}
                )

                if not created:
                    if cantidad > 0:
                        # Actualizar cantidad existente
                        detalle.cantidad = cantidad
                        detalle.save()
                    else:
                        # Si cantidad es 0, eliminar el detalle
                        detalle.delete()
                else:
                    if cantidad <= 0:
                        # Si se creó con cantidad 0, eliminarlo inmediatamente
                                detalle.delete()
            return redirect('socios_home') # Cambiado a la URL del panel de socios
        # Si el formset NO es válido (cuando request.method == 'POST'),
        # formset ya está definido con los errores desde la línea 90.
        # El flujo continuará y se usará ese formset en el render.

    else:  # Esto corresponde a if request.method != 'POST' (es decir, es GET)
        # Buscar si ya existe una selección previa del socio para este pedido
        try:
            # Ya hemos comprobado que request.user.socio existe
            seleccion_existente = SeleccionSocio.objects.get(
                pedido=pedido,
                socio=request.user.socio
            )
            detalles_existentes = {
                d.producto_id: d.cantidad
                for d in DetalleSeleccion.objects.filter(seleccion=seleccion_existente)
            }
        except SeleccionSocio.DoesNotExist:
            detalles_existentes = {}

        # Inicializar el formulario con las cantidades existentes
        # Aseguramos que initial_data se define antes de usarla
        current_initial_data = [] # Renombrado para evitar confusión con la variable global initial_data
        for p in productos:
            cantidad = detalles_existentes.get(p.id, 0)
            current_initial_data.append({'producto': p.id, 'cantidad': cantidad})

        formset = DetalleFormSet(initial=current_initial_data)
        for form in formset:
            form.fields['producto'].queryset = productos

    # Ahora 'formset' siempre estará definido antes de esta línea
    enumerated_pairs = list(enumerate(zip(productos, formset.forms), start=1))
    return render(request, 'pedidos/seleccionar_pedido.html', {
        'pedido': pedido,
        'formset': formset,
        'productos': productos,
        'enumerated_pairs': enumerated_pairs,
    })

@login_required
def pedidos_abiertos(request):
    # Mostrar solo pedidos estrictamente 'abiertos' en esta lista
    # y que ya hayan alcanzado su fecha_inicio_pedidos y no hayan pasado su fecha_cierre
    from django.utils import timezone # Asegurar importación
    from django.db.models import Q # Para consultas OR
    ahora = timezone.now()
    pedidos = PedidoColectivo.objects.filter(
        Q(estado='abierto') &
        (Q(fecha_inicio_pedidos__isnull=True) | Q(fecha_inicio_pedidos__lte=ahora)) &
        Q(fecha_cierre__gte=ahora)
    ).order_by('fecha_cierre') # Opcional: ordenar por fecha de cierre
    return render(request, 'pedidos/pedidos_abiertos.html', {'pedidos': pedidos})

# --- Re-added panel_principal view ---
@login_required
def panel_principal(request):
    """
    Vista principal del panel (puede estar en otra app, pero si la tienes aquí, se respeta).
    """
    # --- Comprobación de perfil de socio ---
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Tu usuario no tiene un perfil de socio asociado. No se puede mostrar el panel.")
        # Redirigir a una página adecuada, por ejemplo, la página de inicio de la web pública
        return redirect('web_home') # O a la URL que consideres apropiada
    # --- Fin comprobación ---

    socio = request.user.socio
    saldo = 0  # Ejemplo
    ultimos_movimientos = []
    ultimas_comandas = []
    pedidos_abiertos_list = PedidoColectivo.objects.filter(estado__in=['abierto', 'pendiente'])[:5]
    events_json = "[]"  # Ejemplo

    context = {
        'socio': socio,
        'saldo': saldo,
        'ultimos_movimientos': ultimos_movimientos,
        'ultimas_comandas': ultimas_comandas,
        'pedidos_abiertos': pedidos_abiertos_list,
        'events_json': events_json,
    }
    return render(request, 'panel_principal.html', context)
# --- End re-added view ---

@login_required
def seleccionar_comanda(request):
    """
    Muestra dos secciones:
      - Comandas recurrentes asignadas al socio (comandas_recurrentes).
      - Pedidos esporádicos asignados al socio (pedidos_esporadicos).
    """
    # --- Comprobación de perfil de socio ---
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Tu usuario no tiene un perfil de socio asociado. No puedes seleccionar comandas.")
        return redirect('dashboard_principal') # O a la URL que consideres apropiada
    # --- Fin comprobación ---
    socio = request.user.socio

    # Filtrar comandas recurrentes activas asignadas al socio
    comandas_recurrentes = ComandaRecurrente.objects.filter(
        socio_asignado=socio,
        estado='activa'
    )

    # Añadir información del último pedido colectivo a cada comanda recurrente
    for comanda in comandas_recurrentes:
        # Buscar el último pedido colectivo asociado a esta comanda
        ultimo_pedido = PedidoColectivo.objects.filter(comanda=comanda).order_by('-fecha_apertura').first()
        if ultimo_pedido:
            comanda.ultimo_pedido_estado = ultimo_pedido.get_estado_display() # Usar get_estado_display() para el nombre legible
            comanda.ultimo_pedido_id = ultimo_pedido.id # Opcional: guardar ID si se necesita enlace
        else:
            comanda.ultimo_pedido_estado = "Sin pedidos generados"
            comanda.ultimo_pedido_id = None

    # Ya no necesitamos filtrar pedidos esporádicos por separado
    # pedidos_esporadicos = PedidoColectivo.objects.filter(
    #     tipo='esporadico',
    #     socio=socio,
    #     estado__in=['abierto', 'pendiente']
    # )

    # Propuestas pendientes para el socio gestor
    from pedidos.models import PropuestaCorreccionComanda
    propuestas_pendientes = PropuestaCorreccionComanda.objects.filter(
        comanda__socio_asignado=socio,
        estado='pendiente'
    ).select_related('comanda', 'usuario')

    # Todos los socios y productos para mostrar nombres en la tabla de cambios
    from socios.models import Socio
    from productos.models import Producto
    socios = Socio.objects.all()
    productos = Producto.objects.all()

    # Diccionario de cantidades actuales por (comanda, socio, producto)
    from pedidos.models import DetalleSeleccion, SeleccionSocio
    cantidades_actuales = {}
    for propuesta in propuestas_pendientes:
        comanda = propuesta.comanda
        pedidos_abiertos = PedidoColectivo.objects.filter(comanda=comanda, estado__in=['abierto', 'pendiente'])
        for pedido in pedidos_abiertos:
            selecciones = SeleccionSocio.objects.filter(pedido=pedido)
            for seleccion in selecciones:
                detalles = DetalleSeleccion.objects.filter(seleccion=seleccion)
                for detalle in detalles:
                    key = (comanda.id, seleccion.socio_id, detalle.producto_id)
                    cantidades_actuales[key] = detalle.cantidad

    context = {
        'comandas_recurrentes': comandas_recurrentes,
        # 'pedidos_esporadicos': pedidos_esporadicos, # Eliminado del contexto
        'propuestas_pendientes': propuestas_pendientes,
        'socios': socios,
        'productos': productos,
        'cantidades_actuales': cantidades_actuales,
    }
    return render(request, 'pedidos/seleccionar_comanda.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from pedidos.models import (
    PedidoColectivo, SeleccionSocio, DetalleSeleccion, ComandaRecurrente
)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from pedidos.models import (
    PedidoColectivo, SeleccionSocio, DetalleSeleccion, ComandaRecurrente
)

@login_required
def gestionar_comanda(request, comanda_id):
    comanda = get_object_or_404(ComandaRecurrente, id=comanda_id)
    # Solo el gestor puede acceder
    if not comanda.socio_asignado or comanda.socio_asignado.user != request.user:
        return HttpResponseForbidden("No tienes permiso para gestionar esta comanda. Solo el socio gestor asignado puede acceder.")
    # Obtener los PedidoColectivo relevantes para esta comanda (los que aún no están inactivos/cerrados)
    pedidos_relevantes = PedidoColectivo.objects.filter(
        comanda=comanda,
        estado__in=['abierto', 'pendiente', 'listo_para_finalizar'] # Incluir el nuevo estado
    )
    pedidos_relevantes_ids = list(pedidos_relevantes.values_list('id', flat=True))
    total_pedidos = len(pedidos_relevantes_ids) # Contar todos los relevantes
    # Obtener el estado del primer pedido activo/pendiente (si existe)
    # Determinar el estado actual relevante (priorizando listo > pendiente > abierto)
    # Esto asume que no debería haber más de uno en estos estados a la vez para la misma comanda.
    pedido_actual_obj = pedidos_relevantes.filter(estado='listo_para_finalizar').first() or \
                        pedidos_relevantes.filter(estado='pendiente').first() or \
                        pedidos_relevantes.filter(estado='abierto').first()
    estado_pedido_actual = pedido_actual_obj.estado if pedido_actual_obj else None

    # ------------------------
    # A) Resumen Global (sin socios)
    # ------------------------
    resumen_global_queryset = (
        DetalleSeleccion.objects
        # Filtrar por los IDs de todos los pedidos relevantes para el resumen
        .filter(seleccion__pedido_id__in=pedidos_relevantes_ids)
        .annotate(
            subtotal=ExpressionWrapper(
                F('cantidad') * F('producto__precio'),
                output_field=FloatField()
            )
        )
        .values('producto__nombre')
        .annotate(
            total_cantidad=Sum('cantidad'),
            total_precio=Sum('subtotal')
        )
        .order_by('producto__nombre')
    )

    resumen_global_data = []
    resumen_global_total_cantidad = 0
    resumen_global_total_precio = 0
    for item in resumen_global_queryset:
        producto = item['producto__nombre']
        cant = item['total_cantidad']
        prec = item['total_precio'] or 0
        resumen_global_data.append({
            'producto': producto,
            'cantidad': cant,
            'precio': prec,
        })
        resumen_global_total_cantidad += cant
        resumen_global_total_precio += prec

    # ------------------------
    # B) Pivot por socio
    # ------------------------
    detalle_queryset = (
        DetalleSeleccion.objects
        # Filtrar por los IDs de todos los pedidos relevantes para el pivot
        .filter(seleccion__pedido_id__in=pedidos_relevantes_ids)
        .annotate(
            subtotal=ExpressionWrapper(
                F('cantidad') * F('producto__precio'),
                output_field=FloatField()
            )
        )
        .values(
            'seleccion__socio__id',
            'seleccion__socio__nombre',
            'producto__nombre'
        )
        .annotate(
            total_cantidad=Sum('cantidad'),
            total_precio=Sum('subtotal')
        )
        .order_by('seleccion__socio__nombre', 'producto__nombre')
    )

    pivot = {}
    productos_set = set()
    for entry in detalle_queryset:
        socio_id = entry['seleccion__socio__id']
        socio_nombre = entry['seleccion__socio__nombre']
        producto = entry['producto__nombre']
        cant = entry['total_cantidad']
        prec = entry['total_precio'] or 0

        productos_set.add(producto)
        if socio_id not in pivot:
            pivot[socio_id] = {
                'socio_nombre': socio_nombre,
                'productos': {}
            }
        pivot[socio_id]['productos'][producto] = {
            'cantidad': cant,
            'precio': prec,
        }

    productos_list_nombres = sorted(list(productos_set))
    # Obtener los objetos Producto correspondientes para pasar a la plantilla
    productos_obj_list = list(Producto.objects.filter(nombre__in=productos_list_nombres).order_by('nombre'))

    # Para totales por columna
    # Usar nombres de objetos para inicializar
    column_totals_cantidad = {p.nombre: 0 for p in productos_obj_list}
    column_totals_precio = {p.nombre: 0 for p in productos_obj_list}
    grand_total_cantidad = 0
    grand_total_precio = 0

    pivot_data = []
    for sid, data in sorted(pivot.items(), key=lambda item: item[1]['socio_nombre']):
        row_total_cantidad = 0
        row_total_precio = 0
        row_products = {}

        for producto_obj in productos_obj_list:
            producto_nombre = producto_obj.nombre
            info = data['productos'].get(producto_nombre, {'cantidad': 0, 'precio': 0})
            c = info['cantidad']
            p = info['precio']
            row_products[producto_nombre] = info
            row_total_cantidad += c
            row_total_precio += p
            column_totals_cantidad[producto_nombre] += c
            column_totals_precio[producto_nombre] += prec # Usar prec (precio)

        grand_total_cantidad += row_total_cantidad
        grand_total_precio += row_total_precio

        pivot_data.append({
            'socio_id': sid, # <-- Añadir el ID del socio aquí
            'socio_nombre': data['socio_nombre'],
            'productos': row_products,
            'row_total_cantidad': row_total_cantidad,
            'row_total_precio': row_total_precio,
        })

    # Cálculo de colspan (ejemplo):
    # Si tienes 2 columnas por producto y luego 2 columnas de totales + 1 columna para el socio,
    # => (len(productos_list) * 2) + 3
    # Ajusta si tu diseño es distinto.
    colspan_pivot = (len(productos_obj_list) * 2) + 3

    # Propuestas de corrección pendientes para esta comanda
    from pedidos.models import PropuestaCorreccionComanda
    propuestas_pendientes = PropuestaCorreccionComanda.objects.filter(
        comanda=comanda,
        estado='pendiente'
    ).select_related('comanda', 'usuario')

    # Todos los socios y productos para mostrar nombres en la tabla de cambios
    from socios.models import Socio
    socios = Socio.objects.all()
    productos = Producto.objects.all()

    # Diccionario de cantidades actuales por (comanda, socio, producto)
    cantidades_actuales = {}
    # Usar pedidos_relevantes para obtener las cantidades actuales
    for pedido in pedidos_relevantes:
        selecciones = SeleccionSocio.objects.filter(pedido=pedido)
        for seleccion in selecciones:
            detalles = DetalleSeleccion.objects.filter(seleccion=seleccion)
            for detalle in detalles:
                key = f"{comanda.id},{seleccion.socio_id},{detalle.producto_id}"
                cantidades_actuales[key] = detalle.cantidad

    # Historial de todas las propuestas para esta comanda
    historial_propuestas_comanda = PropuestaCorreccionComanda.objects.filter(
        comanda=comanda
    ).select_related('usuario', 'usuario_validador').order_by('-fecha_propuesta')

    # Historial de todos los PedidoColectivo para esta comanda
    historial_pedidos_colectivos_list = PedidoColectivo.objects.filter(
        comanda=comanda
    ).order_by('-fecha_apertura') # O por fecha_cierre, según preferencia

    # Paginación para el historial de propuestas
    propuestas_paginator = Paginator(historial_propuestas_comanda, 5) # 5 por página
    propuestas_page_number = request.GET.get('propuestas_page')
    try:
        historial_propuestas_comanda_paginado = propuestas_paginator.page(propuestas_page_number)
    except PageNotAnInteger:
        historial_propuestas_comanda_paginado = propuestas_paginator.page(1)
    except EmptyPage:
        historial_propuestas_comanda_paginado = propuestas_paginator.page(propuestas_paginator.num_pages)

    # Paginación para el historial de pedidos colectivos
    pedidos_paginator = Paginator(historial_pedidos_colectivos_list, 5) # 5 por página
    pedidos_page_number = request.GET.get('pedidos_page')
    try:
        historial_pedidos_colectivos_paginado = pedidos_paginator.page(pedidos_page_number)
    except PageNotAnInteger:
        historial_pedidos_colectivos_paginado = pedidos_paginator.page(1)
    except EmptyPage:
        historial_pedidos_colectivos_paginado = pedidos_paginator.page(pedidos_paginator.num_pages)

    # --- Lógica de mensajes flash para 'propuesta_validada' eliminada ---
    # La activación de botones ahora dependerá directamente de 'estado_pedido_actual'


    context = {
        'comanda': comanda,
        'pedidos': pedidos_relevantes, # Pasar la lista completa relevante
        'total_pedidos': total_pedidos,

        # Resumen Global
        'resumen_global_data': resumen_global_data,
        'resumen_global_total_cantidad': resumen_global_total_cantidad,
        'resumen_global_total_precio': resumen_global_total_precio,

        # Pivot por socio
        'productos_list': productos_list_nombres,
        'productos_obj_list': productos_obj_list,
        'pivot_data': pivot_data,
        'column_totals_cantidad': column_totals_cantidad,
        'column_totals_precio': column_totals_precio,
        'grand_total_cantidad': grand_total_cantidad,
        'grand_total_precio': grand_total_precio,

        'colspan_pivot': (len(productos_obj_list) * 2) + 3,

        # Propuestas de corrección
        'propuestas_pendientes': propuestas_pendientes,
        'socios': socios,
        'productos': productos,
        'cantidades_actuales': cantidades_actuales,
        'user': request.user,
        # Variable 'puede_finalizar_tras_validacion' eliminada del contexto
        # Estado del pedido actual para controlar los botones
        'estado_pedido_actual': estado_pedido_actual, # Ya se pasaba, ahora es la única referencia
        'historial_propuestas_comanda': historial_propuestas_comanda_paginado, # Usar la versión paginada
        'historial_pedidos_colectivos': historial_pedidos_colectivos_paginado, # Usar la versión paginada
    }
    return render(request, 'pedidos/gestionar_comanda.html', context)

# --- Vista para finalizar comanda y descontar monederos ---
from django.views.decorators.http import require_POST
from django.db import transaction
from socios.models import Socio, CuentaSocio, MovimientoCuenta

@login_required
@require_POST
@transaction.atomic
def finalizar_comanda(request, comanda_id):
    comanda = get_object_or_404(ComandaRecurrente, id=comanda_id)
    # Solo el gestor puede finalizar y solo si está activa
    if not comanda.socio_asignado or comanda.socio_asignado.user != request.user or comanda.estado != 'activa':
        messages.error(request, "No tienes permisos para finalizar esta comanda o ya está finalizada.")
        return redirect('gestionar_comanda', comanda_id=comanda.id)

    # --- INICIO: Procesar cambios de cantidad enviados ---
    pedidos_actuales = PedidoColectivo.objects.filter(comanda=comanda, estado__in=['abierto', 'pendiente'])
    pedidos_actuales_ids = list(pedidos_actuales.values_list('id', flat=True))
    cambios_realizados = 0

    for key, value in request.POST.items():
        if key.startswith('cantidad_'):
            try:
                parts = key.split('_')
                 # Verificar que tenemos exactamente 3 partes y que socio/producto ID no están vacíos
                if len(parts) == 3 and parts[1] and parts[2]:
                    socio_id_str = parts[1]
                    producto_id_str = parts[2]
                    socio_id = int(socio_id_str)
                    producto_id = int(producto_id_str)
                else:
                    # Si el formato no es cantidad_X_Y, ignorar este campo silenciosamente o loggear
                    print(f"WARN: Ignorando campo con formato inesperado al finalizar: {key}")
                    continue # Saltar al siguiente item del POST

                cantidad_str = value.strip()
                if cantidad_str == '': # Si está vacío, tratar como 0
                    cantidad = 0.0
                else:
                    cantidad = float(cantidad_str.replace(',', '.'))

                # Buscar el pedido colectivo abierto de este socio en esta comanda
                # Importante: Usar filter() y first() para manejar el caso de que no exista
                pedido_socio = pedidos_actuales.filter(socio_id=socio_id).first()
                if not pedido_socio:
                    # Si no hay pedido activo para este socio en esta comanda, no podemos guardar el detalle.
                    # Podría ser un socio que no participa o un error en el formulario.
                    print(f"WARN: No se encontró pedido activo para socio {socio_id} en comanda {comanda_id} al intentar guardar cantidad.")
                    continue # Saltar al siguiente campo del formulario

                # Obtener o crear la selección del socio para este pedido específico
                seleccion, created_seleccion = SeleccionSocio.objects.get_or_create(
                    pedido=pedido_socio,
                    socio_id=socio_id
                )
                # Si la selección se acaba de crear, no debería haber detalles previos.

                # Obtener o crear/actualizar/eliminar el detalle
                detalle, created_detalle = DetalleSeleccion.objects.get_or_create(
                    seleccion=seleccion,
                    producto_id=producto_id,
                    defaults={'cantidad': cantidad} # Solo se usa si se crea
                )

                if not created_detalle: # Si el detalle ya existía...
                    if cantidad > 0:
                        if detalle.cantidad != cantidad: # Solo actualizar si hay cambio real
                            detalle.cantidad = cantidad
                            detalle.save()
                            cambios_realizados += 1
                    else: # Si la cantidad nueva es 0 o menos, eliminar el detalle existente
                        detalle.delete()
                        cambios_realizados += 1 # Contamos la eliminación como un cambio
                # Si el detalle se acaba de crear (created_detalle es True)...
                elif cantidad <= 0: # ...y se creó con 0 o menos, eliminarlo inmediatamente
                    detalle.delete()
                    # No contamos como cambio si se crea y elimina al instante
                else: # ...y se creó con cantidad > 0, sí lo contamos como cambio
                    cambios_realizados += 1

            except (ValueError, IndexError, SeleccionSocio.DoesNotExist, Producto.DoesNotExist) as e:
                # Capturar errores específicos para mejor depuración
                messages.error(request, f"Error procesando el campo {key}={value}: {e}. No se aplicaron todos los cambios.")
                print(f"Error procesando campo {key}={value}: {e}")
                # Decidimos continuar para intentar guardar otros cambios válidos
                continue

    if cambios_realizados > 0:
        messages.info(request, f"Se aplicaron {cambios_realizados} cambios en las cantidades.")
    # --- FIN: Procesar cambios de cantidad enviados ---

    # --- Lógica de finalización ---
    # Buscar el pedido asociado a la comanda que esté listo para finalizar
    # Asumimos que solo debería haber uno en este estado por comanda a la vez
    pedido_a_finalizar = PedidoColectivo.objects.filter(
        comanda=comanda,
        estado='listo_para_finalizar' # Cambiado el filtro de estado
    ).first()

    # Si no se encuentra un pedido en estado 'listo_para_finalizar'
    if not pedido_a_finalizar:
        messages.error(request, "No se encontró un pedido 'listo para finalizar' asociado a esta comanda.")
        return redirect('gestionar_comanda', comanda_id=comanda.id) # Volver a la gestión

    # Calcular el total a descontar por socio (pivot) BASADO EN DATOS ACTUALIZADOS
    # Usamos el ID del pedido encontrado
    detalle_queryset = (
        DetalleSeleccion.objects
        .filter(seleccion__pedido_id=pedido_a_finalizar.id)
        .select_related('producto', 'seleccion__socio') # Optimizar consulta
        .annotate(
            subtotal=ExpressionWrapper(
                F('cantidad') * F('producto__precio'),
                output_field=FloatField()
            )
        )
        .values(
            'seleccion__socio__id',
            'seleccion__socio__nombre' # Incluir nombre para mensaje
        )
        .annotate(
            total_precio_socio=Sum('subtotal') # Renombrar para claridad
        )
        .order_by('seleccion__socio__nombre') # Ordenar para mensaje consistente
    )

    socios_afectados_msg = []
    total_descontado_general = 0
    for entry in detalle_queryset:
        socio_id = entry['seleccion__socio__id']
        socio_nombre = entry['seleccion__socio__nombre'] # Usar el nombre obtenido
        total_a_descontar = entry['total_precio_socio'] or 0

        if total_a_descontar <= 0: # No descontar si el total es 0 o negativo
            continue

        try:
            # Ya tenemos el socio_id, obtener la cuenta
            cuenta, _ = CuentaSocio.objects.get_or_create(socio_id=socio_id)
        except CuentaSocio.DoesNotExist: # Aunque get_or_create debería manejarlo
             print(f"WARN: No se pudo obtener/crear cuenta para socio ID {socio_id}")
             continue

        # Crear movimiento negativo y validar
        MovimientoCuenta.objects.create(
            cuenta=cuenta,
            tipo_movimiento="egreso",
            monto=-total_a_descontar, # Monto negativo para egreso
            descripcion=f"Descuento por compra en comanda '{comanda.nombre}' (ID {comanda.id})",
            estado="validado" # Asumimos que siempre se valida al finalizar
        )

        # Actualizar saldo (restar el valor positivo del total)
        # Usar F() para evitar race conditions
        cuenta.saldo_actual = F('saldo_actual') - total_a_descontar
        cuenta.save(update_fields=['saldo_actual']) # Actualizar solo el saldo

        socios_afectados_msg.append(f"{socio_nombre} ({total_a_descontar:.2f}€)")
        total_descontado_general += total_a_descontar

    # Cambiar estado del pedido a 'inactivo' DESPUÉS de descontar
    pedido_a_finalizar.estado = 'inactivo'
    pedido_a_finalizar.save(update_fields=['estado'])
    num_pedidos_finalizados = 1 # Solo finalizamos uno

    # Mensaje final más detallado
    if socios_afectados_msg:
        mensaje_final = (f"Comanda finalizada (Pedido ID {pedido_a_finalizar.id} marcado como inactivo). "
                         f"Se descontó un total de {total_descontado_general:.2f}€ de los monederos de: "
                         f"{', '.join(socios_afectados_msg)}.")
    else:
        mensaje_final = (f"Comanda finalizada ({num_pedidos_finalizados} pedidos asociados marcados como inactivos). "
                         f"No se realizaron descuentos (total 0€).")

    messages.success(request, mensaje_final)
    # Redirigir a la selección de comandas o donde sea apropiado después de finalizar
    return redirect('seleccionar_comanda')

# --- Vista para validar propuesta de corrección ---
@login_required
def validar_propuesta_correccion(request, propuesta_id):
    from django.utils import timezone
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from pedidos.models import PropuestaCorreccionComanda, PedidoColectivo, SeleccionSocio, DetalleSeleccion

    propuesta = get_object_or_404(PropuestaCorreccionComanda, id=propuesta_id)
    comanda = propuesta.comanda

    # Solo el gestor de la comanda puede validar
    if not comanda.socio_asignado or comanda.socio_asignado.user != request.user:
        messages.error(request, "No tienes permisos para validar esta propuesta.")
        return redirect('seleccionar_comanda')

    cambios = propuesta.get_cambios_list()
    pedidos_abiertos = PedidoColectivo.objects.filter(comanda=comanda, estado__in=['abierto', 'pendiente'])

    for cambio in cambios:
        socio_id = cambio['socio_id']
        producto_id = cambio['producto_id']
        cantidad = cambio['cantidad']
        # Buscar la selección del socio DENTRO de los pedidos abiertos/pendientes de esta comanda
        # Es posible que un socio tenga selección en más de un pedido activo si la lógica lo permite,
        # aunque lo normal será uno. Aplicamos a la primera encontrada.
        seleccion = SeleccionSocio.objects.filter(
            pedido__in=pedidos_abiertos, # Buscar en los pedidos correctos
            socio_id=socio_id
        ).first()

        # Si no hay selección para este socio en ningún pedido abierto/pendiente, no podemos aplicar el cambio.
        if not seleccion:
             # Podríamos loggear un warning aquí si se espera que siempre exista
             print(f"WARN: No se encontró SelecciónSocio para socio {socio_id} en pedidos abiertos/pendientes de comanda {comanda.id} al validar propuesta.")
             continue

        # Ahora que tenemos la selección correcta, operamos sobre sus detalles
        detalle, created = DetalleSeleccion.objects.get_or_create(
            seleccion=seleccion, # Usar la selección encontrada
            producto_id=producto_id,
            defaults={'cantidad': cantidad}
        )
        if not created: # Si ya existía el detalle...
            if cantidad > 0:
                if detalle.cantidad != cantidad: # Solo guardar si hay cambio real
                    detalle.cantidad = cantidad
                    detalle.save()
            else: # Si la cantidad propuesta es 0 o menos, eliminar
                detalle.delete()
        elif cantidad <= 0: # Si se creó con 0 o menos, eliminarlo inmediatamente
            detalle.delete()

        # Aquí iría la lógica para descontar del monedero del socio (placeholder)
        # Por ejemplo: socio.monedero -= cantidad * producto.precio

    propuesta.estado = 'validada'
    propuesta.fecha_validacion = timezone.now()
    propuesta.usuario_validador = request.user
    propuesta.save()

    # Después de validar la propuesta, buscar el pedido pendiente asociado y marcarlo como listo para finalizar
    pedido_a_actualizar = PedidoColectivo.objects.filter(
        comanda=comanda,
        estado='pendiente' # Solo actuar si está pendiente
    ).first()

    if pedido_a_actualizar:
        pedido_a_actualizar.estado = 'listo_para_finalizar'
        pedido_a_actualizar.save(update_fields=['estado'])
        messages.info(request, f"Propuesta validada. El pedido asociado (ID: {pedido_a_actualizar.id}) está ahora listo para finalizar.")
    else:
        # Si no se encontró un pedido pendiente, puede que ya estuviera listo o inactivo.
        # Solo mostramos el mensaje de éxito de la validación de la propuesta.
        messages.warning(request, "Propuesta validada, pero no se encontró un pedido asociado en estado 'pendiente' para marcar como listo.")

    messages.success(request, "Propuesta validada y aplicada correctamente. Los cambios han sido registrados.")
    # Eliminamos el mensaje flash especial
    # messages.success(request, "Señal interna: propuesta validada", extra_tags='propuesta_validada')
    # Construir la URL base usando reverse
    redirect_url = reverse('gestionar_comanda', kwargs={'comanda_id': comanda.id})
    # Añadir el fragmento para la pestaña deseada
    redirect_url_with_fragment = f"{redirect_url}#tab-pedidos"
    return HttpResponseRedirect(redirect_url_with_fragment) # Usar HttpResponseRedirect para URL completa
# --- Fin vista validar propuesta ---
    # Esta línea parece un error residual, la vista validar_propuesta_correccion no debería llegar aquí.
    # return render(request, 'pedidos/gestionar_comanda.html', context)


@login_required
def gestionar_pedidos_esporadicos(request):
    """
    Gestiona pedidos esporádicos asignados al socio.
    Genera un resumen pivot similar al de las comandas recurrentes.
    """
    # --- Comprobación de perfil de socio ---
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Tu usuario no tiene un perfil de socio asociado. No puedes gestionar pedidos.")
        return redirect('dashboard_principal') # O a la URL que consideres apropiada
    # --- Fin comprobación ---
    socio = request.user.socio
    # Pedidos esporádicos del socio
    # Pedidos esporádicos *abiertos* del socio
    pedidos_esporadicos_abiertos = PedidoColectivo.objects.filter(tipo='esporadico', socio=socio, estado__in=['abierto', 'pendiente'])
    pedidos_esporadicos_abiertos_ids = list(pedidos_esporadicos_abiertos.values_list('id', flat=True))
    total_pedidos = len(pedidos_esporadicos_abiertos_ids)

    # Agrupamos DetalleSeleccion para estos pedidos
    detalle_queryset = (
        DetalleSeleccion.objects
        # Filtrar por los IDs de los pedidos esporádicos abiertos del socio
        .filter(seleccion__pedido_id__in=pedidos_esporadicos_abiertos_ids)
        .values('seleccion__socio__id', 'seleccion__socio__nombre', 'producto__nombre')
        .annotate(
             total_cantidad=Sum('cantidad'),
             # Añadir cálculo de subtotal para el resumen global y pivot
             subtotal=ExpressionWrapper(
                 F('cantidad') * F('producto__precio'),
                 output_field=FloatField()
             )
        )
        .order_by('seleccion__socio__nombre', 'producto__nombre')
    )

    # --- Añadir cálculo de Resumen Global (similar a gestionar_comanda) ---
    resumen_global_queryset = (
        DetalleSeleccion.objects
        .filter(seleccion__pedido_id__in=pedidos_esporadicos_abiertos_ids)
        .values('producto__nombre')
        .annotate(
            total_cantidad=Sum('cantidad'),
            total_precio=Sum(ExpressionWrapper(F('cantidad') * F('producto__precio'), output_field=FloatField()))
        )
        .order_by('producto__nombre')
    )

    resumen_global_data = []
    resumen_global_total_cantidad = 0
    resumen_global_total_precio = 0
    for item in resumen_global_queryset:
        resumen_global_data.append({
            'producto': item['producto__nombre'],
            'cantidad': item['total_cantidad'],
            'precio': item['total_precio'] or 0,
        })
        resumen_global_total_cantidad += item['total_cantidad']
        resumen_global_total_precio += item['total_precio'] or 0
    # --- Fin cálculo Resumen Global ---

    pivot = {}
    productos_set = set()
    for entry in detalle_queryset:
        sid = entry['seleccion__socio__id']
        snombre = entry['seleccion__socio__nombre']
        prod = entry['producto__nombre']
        cant = entry['total_cantidad']
        prec = entry['subtotal'] or 0
        productos_set.add(str(prod)) # Ensure product name is stored as string in the set

        if sid not in pivot:
            pivot[sid] = {'socio_nombre': snombre, 'productos': {}}
        pivot[sid]['productos'][prod] = {'cantidad': cant, 'precio': prec}

    productos_list_nombres = sorted(list(productos_set))
    # Obtener los objetos Producto correspondientes
    productos_obj_list = list(Producto.objects.filter(nombre__in=productos_list_nombres).order_by('nombre'))
    pivot_data = []
    # Adaptar cálculo de totales para incluir precio
    # Ensure keys are strings during initialization
    column_totals_cantidad = {p.nombre: 0 for p in productos_obj_list}
    column_totals_precio = {p.nombre: 0 for p in productos_obj_list}
    grand_total_cantidad = 0
    grand_total_precio = 0
    for sid, data in sorted(pivot.items(), key=lambda item: item[1]['socio_nombre']):
        row_total_cantidad = 0
        row_total_precio = 0
        row_products = {}
        for producto_obj in productos_obj_list:
            p = producto_obj.nombre
            info = data['productos'].get(p, {'cantidad': 0, 'precio': 0})
            c = info['cantidad']
            p_val = info['precio'] # Renombrado para evitar conflicto
            row_products[p] = info
            row_total_cantidad += c
            row_total_precio += p_val
            # Ensure p is treated as a string key (p is already string here)
            # --- DEBUG PRINT ---
            # print(f"DEBUG: p='{p}', c={c}, prec={prec}, keys={list(column_totals_cantidad.keys())}")
            # --- END DEBUG ---
            if p in column_totals_cantidad: # Check if key exists before adding
                column_totals_cantidad[p] += c
                column_totals_precio[p] += p_val # Corregido: usar p_val
            else:
                # Optional: Log a warning if a product appears unexpectedly
                print(f"WARN: Product '{p}' found in pivot but not in initial product list.")
        grand_total_cantidad += row_total_cantidad
        grand_total_precio += row_total_precio
        pivot_data.append({
            'socio_nombre': data['socio_nombre'],
            'productos': row_products,
            'row_total_cantidad': row_total_cantidad,
            'row_total_precio': row_total_precio,
        })

    context = {
        'pedidos': pedidos_esporadicos_abiertos,
        'total_pedidos': total_pedidos,
        'productos_list': productos_list_nombres,
        'productos_obj_list': productos_obj_list,

        # Añadir datos de Resumen Global
        'resumen_global_data': resumen_global_data,
        'resumen_global_total_cantidad': resumen_global_total_cantidad,
        'resumen_global_total_precio': resumen_global_total_precio,

        # Datos de Pivot (nombres adaptados)
        'pivot_data': pivot_data,
        'column_totals_cantidad': column_totals_cantidad,
        'column_totals_precio': column_totals_precio,
        'grand_total_cantidad': grand_total_cantidad,
        'grand_total_precio': grand_total_precio,
        'colspan_pivot': (len(productos_obj_list) * 2) + 3
    }
    return render(request, 'pedidos/gestionar_pedidos_esporadicos.html', context)

# --- Nueva vista Master Control ---
from socios.models import Socio # Importar Socio

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Importar Paginator

@login_required
# @permission_required('pedidos.can_manage_reception', raise_exception=True) # TODO: Añadir permiso si es necesario
def master_control_view(request):
    """
    Vista para que los encargados gestionen la recepción de pedidos y stock.
    Muestra un listado de pedidos colectivos abiertos.
    """
    # Obtener todos los pedidos colectivos que están abiertos o pendientes
    pedidos_abiertos = PedidoColectivo.objects.filter(estado__in=['abierto', 'pendiente']).order_by('fecha_cierre')
    pedidos_abiertos_ids = list(pedidos_abiertos.values_list('id', flat=True))

    # Obtener IDs de productos únicos seleccionados en estos pedidos abiertos
    # (Compatible con SQLite y otras BD)
    producto_ids_unicos = DetalleSeleccion.objects.filter(
        seleccion__pedido_id__in=pedidos_abiertos_ids
    ).values_list('producto_id', flat=True).distinct()

    # Obtener los objetos Producto correspondientes a esos IDs
    productos_unicos = list(Producto.objects.filter(id__in=producto_ids_unicos))
    # Ordenar por nombre para consistencia
    productos_unicos.sort(key=lambda x: x.nombre) # Productos que aparecen en pedidos abiertos

    # Obtener todos los socios para el selector
    todos_los_socios = Socio.objects.all().order_by('nombre', 'apellido')

    # Obtener productos marcados como de stock
    productos_de_stock = Producto.objects.filter(es_stock=True).order_by('nombre')

    # Diccionario: {pedido_id: [productos de ese pedido]}
    productos_por_pedido = {}
    for pedido in pedidos_abiertos:
        productos_ids = DetalleSeleccion.objects.filter(
            seleccion__pedido=pedido
        ).values_list('producto_id', flat=True).distinct()
        productos_por_pedido[pedido.id] = list(Producto.objects.filter(id__in=productos_ids).order_by('nombre'))

    # Preparar resumen editable para cada pedido abierto (como en gestionar_comanda)
    resumen_por_pedido = {}
    for pedido in pedidos_abiertos:
        pedido_id = pedido.id
        # IDs de socios con selección en este pedido
        seleccion_socio_ids = SeleccionSocio.objects.filter(pedido=pedido).values_list('socio_id', flat=True)
        # Productos de este pedido
        productos_obj_list = productos_por_pedido.get(pedido_id, [])
        productos_list_nombres = [p.nombre for p in productos_obj_list]
        # Pivot por socio
        detalle_queryset = (
            DetalleSeleccion.objects
            .filter(seleccion__pedido=pedido)
            .annotate(
                subtotal=ExpressionWrapper(
                    F('cantidad') * F('producto__precio'),
                    output_field=FloatField()
                )
            )
            .values(
                'seleccion__socio__id',
                'seleccion__socio__nombre',
                'producto__nombre'
            )
            .annotate(
                total_cantidad=Sum('cantidad'),
                total_precio=Sum('subtotal')
            )
            .order_by('seleccion__socio__nombre', 'producto__nombre')
        )
        pivot = {}
        for entry in detalle_queryset:
            socio_id = entry['seleccion__socio__id']
            socio_nombre = entry['seleccion__socio__nombre']
            producto = entry['producto__nombre']
            cant = entry['total_cantidad']
            prec = entry['total_precio'] or 0
            if socio_id not in pivot:
                pivot[socio_id] = {
                    'socio_id': socio_id,
                    'socio_nombre': socio_nombre,
                    'productos': {}
                }
            pivot[socio_id]['productos'][producto] = {
                'cantidad': cant,
                'precio': prec,
            }
        # Totales y filas
        column_totals_cantidad = {p.nombre: 0 for p in productos_obj_list}
        column_totals_precio = {p.nombre: 0 for p in productos_obj_list}
        grand_total_cantidad = 0
        grand_total_precio = 0
        pivot_data = []
        for sid, data in sorted(pivot.items(), key=lambda item: item[1]['socio_nombre']):
            row_total_cantidad = 0
            row_total_precio = 0
            row_products = {}
            for producto_obj in productos_obj_list:
                producto_nombre = producto_obj.nombre
                info = data['productos'].get(producto_nombre, {'cantidad': 0, 'precio': 0})
                c = info['cantidad']
                p_val = info['precio'] # Renombrado
                row_products[producto_nombre] = info
                row_total_cantidad += c
                row_total_precio += p_val
                column_totals_cantidad[producto_nombre] += c
                column_totals_precio[producto_nombre] += p_val # Corregido
            grand_total_cantidad += row_total_cantidad
            grand_total_precio += row_total_precio
            pivot_data.append({
                'socio_id': data['socio_id'],
                'socio_nombre': data['socio_nombre'],
                'productos': row_products,
                'row_total_cantidad': row_total_cantidad,
                'row_total_precio': row_total_precio,
            })
        colspan_pivot = (len(productos_obj_list) * 2) + 3
        resumen_por_pedido[pedido_id] = {
            'productos_obj_list': productos_obj_list,
            'pivot_data': pivot_data,
            'column_totals_cantidad': column_totals_cantidad,
            'column_totals_precio': column_totals_precio,
            'grand_total_cantidad': grand_total_cantidad,
            'grand_total_precio': grand_total_precio,
            'colspan_pivot': colspan_pivot,
        }

    # Historial de TODAS las propuestas enviadas
    from pedidos.models import PropuestaCorreccionComanda # Asegurar importación
    propuestas_list = PropuestaCorreccionComanda.objects.all( # Eliminado filtro por usuario
    ).select_related('comanda', 'usuario', 'usuario_validador').order_by('-fecha_propuesta') # Añadido 'usuario' a select_related

    # Paginación para el historial de propuestas
    paginator = Paginator(propuestas_list, 5) # Mostrar 5 propuestas por página
    page_number = request.GET.get('page')
    try:
        mis_propuestas_paginadas = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page no es un entero, entregar la primera página.
        mis_propuestas_paginadas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango (p.ej. 9999), entregar la última página de resultados.
        mis_propuestas_paginadas = paginator.page(paginator.num_pages)


    context = {
        'pedidos_abiertos': pedidos_abiertos,
        'todos_los_socios': todos_los_socios,
        'productos_de_stock': productos_de_stock,
        'resumen_por_pedido': resumen_por_pedido,
        'mis_propuestas_enviadas': mis_propuestas_paginadas, # Pasar el objeto Page al contexto
    }
    return render(request, 'pedidos/master_control.html', context)

# --- Vista para notificar recepción de productos por el master ---
import json
from pedidos.models import NotificacionRecepcionComanda

@login_required
def notificar_recepcion_comanda(request, pedido_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Método no permitido")

    pedido = get_object_or_404(PedidoColectivo, id=pedido_id)
    cantidades = {}
    for key, value in request.POST.items():
        if key.startswith('cantidad_'):
            try:
                producto_id = int(key.split('_')[1])
                cantidad_str = value.strip()
                if cantidad_str:
                    cantidad = float(cantidad_str.replace(',', '.'))
                    cantidades[str(producto_id)] = cantidad
            except Exception:
                continue
    mensaje = request.POST.get('mensaje', '').strip()

    NotificacionRecepcionComanda.objects.create(
        pedido=pedido,
        usuario=request.user,
        mensaje=mensaje,
        cantidades_recibidas=json.dumps(cantidades)
    )
    messages.success(request, "Notificación enviada a gestión comanda.")
    return redirect('master_control')
# --- Fin nueva vista ---

# --- Nueva vista API para resumen de pedido por socio ---
# @login_required # Podría requerir login, pero no permiso específico de socio
# @permission_required('pedidos.can_view_master_summary', raise_exception=True) # TODO: Añadir permiso si es necesario
def api_resumen_pedido_socios(request, pedido_id):
    """
    Devuelve en JSON el resumen por socio para un PedidoColectivo específico.
    Accesible para usuarios con permisos adecuados (ej. Master).
    """
    pedido = get_object_or_404(PedidoColectivo, id=pedido_id)
    pedidos_actuales_ids = [pedido.id] # Solo este pedido

    # Reutilizamos la lógica de cálculo de pivot de gestionar_comanda/esporadicos
    # pero sin filtrar por request.user.socio

    detalle_queryset = (
        DetalleSeleccion.objects
        .filter(seleccion__pedido_id__in=pedidos_actuales_ids)
        .annotate(
            subtotal=ExpressionWrapper(
                F('cantidad') * F('producto__precio'),
                output_field=FloatField()
            )
        )
        .values(
            'seleccion__socio__id',
            'seleccion__socio__nombre',
            'producto__nombre'
        )
        .annotate(
            total_cantidad=Sum('cantidad'),
            total_precio=Sum('subtotal')
        )
        .order_by('seleccion__socio__nombre', 'producto__nombre')
    )

    pivot = {}
    productos_set = set()
    for entry in detalle_queryset:
        socio_id = entry['seleccion__socio__id']
        socio_nombre = entry['seleccion__socio__nombre']
        prod = str(entry['producto__nombre']) # Asegurar string
        cant = entry['total_cantidad']
        prec = entry['total_precio'] or 0

        productos_set.add(prod)
        if socio_id not in pivot:
            pivot[socio_id] = {
                'socio_nombre': socio_nombre,
                'productos': {}
            }
        pivot[socio_id]['productos'][prod] = {
            'cantidad': cant,
            'precio': prec,
        }

    productos_list = sorted(list(productos_set))

    pivot_data_list = []
    for sid, data in sorted(pivot.items(), key=lambda item: item[1]['socio_nombre']):
        row_total_cantidad = 0
        row_total_precio = 0
        row_products = {}
        for p in productos_list:
            info = data['productos'].get(p, {'cantidad': 0, 'precio': 0})
            c = info['cantidad']
            p_val = info['precio'] # Renombrado para evitar conflicto
            row_products[p] = info
            row_total_cantidad += c
            row_total_precio += p_val
        pivot_data_list.append({
            'socio_nombre': data['socio_nombre'],
            'productos': row_products, # Diccionario {nombre_producto: {'cantidad': x, 'precio': y}}
            'row_total_cantidad': row_total_cantidad,
            'row_total_precio': row_total_precio,
        })

    # Datos a devolver en JSON
    response_data = {
        'pedido_id': pedido.id,
        'proveedor': pedido.proveedor.nombre if pedido.proveedor else None,
        'categoria': pedido.categoria.nombre if pedido.categoria else None,
        'productos_list': productos_list, # Lista de nombres de productos (columnas)
        'resumen_socios': pivot_data_list, # Lista de diccionarios por socio
    }

    return JsonResponse(response_data)
# --- Fin vista API ---

# --- Nueva vista para guardar anotaciones de stock ---
@login_required
# @permission_required('pedidos.add_anotacionstockconsumido', raise_exception=True) # TODO: Añadir permiso
def guardar_anotacion_stock(request):
    """Guarda las anotaciones de stock consumido enviadas desde el formulario."""
    if request.method != 'POST':
        return HttpResponseForbidden("Método no permitido")

    socio_id = request.POST.get('socio_stock')
    if not socio_id:
        messages.error(request, "Debes seleccionar un socio.")
        return HttpResponseRedirect(reverse('master_control'))

    try:
        socio = Socio.objects.get(id=socio_id)
    except Socio.DoesNotExist:
        messages.error(request, "Socio seleccionado no válido.")
        return HttpResponseRedirect(reverse('master_control'))

    anotaciones_creadas = 0
    for key, value in request.POST.items():
        if key.startswith(f'stock_usado_{socio_id}_'):
            try:
                # Extraer producto_id del nombre del campo (ej: stock_usado_5_12 -> 12)
                producto_id = int(key.split('_')[-1])
                cantidad_str = value.strip()
                if cantidad_str: # Solo procesar si hay valor
                    cantidad = float(cantidad_str.replace(',', '.')) # Permitir coma decimal
                    if cantidad > 0:
                        # Obtener el producto
                        producto = Producto.objects.get(id=producto_id, es_stock=True)
                        # Crear la anotación
                        AnotacionStockConsumido.objects.create(
                            socio=socio,
                            producto=producto,
                            cantidad=cantidad,
                            anotado_por=request.user
                        )
                        anotaciones_creadas += 1
            except (ValueError, IndexError, Producto.DoesNotExist) as e:
                print(f"Error procesando campo {key}={value}: {e}")
                messages.warning(request, f"Error procesando anotación para campo {key}. Verifica el valor.")
                # Continuar con los siguientes campos

    if anotaciones_creadas > 0:
        messages.success(request, f"Se guardaron {anotaciones_creadas} anotaciones de stock para {socio.nombre}.")
    else:
        messages.info(request, f"No se introdujo ninguna cantidad de stock para {socio.nombre}.")

    return HttpResponseRedirect(reverse('master_control'))
# --- Vista para corregir cantidades de socios en la comanda ---
from django.views.decorators.http import require_POST

from pedidos.models import PropuestaCorreccionComanda  # Añadir al inicio del archivo si no está

@login_required
@require_POST
def corregir_cantidades_socios(request, comanda_id):
    """
    Permite proponer correcciones de cantidades de productos asignados a cada socio en una comanda.
    Ahora NO aplica los cambios directamente, sino que crea una propuesta para que el gestor la valide.
    """
    import json
    comanda = get_object_or_404(ComandaRecurrente, id=comanda_id)
    # Obtener los pedidos colectivos abiertos de esta comanda
    pedidos_actuales = PedidoColectivo.objects.filter(comanda=comanda, estado__in=['abierto', 'pendiente'])
    pedidos_actuales_ids = list(pedidos_actuales.values_list('id', flat=True))

    # Mapear (socio_id, producto_id) a cantidad
    cambios = []
    for key, value in request.POST.items():
        if key.startswith('cantidad_'):
            try:
                _, socio_id, producto_id = key.split('_')
                socio_id = int(socio_id)
                producto_id = int(producto_id)
                cantidad_str = value.strip()
                if cantidad_str == '':
                    continue
                cantidad = float(cantidad_str.replace(',', '.'))
                cambios.append({'socio_id': socio_id, 'producto_id': producto_id, 'cantidad': cantidad})
            except Exception as e:
                print(f"Error procesando campo {key}: {e}")
                continue

    if not cambios:
        messages.info(request, "No se detectaron cambios para proponer.")
        return redirect('gestionar_comanda', comanda_id=comanda.id)

    # Crear la propuesta de corrección (estado pendiente)
    PropuestaCorreccionComanda.objects.create(
        comanda=comanda,
        usuario=request.user,
        cambios=json.dumps(cambios),
        estado='pendiente'
    )

    # Notificar al gestor de la comanda (puedes mejorar esto con emails o notificaciones internas)
    if comanda.socio_asignado:
        messages.success(request, f"Propuesta enviada a gestión comanda ({comanda.socio_asignado.nombre}). Debe ser validada antes de aplicar los cambios.")
    else:
        messages.success(request, "Propuesta enviada. No hay gestor asignado a la comanda.")

    # Renderizar la misma página de master control con mensaje de éxito
    pedidos_abiertos = PedidoColectivo.objects.filter(estado__in=['abierto', 'pendiente']).order_by('fecha_cierre')
    from socios.models import Socio
    from productos.models import Producto
    todos_los_socios = Socio.objects.all().order_by('nombre', 'apellido')
    productos_de_stock = Producto.objects.filter(es_stock=True).order_by('nombre')
    # (Resto de lógica de master_control_view para resumen_por_pedido...)
    # Para simplificar, redirigimos a master_control pero con mensaje flash
    messages.info(request, "Tus correcciones han sido guardadas como propuesta. Los cambios NO se aplicarán hasta que el gestor de la comanda los valide.")
    # Redirección según si el usuario es gestor o no
    if comanda.socio_asignado and comanda.socio_asignado.user == request.user:
        return redirect('gestionar_comanda', comanda_id=comanda.id)
    else:
        return redirect('master_control')
# --- Fin vista corregir cantidades ---

# --- NUEVA VISTA: Mis Pedidos (Historial) ---
@login_required
def mis_pedidos(request):
    """
    Muestra un historial de todos los pedidos (abiertos, pendientes, inactivos)
    en los que el socio actual ha participado.
    """
    # --- Comprobación de perfil de socio ---
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Tu usuario no tiene un perfil de socio asociado.")
        return redirect('dashboard_principal')
    # --- Fin comprobación ---
    socio = request.user.socio

    # Obtener los IDs de los pedidos en los que el socio tiene una selección
    pedidos_ids_participados = SeleccionSocio.objects.filter(socio=socio).values_list('pedido_id', flat=True).distinct()

    # Obtener los objetos PedidoColectivo correspondientes, ordenados por fecha de entrega descendente
    pedidos_participados = PedidoColectivo.objects.filter(id__in=pedidos_ids_participados).order_by('-fecha_entrega')

    # Opcional: Obtener detalles de cada pedido para mostrar en la plantilla
    detalles_por_pedido = {}
    for pedido in pedidos_participados:
        try:
            seleccion = SeleccionSocio.objects.get(pedido=pedido, socio=socio)
            detalles = DetalleSeleccion.objects.filter(seleccion=seleccion).select_related('producto')
            total_pedido = sum(d.cantidad * d.producto.precio for d in detalles if d.producto.precio is not None)
            detalles_por_pedido[pedido.id] = {
                'detalles': detalles,
                'total': total_pedido
            }
        except SeleccionSocio.DoesNotExist:
            detalles_por_pedido[pedido.id] = {'detalles': [], 'total': 0}


    context = {
        'pedidos_participados': pedidos_participados,
        'detalles_por_pedido': detalles_por_pedido,
    }
    return render(request, 'pedidos/mis_pedidos.html', context)
# --- FIN NUEVA VISTA ---

# --- Fin vista guardar anotaciones ---

# --- Nueva vista para guardar cambios en comanda pendiente ---
from django.views.decorators.http import require_POST
from django.db import transaction
from socios.models import Socio # Asegurarse de que Socio está importado
from decimal import Decimal, InvalidOperation

@login_required
@require_POST
@transaction.atomic
def guardar_cambios_comanda_pendiente(request, comanda_id):
    """
    Guarda los cambios de cantidad enviados desde el formulario de gestión de comanda,
    pero SOLO si el pedido asociado está en estado 'pendiente'.
    NO finaliza la comanda ni descuenta de monederos.
    """
    comanda = get_object_or_404(ComandaRecurrente, id=comanda_id)

    # --- Permisos y Estado ---
    # Solo el gestor puede guardar cambios
    if not comanda.socio_asignado or comanda.socio_asignado.user != request.user:
        messages.error(request, "No tienes permiso para guardar cambios en esta comanda.")
        return redirect('gestionar_comanda', comanda_id=comanda.id)

    # Buscar el pedido colectivo asociado que esté 'pendiente'
    pedido_pendiente = PedidoColectivo.objects.filter(comanda=comanda, estado='pendiente').first()

    if not pedido_pendiente:
        messages.error(request, "No se encontró un pedido en estado 'pendiente' asociado a esta comanda para guardar cambios.")
        return redirect('gestionar_comanda', comanda_id=comanda.id)
    # --- Fin Permisos y Estado ---


    # --- INICIO: Procesar cambios de cantidad enviados (copiado y adaptado de finalizar_comanda) ---
    cambios_realizados = 0
    # Usamos el ID del pedido pendiente encontrado
    pedido_actual_id = pedido_pendiente.id

    for key, value in request.POST.items():
        if key.startswith('cantidad_'):
            try:
                parts = key.split('_')
                # Verificar que tenemos exactamente 3 partes y que socio/producto ID no están vacíos
                if len(parts) == 3 and parts[1] and parts[2]:
                    socio_id_str = parts[1]
                    producto_id_str = parts[2]
                    socio_id = int(socio_id_str)
                    producto_id = int(producto_id_str)
                else:
                    # Si el formato no es cantidad_X_Y, ignorar este campo silenciosamente o loggear
                    print(f"WARN: Ignorando campo con formato inesperado: {key}")
                    continue # Saltar al siguiente item del POST

                cantidad_str = value.strip()
                if cantidad_str == '': # Si está vacío, tratar como 0
                    cantidad = Decimal('0.0') # Usar Decimal
                else:
                    try:
                        cantidad = Decimal(cantidad_str.replace(',', '.'))
                    except InvalidOperation:
                        messages.warning(request, f"Valor inválido '{cantidad_str}' para {key}. Se ignorará.")
                        continue # Saltar este campo

                # Obtener O CREAR la selección del socio para ESTE pedido pendiente específico
                # Necesitamos el objeto Socio para crearlo si no existe
                try:
                    # Intentamos obtener o crear la SeleccionSocio directamente
                    seleccion, created_seleccion = SeleccionSocio.objects.get_or_create(
                        pedido_id=pedido_actual_id, # Filtrar por el pedido pendiente
                        socio_id=socio_id, # Usamos socio_id directamente
                        # No necesitamos defaults aquí si el modelo lo permite
                    )
                    if created_seleccion:
                        # Opcional: podrías loggear esto si quieres saber cuándo se crea una selección nueva
                        pass
                except Exception as e: # Captura más genérica por si hay otros problemas (ej. FK a Socio)
                     print(f"ERROR: No se pudo obtener/crear SelecciónSocio para socio {socio_id} en pedido {pedido_actual_id}. Error: {e}. Ignorando campo {key}.")
                     continue # Saltar al siguiente campo

                # Obtener o crear/actualizar/eliminar el detalle
                detalle, created_detalle = DetalleSeleccion.objects.get_or_create(
                    seleccion=seleccion,
                    producto_id=producto_id,
                    defaults={'cantidad': cantidad} # Solo se usa si se crea
                )

                if not created_detalle: # Si el detalle ya existía...
                    if cantidad > 0:
                        # Convertir detalle.cantidad a Decimal si no lo es, para comparación segura
                        try:
                            # Asegurarse que detalle.cantidad no es None antes de str()
                            detalle_cantidad_str = str(detalle.cantidad) if detalle.cantidad is not None else '0'
                            detalle_cantidad_decimal = Decimal(detalle_cantidad_str)
                        except InvalidOperation:
                             detalle_cantidad_decimal = Decimal('0') # Fallback

                        if detalle_cantidad_decimal != cantidad: # Solo actualizar si hay cambio real
                            detalle.cantidad = cantidad
                            detalle.save()
                            cambios_realizados += 1
                    else: # Si la cantidad nueva es 0 o menos, eliminar el detalle existente
                        detalle.delete()
                        cambios_realizados += 1 # Contamos la eliminación como un cambio
                # Si el detalle se acaba de crear (created_detalle es True)...
                elif cantidad <= 0: # ...y se creó con 0 o menos, eliminarlo inmediatamente
                    detalle.delete()
                    # No contamos como cambio si se crea y elimina al instante
                else: # ...y se creó con cantidad > 0, sí lo contamos como cambio
                    cambios_realizados += 1

            except (ValueError, IndexError, Producto.DoesNotExist, InvalidOperation) as e:
                messages.error(request, f"Error procesando el campo {key}={value}: {e}. No se aplicaron todos los cambios.")
                print(f"Error procesando campo {key}={value}: {e}")
                continue
            except SeleccionSocio.DoesNotExist:
                 print(f"Error: No se encontró SelecciónSocio para {key}={value}")
                 continue


    if cambios_realizados > 0:
        messages.success(request, f"Se guardaron {cambios_realizados} cambios en las cantidades del pedido pendiente.")
    else:
        messages.info(request, "No se detectaron cambios para guardar.")
    # --- FIN: Procesar cambios de cantidad enviados ---

    # Redirigir de vuelta a la gestión de la comanda, a la pestaña de pedidos
    redirect_url = reverse('gestionar_comanda', kwargs={'comanda_id': comanda.id})
    redirect_url_with_fragment = f"{redirect_url}#tab-pedidos"
    return HttpResponseRedirect(redirect_url_with_fragment)
# --- Fin nueva vista ---

# --- Vistas para la Funcionalidad de "Desitjos" ---
from desitjos.models import CartaDeseo, InteresSocioEnCarta # Importar modelos de Desitjos
# from .forms import InteresSocioEnCartaForm, InteresSocioEnCartaFormSet # Comentado temporalmente hasta crear los formularios

@login_required
def listar_cartas_deseo_view(request):
    # Mostrar cartas activas y aquellas donde el mínimo ha sido alcanzado pero aún no completadas/archivadas
    cartas_visibles = CartaDeseo.objects.filter(
        estado__in=['activa', 'minimo_alcanzado']
    ).prefetch_related('productos').order_by('-fecha_creacion')
    
    # Opcional: Paginación
    paginator = Paginator(cartas_visibles, 10) # 10 cartas por página
    page_number = request.GET.get('page')
    try:
        cartas_pagina = paginator.page(page_number)
    except PageNotAnInteger:
        cartas_pagina = paginator.page(1)
    except EmptyPage:
        cartas_pagina = paginator.page(paginator.num_pages)

    context = {
        'cartas_deseo': cartas_pagina,
    }
    return render(request, 'pedidos/desitjos/listar_cartas.html', context)

@login_required
def detalle_carta_deseo_view(request, carta_id):
    carta = get_object_or_404(CartaDeseo.objects.prefetch_related('productos', 'intereses_socios__socio', 'intereses_socios__producto'), id=carta_id)
    
    # Verificar si el socio actual ya tiene interés registrado para los productos de esta carta
    intereses_socio_actual = {}
    if hasattr(request.user, 'socio'):
        intereses_existentes = InteresSocioEnCarta.objects.filter(
            carta_deseo=carta,
            socio=request.user.socio
        ).select_related('producto')
        for interes in intereses_existentes:
            intereses_socio_actual[interes.producto.id] = interes.cantidad_deseada

    # Preparar datos iniciales para el formset
    initial_data_formset = []
    for producto in carta.productos.all():
        initial_data_formset.append({
            'producto_id': producto.id, # Usaremos un campo oculto para el ID del producto
            'producto_nombre': producto.nombre, # Para mostrar en la plantilla
            'unidad_venta': producto.get_unidad_venta_display(), # Para mostrar en la plantilla
            'cantidad_deseada': intereses_socio_actual.get(producto.id, Decimal('0.000'))
        })

    # Crear el formset
    # Asumimos que InteresSocioEnCartaFormSet se definirá en pedidos/forms.py
    # y que tomará 'initial' y un queryset para los productos si es necesario.
    # Por ahora, lo manejaremos más directamente en la vista y plantilla.

    context = {
        'carta_deseo': carta,
        'initial_data_formset': initial_data_formset,
        # 'formset': formset, # Si usamos un FormSet de Django
    }
    return render(request, 'pedidos/desitjos/detalle_carta.html', context)

@login_required
@require_POST # Esta vista solo debería aceptar POST
def registrar_interes_en_carta_view(request, carta_id):
    if not hasattr(request.user, 'socio'):
        messages.error(request, "Has d'estar registrat com a soci per indicar interès.")
        return redirect('listar_cartas_deseo')

    carta = get_object_or_404(CartaDeseo, id=carta_id)
    if carta.estado not in ['activa', 'minimo_alcanzado']: # Solo se puede registrar interés en cartas activas o con mínimo alcanzado
        messages.error(request, "Aquesta carta de desig no accepta nous interessos actualment.")
        return redirect('detalle_carta_deseo', carta_id=carta.id)

    socio_actual = request.user.socio
    productos_de_la_carta = carta.productos.all()
    
    for producto in productos_de_la_carta:
        cantidad_key = f'cantidad_producto_{producto.id}'
        cantidad_str_from_post = request.POST.get(cantidad_key)

        if cantidad_str_from_post is None:
            # Si el campo no está en el POST (ej. input vacío que el navegador no envía),
            # no hacemos nada para este producto, conservando el interés existente.
            continue

        cantidad_str = cantidad_str_from_post.strip()
        
        if not cantidad_str: # Si se envió pero está vacío, tratar como 0
            cantidad_deseada = Decimal('0')
        else:
            try:
                cantidad_deseada = Decimal(cantidad_str.replace(',', '.'))
                if cantidad_deseada < Decimal('0'): # No permitir cantidades negativas
                    cantidad_deseada = Decimal('0')
            except InvalidOperation:
                messages.warning(request, f"La quantitat introduïda per a '{producto.nombre}' no és vàlida ('{cantidad_str}') i s'ha ignorat.")
                continue # Saltar este producto y continuar con el siguiente

        if producto.unidad_venta == 'ud': # Forzar a entero si es por unidad
            cantidad_deseada = cantidad_deseada.to_integral_value(rounding='ROUND_DOWN')

        # Obtener el interés existente, si lo hay
        interes_existente = InteresSocioEnCarta.objects.filter(
            carta_deseo=carta,
            socio=socio_actual,
            producto=producto
        ).first()

        if cantidad_deseada > Decimal('0'):
            if interes_existente:
                if interes_existente.cantidad_deseada != cantidad_deseada:
                    interes_existente.cantidad_deseada = cantidad_deseada
                    interes_existente.save() # Esto llamará a carta_deseo.actualizar_estado_minimo()
            else:
                InteresSocioEnCarta.objects.create(
                    carta_deseo=carta,
                    socio=socio_actual,
                    producto=producto,
                    cantidad_deseada=cantidad_deseada
                ) # El save del modelo llamará a actualizar_estado_minimo()
        else: # Si la cantidad deseada es 0 (o menos, aunque ya lo corregimos)
            if interes_existente:
                interes_existente.delete()
                # Después de borrar, también es bueno recalcular el estado mínimo de la carta
                carta.actualizar_estado_minimo()
            
    # La lógica de actualizar_estado_minimo() se llama en el save() o después del delete()
    messages.success(request, f"El teu interès per a la carta '{carta.titulo}' ha estat registrat/actualitzat.")
    return redirect('listar_cartas_deseo') # Redirigir a la lista de cartas


@login_required
# @user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'socio') and u.socio.puede_gestionar_deseos)) # TODO: Definir permiso
def panel_gestio_desitjos_view(request):
    # Vista para administradores/gestores
    # Agrupar intereses por CartaDeseo y luego por Producto
    cartas_con_interes = CartaDeseo.objects.filter(
        estado__in=['activa', 'minimo_alcanzado'] # Mostrar solo las relevantes para gestión
    ).annotate(
        num_interesados_total=Count('intereses_socios__socio', distinct=True)
    ).prefetch_related('productos', 'intereses_socios__socio', 'intereses_socios__producto').order_by('-fecha_creacion')

    resumen_interes_por_carta = []
    for carta in cartas_con_interes:
        productos_info = []
        for producto_carta in carta.productos.all():
            intereses_producto = InteresSocioEnCarta.objects.filter(carta_deseo=carta, producto=producto_carta)
            cantidad_total_deseada = intereses_producto.aggregate(total=Sum('cantidad_deseada'))['total'] or Decimal('0')
            num_socios_interesados = intereses_producto.values('socio').distinct().count()
            productos_info.append({
                'producto': producto_carta,
                'cantidad_total_deseada': cantidad_total_deseada,
                'num_socios_interesados': num_socios_interesados,
            })
        resumen_interes_por_carta.append({
            'carta': carta,
            'productos_info': productos_info,
            'num_interesados_total_en_carta': carta.num_interesados_total
        })
        
    context = {
        'resumen_interes_por_carta': resumen_interes_por_carta,
    }
    return render(request, 'pedidos/desitjos/panel_gestio.html', context)

# Asegúrate de importar Decimal y InvalidOperation de la librería decimal
from decimal import Decimal, InvalidOperation

# --- Nueva vista para crear comandas esporádicas por socios ---
from .forms import ComandaEsporadicaSocioForm # Asegúrate que el form está importado
from django.contrib.auth.decorators import user_passes_test

def socio_puede_crear_comanda_esporadica(user):
    if hasattr(user, 'socio') and user.socio:
        return user.socio.puede_crear_comandas_esporadicas
    return False

@login_required
@user_passes_test(socio_puede_crear_comanda_esporadica, login_url='/url/a/pagina/de/no_permiso/') # Redirigir si no pasa el test
def crear_comanda_esporadica_socio(request):
    if not hasattr(request.user, 'socio') or not request.user.socio: # Doble check y asegurar que el socio existe
        messages.error(request, "Has de tenir un perfil de soci per realitzar aquesta acció.") # Traducido
        return redirect('socios_home') # O alguna página de inicio relevante

    if request.method == 'POST':
        form = ComandaEsporadicaSocioForm(request.POST)
        if form.is_valid():
            comanda = form.save(commit=False)
            comanda.frecuencia = 'esporadico'
            comanda.socio_asignado = request.user.socio
            comanda.estado = 'activa'
            # dia_semana y dia_mes no son necesarios para esporádicas y deben ser null/blank en el modelo
            comanda.save()
            messages.success(request, f"Comanda esporàdica '{comanda.nombre}' creada amb èxit.") # Traducido
            # Idealmente, redirigir a una vista que muestre las comandas del socio o un panel.
            # Por ahora, redirigimos a 'seleccionar_comanda' que lista las comandas asignadas.
            return redirect('seleccionar_comanda')
    else:
        form = ComandaEsporadicaSocioForm()

    context = {
        'form': form,
        'titulo_pagina': 'Crear Nova Comanda Esporàdica' # Traducido
    }
    return render(request, 'pedidos/crear_comanda_esporadica_socio.html', context)
# --- Fin nueva vista ---
