# coopconsum/views.py
import json
import datetime
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from socios.models import Socio, CuentaSocio, MovimientoCuenta
from pedidos.models import PedidoColectivo, SeleccionSocio

@login_required
def panel_principal(request):
    try:
        socio = request.user.socio
    except Exception:
        socio = None

    try:
        cuenta_socio = CuentaSocio.objects.get(socio=socio)
    except CuentaSocio.DoesNotExist:
        cuenta_socio = None
    saldo = 0
    if cuenta_socio:
        saldo = MovimientoCuenta.objects.filter(
            cuenta=cuenta_socio,
            estado="validado"
        ).aggregate(total=models.Sum('monto'))['total'] or 0

    ultimos_movimientos = []
    if cuenta_socio:
        ultimos_movimientos = MovimientoCuenta.objects.filter(
            cuenta=cuenta_socio,
            estado="validado"
        ).order_by('-fecha')[:5]

    ultimas_comandas = SeleccionSocio.objects.filter(socio=socio).order_by('-fecha_seleccion')[:5]
    pedidos_abiertos = PedidoColectivo.objects.filter(estado='abierto').order_by('fecha_cierre')[:5]

    pedidos_calendario = PedidoColectivo.objects.filter(estado='abierto').order_by('fecha_apertura')
    events = []
    for p in pedidos_calendario:
        prov_name = p.proveedor.nombre if p.proveedor else "Sin prov."
        events.append({
            'title': prov_name,
            'start': p.fecha_apertura.strftime('%Y-%m-%d'),
            'end': (p.fecha_cierre + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            'allDay': True,
            'url': reverse('seleccionar_pedido', args=[p.id])
        })
    events_json = json.dumps(events)

    context = {
        'socio': socio,
        'saldo': saldo,
        'ultimos_movimientos': ultimos_movimientos,
        'ultimas_comandas': ultimas_comandas,
        'pedidos_abiertos': pedidos_abiertos,
        'events_json': events_json,
    }
    return render(request, 'panel_principal.html', context)

@login_required
def seleccionar_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoColectivo, id=pedido_id)
    return render(request, 'pedidos/seleccionar_pedido.html', {'pedido': pedido})

# primera versio interesant
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from socios.models import Socio, CuentaSocio, MovimientoCuenta
# from pedidos.models import PedidoColectivo, SeleccionSocio
#
# @login_required
# def panel_principal(request):
#     socio = request.user.socio
#
#     # Monedero
#     try:
#         cuenta_socio = CuentaSocio.objects.get(socio=socio)
#     except CuentaSocio.DoesNotExist:
#         cuenta_socio = None
#
#     saldo = cuenta_socio.saldo_actual if cuenta_socio else 0
#     ultimos_movimientos = []
#     if cuenta_socio:
#         ultimos_movimientos = MovimientoCuenta.objects.filter(cuenta=cuenta_socio).order_by('-fecha')[:5]
#
#     # Últimas comandas
#     ultimas_comandas = SeleccionSocio.objects.filter(socio=socio).order_by('-fecha_seleccion')[:5]
#
#     # Pedidos para el calendario (rango apertura-cierre)
#     pedidos_calendario = PedidoColectivo.objects.all().order_by('fecha_apertura')
#     # o si quieres solo futuros: .filter(fecha_cierre__gte=timezone.now())
#
#     context = {
#         'socio': socio,
#         'saldo': saldo,
#         'ultimos_movimientos': ultimos_movimientos,
#         'ultimas_comandas': ultimas_comandas,
#         'pedidos_calendario': pedidos_calendario,
#     }
#     return render(request, 'panel_principal.html', context)
