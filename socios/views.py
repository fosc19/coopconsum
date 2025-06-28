from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CuentaSocio, MovimientoCuenta, Socio # Importar Socio para la excepción
from django.db import models
from django.core.paginator import Paginator # Importar Paginator


@login_required
def home(request):
    from pedidos.models import SeleccionSocio, DetalleSeleccion, PedidoColectivo, ComandaRecurrente
    from desitjos.models import CartaDeseo, InteresSocioEnCarta # Importar modelos de Desitjos
    try:
        socio = request.user.socio
    except Socio.DoesNotExist:
        # Si el usuario logueado no tiene perfil de socio, mostrar error.
        return render(request, 'socios/panel_socio.html', {'error_no_socio': True})

    # Obtener todas las selecciones del socio
    selecciones = SeleccionSocio.objects.filter(socio=socio).select_related('pedido')
    comandas_dict = {}

    for seleccion in selecciones:
        pedido = seleccion.pedido
        comanda = pedido.comanda
        detalles = DetalleSeleccion.objects.filter(seleccion=seleccion)
        # Calculamos el total gastado para ESTE pedido específico
        total_gastado_pedido_actual = sum(d.cantidad * d.producto.precio for d in detalles)
        if comanda:
            # Comanda recurrente
            if comanda.id not in comandas_dict:
                comandas_dict[comanda.id] = {
                    'nombre': comanda.nombre,
                    'estado': pedido.estado, # Guardar estado del PEDIDO
                    'fecha_apertura': pedido.fecha_apertura, # Fecha del primer pedido encontrado para esta comanda
                    'total_gastado': total_gastado_pedido_actual, # Total del primer pedido encontrado
                    'id': comanda.id,
                    'tipo': 'recurrente',
                    'pedido_id': pedido.id, # ID del primer pedido encontrado
                }
            else:
                # Si este pedido es más reciente que el que ya tenemos guardado para esta comanda...
                if pedido.fecha_apertura > comandas_dict[comanda.id]['fecha_apertura']:
                    # ...actualizamos los datos para reflejar este pedido más reciente
                    comandas_dict[comanda.id]['pedido_id'] = pedido.id
                    comandas_dict[comanda.id]['fecha_apertura'] = pedido.fecha_apertura
                    comandas_dict[comanda.id]['estado'] = pedido.estado # Actualizar estado al del PEDIDO más reciente
                    # Y lo más importante: SOBREESCRIBIMOS el total gastado con el de este pedido más reciente
                    comandas_dict[comanda.id]['total_gastado'] = total_gastado_pedido_actual
                # Si no es más reciente, no hacemos nada, mantenemos los datos del pedido más reciente que ya teníamos.
        else:
            # Comanda esporádica (pedido sin comanda asociada)
            key = f"esporadico_{pedido.id}"
            comandas_dict[key] = {
                'nombre': pedido.categoria.nombre if pedido.categoria else "Esporádico",
                'estado': pedido.estado,
                'fecha_apertura': pedido.fecha_apertura,
                'total_gastado': total_gastado_pedido_actual,
                'id': pedido.id,
                'tipo': 'esporadico',
                'pedido_id': pedido.id,
            }

    # Filtrar comandas/pedidos por estado
    comandas_activas = []
    comandas_pendientes = []
    comandas_inactivas = []
    
    # Filtrar comandas/pedidos por estado (ya no se imprimen)
    for comanda_data in comandas_dict.values():
        # print(f"Pedido ID: {comanda_data['pedido_id']}, Estado: {comanda_data['estado']}") # Eliminado print
        
        if comanda_data['estado'] == 'abierto':
            comandas_activas.append(comanda_data)
        elif comanda_data['estado'] == 'pendiente':
            comandas_pendientes.append(comanda_data)
        elif comanda_data['estado'] in ['inactivo', 'cerrado']:  # Considerar también 'cerrado' como inactivo
            comandas_inactivas.append(comanda_data)

    # Ordenar por fecha (más recientes primero)
    comandas_activas = sorted(comandas_activas, key=lambda c: c['fecha_apertura'], reverse=True)
    comandas_pendientes = sorted(comandas_pendientes, key=lambda c: c['fecha_apertura'], reverse=True)
    comandas_inactivas = sorted(comandas_inactivas, key=lambda c: c['fecha_apertura'], reverse=True)
    
    # Combinar pedidos abiertos y pendientes para mostrar en la parte superior
    comandas_actuales = comandas_activas + comandas_pendientes
    comandas_actuales = sorted(comandas_actuales, key=lambda c: c['fecha_apertura'], reverse=True)[:5]

    # Diccionario para el detalle de cada comanda/pedido del socio
    detalles_comandas = {}
    for seleccion in selecciones:
        pedido = seleccion.pedido
        comanda = pedido.comanda
        detalles = DetalleSeleccion.objects.filter(seleccion=seleccion)
        productos = []
        for d in detalles:
            productos.append({
                'nombre': d.producto.nombre,
                'cantidad': d.cantidad,
                'precio': d.producto.precio,
                'subtotal': d.cantidad * d.producto.precio,
                'unidad': d.producto.get_unidad_venta_display() if hasattr(d.producto, 'get_unidad_venta_display') else '',
            })
        key = comanda.id if comanda else pedido.id
        detalles_comandas[key] = productos

    # Obtener los últimos 5 movimientos del monedero del socio
    try:
        cuenta = CuentaSocio.objects.get(socio=socio)
        movimientos = MovimientoCuenta.objects.filter(
            cuenta=cuenta,
            estado__in=["validado", "pendiente"]
        ).order_by('-fecha')[:5]
    except CuentaSocio.DoesNotExist:
        movimientos = []

    # Calcular el saldo total del socio (solo movimientos validados)
    saldo = 0
    if 'cuenta' in locals():
        saldo = MovimientoCuenta.objects.filter(
            cuenta=cuenta,
            estado="validado"
        ).aggregate(total_sum=models.Sum('monto'))['total_sum'] or 0

    # Obtener pedidos en los que el socio ha participado (para el historial)
    from pedidos.models import PedidoColectivo
    pedidos_ids_participados = SeleccionSocio.objects.filter(socio=socio).values_list('pedido_id', flat=True).distinct()
    pedidos_participados = PedidoColectivo.objects.filter(id__in=pedidos_ids_participados).order_by('-fecha_entrega')
    
    # Obtener detalles de cada pedido para mostrar en la plantilla
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

    # Ya no se imprimen los pedidos inactivos
    # print(f"Total de pedidos inactivos encontrados: {len(comandas_inactivas)}") # Eliminado print
    # for i, comanda in enumerate(comandas_inactivas[:3]):
    #     print(f"Pedido inactivo {i+1}: ID={comanda['id']}, Nombre={comanda['nombre']}") # Eliminado print

    # Paginación para pedidos_participados
    paginator = Paginator(pedidos_participados, 5) # Mostrar 5 pedidos por página
    page_number = request.GET.get('page')
    pedidos_pagina = paginator.get_page(page_number)

    # Obtener los deseos del socio
    mis_intereses_activos = []
    if socio:
        # Obtener todas las cartas activas o con mínimo alcanzado
        cartas_deseo_relevantes = CartaDeseo.objects.filter(
            estado__in=['activa', 'minimo_alcanzado']
        ).prefetch_related('productos')

        for carta in cartas_deseo_relevantes:
            intereses_en_esta_carta = InteresSocioEnCarta.objects.filter(
                carta_deseo=carta,
                socio=socio
            ).select_related('producto')
            
            # Si el socio tiene algún interés en esta carta, o si queremos mostrar todas las cartas activas
            # independientemente de si ha participado, ajustamos la lógica.
            # Por ahora, solo mostraremos las cartas donde tiene interés o todas las activas.
            # Para simplificar, mostraremos todas las cartas activas y marcaremos su interés.
            
            productos_con_interes = []
            for producto_carta in carta.productos.all():
                interes_producto_actual = None
                for interes in intereses_en_esta_carta:
                    if interes.producto == producto_carta:
                        interes_producto_actual = interes
                        break
                productos_con_interes.append({
                    'producto': producto_carta,
                    'cantidad_deseada': interes_producto_actual.cantidad_deseada if interes_producto_actual else Decimal('0.000'),
                    'tiene_interes': interes_producto_actual is not None
                })

            mis_intereses_activos.append({
                'carta': carta,
                'productos_con_interes': productos_con_interes,
                'algun_interes_en_carta': any(p['tiene_interes'] for p in productos_con_interes)
            })
    
    # Filtrar para mostrar solo las cartas donde el socio tiene algún interés o todas las activas
    # Esto es una simplificación, se podría hacer más eficiente si solo se quieren las que tienen interés.
    # mis_desitjos_filtrados = [interes for interes in mis_intereses_activos if interes['algun_interes_en_carta']]
    # O simplemente pasar todas las cartas activas y que la plantilla decida:
    mis_desitjos_filtrados = mis_intereses_activos


    context = {
        'comandas': comandas_actuales,
        'movimientos': movimientos,
        'detalles_comandas': detalles_comandas,
        'saldo': saldo,
        'pedidos_pagina': pedidos_pagina,
        'detalles_por_pedido': detalles_por_pedido,
        'mis_desitjos': mis_desitjos_filtrados, # Añadir deseos al contexto
    }
    # Añadir la URL de la API de eventos al contexto
    context['api_eventos_url'] = reverse('api_eventos_calendario')
    return render(request, 'socios/panel_socio.html', context)

