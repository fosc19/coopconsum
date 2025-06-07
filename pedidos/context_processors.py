from .models import PropuestaCorreccionComanda, ComandaRecurrente, PedidoColectivo
from django.db.models import Q # Importar Q

def pedidos_info_processor(request): # Renombrada para reflejar que devuelve más información
    """
    Añade información sobre propuestas pendientes y pedidos listos para finalizar
    para el usuario actual al contexto.
    """
    propuestas_count = 0
    listos_para_finalizar_count = 0
    pedidos_abiertos_global_count = 0
    cartas_deseo_minimo_alcanzado_count = 0 # Nuevo contador para Desitjos

    if request.user.is_authenticated:
        # Contar todos los PedidoColectivo en estado 'abierto'
        # (Considerar si se deben aplicar filtros de fecha aquí, como en la vista pedidos_abiertos)
        from django.utils import timezone
        ahora = timezone.now()
        pedidos_abiertos_global_count = PedidoColectivo.objects.filter(
            Q(estado='abierto') &
            (Q(fecha_inicio_pedidos__isnull=True) | Q(fecha_inicio_pedidos__lte=ahora)) &
            Q(fecha_cierre__gte=ahora)
        ).count()

        # Contar cartas de deseo con mínimo alcanzado
        from desitjos.models import CartaDeseo # Importar desde la nueva app desitjos
        cartas_deseo_minimo_alcanzado_count = CartaDeseo.objects.filter(estado='minimo_alcanzado').count()

        if hasattr(request.user, 'socio'):
            socio = request.user.socio
            try:
                # Contar las propuestas pendientes en las comandas gestionadas por el socio actual
                propuestas_count = PropuestaCorreccionComanda.objects.filter(
                    comanda__socio_asignado=socio,
                    estado='pendiente'
                ).count()

                # Contar los PedidoColectivo en estado 'listo_para_finalizar' gestionados por el socio
                listos_para_finalizar_count = PedidoColectivo.objects.filter(
                    comanda__socio_asignado=socio,
                    estado='listo_para_finalizar'
                ).count()
            except Exception:
                # En caso de error, simplemente dejamos las cuentas en 0.
                pass
            
    return {
        'propuestas_pendientes_count': propuestas_count,
        'listos_para_finalizar_count': listos_para_finalizar_count,
        'pedidos_abiertos_global_count': pedidos_abiertos_global_count,
        'cartas_deseo_minimo_alcanzado_count': cartas_deseo_minimo_alcanzado_count, # Añadir nuevo contador
    }