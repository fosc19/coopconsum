# coopconsum/views.py
import json
import datetime
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test # Para permisos de superusuario
from django.urls import reverse
from django.shortcuts import redirect # Añadir redirect
from django.contrib import messages # Para mensajes de feedback
from socios.models import Socio, CuentaSocio, MovimientoCuenta, RegistroCompraSocio # Importar el nuevo modelo
from socios.forms import RegistroCompraSocioForm # Importar el nuevo formulario
from pedidos.models import PedidoColectivo, SeleccionSocio
from django.http import HttpResponseRedirect

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

    from eventos.models import EventoCalendario # Importar el modelo EventoCalendario

    # Obtener eventos del modelo EventoCalendario
    eventos_calendario = EventoCalendario.objects.all().order_by('fecha') # O filtrar por rango de fechas si es necesario

    events = []

    # Añadir eventos del modelo EventoCalendario
    for evento in eventos_calendario:
        events.append({
            'title': evento.titulo,
            'start': evento.fecha.isoformat(),
            'description': evento.descripcion,
            'color': evento.color,
            'allDay': True, # Mostrar como evento de día completo
            # Puedes añadir más campos si tu modelo o librería de calendario los soporta
        })

    # Obtener pedidos colectivos abiertos para el calendario
    pedidos_calendario = PedidoColectivo.objects.filter(estado='abierto').order_by('fecha_apertura')

    # Añadir pedidos colectivos como eventos
    for p in pedidos_calendario:
        prov_name = p.proveedor.nombre if p.proveedor else "Sin prov."
        events.append({
            'title': f"Comanda: {prov_name}", # Título más descriptivo
            'start': p.fecha_apertura.strftime('%Y-%m-%d'),
            'end': (p.fecha_cierre + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), # Evento de rango
            'allDay': True,
            'url': reverse('seleccionar_pedido', args=[p.id]), # Enlace a la página de selección
            'color': '#28a745', # Color verde para pedidos abiertos (ejemplo)
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

# Vista para la sección Master (asumiendo que existe o se creará)
# Si ya existe una vista 'master_control', esta nueva funcionalidad
# podría integrarse allí o ser una vista separada como se hace aquí.
@login_required
@user_passes_test(lambda u: u.is_superuser) # Solo superusuarios
def master_control_view(request):
    # Lógica existente de la vista master (si la hay)
    # ...
    # Por ahora, solo renderiza una plantilla simple o redirige
    # a la nueva funcionalidad si es la única parte del master.
    # return render(request, 'master/master_dashboard.html') # Ejemplo
    # O redirigir directamente a la nueva función:
    return redirect('registrar_compra_socio')


# Nueva vista para registrar compras de socios manualmente
@login_required
# @user_passes_test(lambda u: u.is_superuser) # Eliminado: Ahora accesible para todos los logueados
def registrar_compra_socio_view(request):
    if request.method == 'POST':
        form = RegistroCompraSocioForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.registrado_por = request.user # Guardar quién hizo el registro
            registro.save()
            messages.success(request, f"Compra de {registro.cantidad} {registro.producto.get_unidad_venta_display()} de '{registro.producto.nombre}' registrada para {registro.socio}.")
            # Redirigir a la misma página para limpiar el formulario y ver el nuevo registro en la lista
            return redirect('registrar_compra_socio')
        else:
            messages.error(request, "Error al registrar la compra. Por favor, revisa los datos del formulario.")
    else:
        form = RegistroCompraSocioForm()

    # Obtener los últimos registros para mostrarlos en la página
    ultimos_registros = RegistroCompraSocio.objects.select_related('socio', 'producto', 'registrado_por').order_by('-fecha_registro')[:20] # Mostrar los últimos 20

    context = {
        'form': form,
        'ultimos_registros': ultimos_registros,
    }
    # Usaremos una nueva plantilla para esta funcionalidad
    return render(request, 'master/registrar_compra_socio.html', context)

def custom_logout(request):
    """Vista personalizada de logout que accepta GET i POST requests"""
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/')


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