@login_required
def enviar_ingreso(request):
    import logging
    from django.contrib import messages
    from .forms import IngresoForm
    
    # Logger opcional - no falla si no está configurado
    try:
        logger = logging.getLogger('socios')
    except:
        logger = None
    
    def safe_log(level, message):
        """Función para logging seguro que no falla si no está configurado"""
        try:
            if logger:
                getattr(logger, level)(message)
        except:
            pass  # Ignorar errores de logging para no afectar la funcionalidad
    
    if request.method == "POST":
        form = IngresoForm(request.POST, request.FILES)
        
        safe_log('info', f"Intento de envío de ingreso - Usuario: {request.user.username}")
        
        if form.is_valid():
            try:
                # Verificar que el usuario tiene perfil de socio
                try:
                    socio = request.user.socio
                    safe_log('info', f"Socio encontrado: {socio.nombre} {socio.apellido} (ID: {socio.id})")
                except Socio.DoesNotExist:
                    messages.error(request, "L'usuari actual no té un perfil de soci associat.")
                    safe_log('error', f"Envío de ingreso fallido - Usuario sin perfil de socio: {request.user.username}")
                    return HttpResponseRedirect(reverse('socios_home'))
                
                # Obtener o crear cuenta del socio
                try:
                    cuenta, created = CuentaSocio.objects.get_or_create(socio=socio)
                    if created:
                        safe_log('info', f"Cuenta creada automáticamente para socio {socio.id}")
                    else:
                        safe_log('info', f"Cuenta existente encontrada para socio {socio.id}")
                except Exception as e:
                    messages.error(request, "Error al accedir al compte del soci.")
                    safe_log('error', f"Error al obtener/crear cuenta para socio {socio.id}: {e}")
                    return HttpResponseRedirect(reverse('socios_home'))
                
                # Obtener datos validados del formulario
                monto = form.cleaned_data['monto']
                comentario = form.cleaned_data['comentario']
                justificante = form.cleaned_data.get('justificante')
                
                # Si el comentari està buit, usar un text per defecte
                descripcion = comentario.strip() if comentario and comentario.strip() else "Ingrés enviat per validar"
                
                # Crear el movimiento
                try:
                    movimiento = MovimientoCuenta.objects.create(
                        cuenta=cuenta,
                        tipo_movimiento="ingreso",
                        monto=monto,
                        descripcion=descripcion,
                        estado="pendiente"
                    )
                    
                    # Ejecutar validaciones del modelo
                    movimiento.full_clean()
                    
                    safe_log('info', f"Movimiento creado exitosamente - ID: {movimiento.id}, Socio: {socio.id}, Monto: {monto}")
                    messages.success(request, f"Ingrés de {monto}€ enviat correctament per a validació.")
                    
                    # TODO: Manejar el archivo justificante si se implementa en el futuro
                    if justificante:
                        safe_log('info', f"Archivo justificante recibido: {justificante.name} (no se guarda por ahora)")
                    
                except Exception as e:
                    messages.error(request, "Error al crear el moviment. Si us plau, intenta-ho de nou.")
                    safe_log('error', f"Error al crear movimiento para socio {socio.id}: {e}")
                    return HttpResponseRedirect(reverse('socios_home'))
                    
            except Exception as e:
                messages.error(request, "Error inesperat. Si us plau, intenta-ho de nou.")
                safe_log('error', f"Error inesperado en enviar_ingreso: {e}")
                return HttpResponseRedirect(reverse('socios_home'))
        
        else:
            # El formulario no es válido, mostrar errores
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            
            safe_log('warning', f"Formulario de ingreso inválido - Usuario: {request.user.username}, Errores: {form.errors}")
    
    else:
        safe_log('warning', f"Intento de acceso GET a enviar_ingreso - Usuario: {request.user.username}")
    
    return HttpResponseRedirect(reverse('socios_home'))

# Asegurarse de importar Decimal
from decimal import Decimal
