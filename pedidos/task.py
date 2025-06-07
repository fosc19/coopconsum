from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import PedidoColectivo, ComandaRecurrente

@shared_task
def generar_pedidos_recurrentes():
    hoy = timezone.now().date()
    comandas = ComandaRecurrente.objects.filter(
        estado='activa',
        fecha_inicio__lte=hoy
    ).exclude(fecha_fin__lt=hoy)

    for comanda in comandas:
        generar = False
        dias_ciclo = 0
        dias_apertura_offset = 0 # timedelta usa N-1 para N días de apertura
        dias_entrega_offset = 0  # timedelta desde apertura hasta entrega

        if comanda.frecuencia == 'semanal':
            dias_ciclo = 7
            dias_apertura_offset = 6  # Abierta 7 días
            dias_entrega_offset = 9   # Entrega 3 días después de cierre
        elif comanda.frecuencia == 'quincenal':
            dias_ciclo = 14
            # Duración siempre semanal (7 días)
            dias_apertura_offset = 6
            dias_entrega_offset = 9
        elif comanda.frecuencia == 'mensual': # Basado en 4 semanas = 28 días
            dias_ciclo = 28
            # Duración siempre semanal (7 días)
            dias_apertura_offset = 6
            dias_entrega_offset = 9

        # --- Lógica para frecuencias periódicas (semanal, quincenal, mensual) ---
        if dias_ciclo > 0:
            # Verificar si es el día de la semana correcto
            if comanda.dia_semana and hoy.strftime('%A').lower() == comanda.dia_semana:
                # Verificar si es la primera generación o si ya pasó el ciclo
                if comanda.ultima_generacion is None:
                    # Primera generación: solo verificar fecha_inicio
                    if hoy >= comanda.fecha_inicio:
                        generar = True
                else:
                    # Generaciones siguientes: verificar si han pasado suficientes días
                    if (hoy - comanda.ultima_generacion).days >= dias_ciclo:
                        generar = True

            # Si se cumplen las condiciones, generar el pedido periódico
            if generar:
                PedidoColectivo.objects.create(
                    comanda=comanda,
                    fecha_apertura=timezone.now(),
                    fecha_cierre=timezone.now() + timedelta(days=dias_apertura_offset),
                    fecha_entrega=timezone.now() + timedelta(days=dias_entrega_offset),
                    tipo=comanda.frecuencia, # Usar la frecuencia como tipo
                    estado='abierto',
                    categoria=comanda.categoria,
                    proveedor=comanda.proveedor,
                    socio=comanda.socio_asignado
                )
                # Actualizar la fecha de última generación
                comanda.ultima_generacion = hoy
                comanda.save(update_fields=['ultima_generacion'])

        # --- Lógica para frecuencia esporádica (se mantiene igual) ---
        elif comanda.frecuencia == 'esporadico':
            # Genera el pedido esporádico solo si no existe ya uno para esta comanda
            if not PedidoColectivo.objects.filter(comanda=comanda).exists():
                PedidoColectivo.objects.create(
                    comanda=comanda,
                    fecha_apertura=timezone.now(),
                    # Abierto por 7 días (cerrando al inicio del 8º día)
                    fecha_cierre=timezone.now() + timedelta(days=6),
                    # Entrega 3 días después del cierre
                    fecha_entrega=timezone.now() + timedelta(days=9),
                    tipo='esporadico',
                    estado='abierto',
                    categoria=comanda.categoria,
                    proveedor=comanda.proveedor,
                    socio=comanda.socio_asignado
                )
        # Nota: No se actualiza ultima_generacion para esporádico
