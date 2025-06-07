from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from pedidos.models import PedidoColectivo, ComandaRecurrente

# Diccionario para mapear días de la semana de inglés a español.
days_map = {
    "monday": "lunes",
    "tuesday": "martes",
    "wednesday": "miercoles",
    "thursday": "jueves",
    "friday": "viernes",
    "saturday": "sabado",
    "sunday": "domingo"
}

class Command(BaseCommand):
    # Modificado para indicar que es para pruebas
    help = 'Genera pedidos colectivos para PRUEBAS, ignorando ultima_generacion para pedidos periódicos.'

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        self.stdout.write(f"=== [TEST] Revisando comandas para el día {hoy} (ignora ultima_generacion) ===")

        # Filtrar las comandas activas y vigentes.
        comandas = ComandaRecurrente.objects.filter(
            estado='activa',
            fecha_inicio__lte=hoy
        ).filter(
            Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=hoy)
        )

        for comanda in comandas:
            if comanda.frecuencia == 'semanal':
                day_today_es = days_map[hoy.strftime('%A').lower()]
                self.stdout.write(
                    f"Comanda {comanda.nombre} (semanal): dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
                )
                if day_today_es == (comanda.dia_semana or '').lower().strip():
                    # Eliminamos la comprobación de ultima_generacion para semanal
                    fecha_apertura = timezone.now()
                    # Duración: 7 días abierto (cierre offset 6), entrega +5 días desde cierre
                    fecha_cierre = fecha_apertura + timedelta(days=6)
                    fecha_entrega = fecha_apertura + timedelta(days=11) # 6 (cierre) + 5 = 11
                    # Calcular fecha inicio pedidos (apertura + 2 días)
                    fecha_inicio_pedidos_calculada = fecha_apertura + timedelta(days=2)
                    PedidoColectivo.objects.create(
                        fecha_apertura=fecha_apertura,
                        fecha_inicio_pedidos=fecha_inicio_pedidos_calculada, # Añadido
                        fecha_cierre=fecha_cierre,
                        fecha_entrega=fecha_entrega,
                        tipo='semanal',
                        estado='abierto',
                        categoria=comanda.categoria,
                        proveedor=comanda.proveedor,
                        socio=comanda.socio_asignado,
                        comanda=comanda
                    )
                    self.stdout.write(f"Pedido semanal creado para comanda: {comanda.nombre}")
                    # Ya no actualizamos ultima_generacion aquí en el comando manual
                    # comanda.ultima_generacion = hoy
                    # comanda.save()

            elif comanda.frecuencia == 'quincenal':
                day_today_es = days_map[hoy.strftime('%A').lower()]
                self.stdout.write(
                    f"Comanda {comanda.nombre} (quincenal): dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
                )
                if day_today_es == (comanda.dia_semana or '').lower().strip():
                    # Eliminamos la comprobación de ultima_generacion para quincenal
                    fecha_apertura = timezone.now()
                    # Duración siempre semanal (7 días)
                    fecha_cierre = fecha_apertura + timedelta(days=6)
                    fecha_entrega = fecha_apertura + timedelta(days=11) # 6 (cierre) + 5 = 11
                    # Calcular fecha inicio pedidos (apertura + 2 días)
                    fecha_inicio_pedidos_calculada = fecha_apertura + timedelta(days=2)
                    PedidoColectivo.objects.create(
                        fecha_apertura=fecha_apertura,
                        fecha_inicio_pedidos=fecha_inicio_pedidos_calculada, # Añadido
                        fecha_cierre=fecha_cierre,
                        fecha_entrega=fecha_entrega,
                        tipo='quincenal',
                        estado='abierto',
                        categoria=comanda.categoria,
                        proveedor=comanda.proveedor,
                        socio=comanda.socio_asignado,
                        comanda=comanda
                    )
                    self.stdout.write(f"Pedido quincenal creado para comanda: {comanda.nombre}")
                    # Ya no actualizamos ultima_generacion aquí en el comando manual
                    # comanda.ultima_generacion = hoy
                    # comanda.save()

            elif comanda.frecuencia == 'mensual':
                day_today_es = days_map[hoy.strftime('%A').lower()]
                self.stdout.write(
                    f"Comanda {comanda.nombre} (mensual): dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
                )
                if day_today_es == (comanda.dia_semana or '').lower().strip():
                    # Eliminamos la comprobación de ultima_generacion para mensual
                    fecha_apertura = timezone.now()
                    # Duración siempre semanal (7 días)
                    fecha_cierre = fecha_apertura + timedelta(days=6)
                    fecha_entrega = fecha_apertura + timedelta(days=11) # 6 (cierre) + 5 = 11
                    # Calcular fecha inicio pedidos (apertura + 2 días)
                    fecha_inicio_pedidos_calculada = fecha_apertura + timedelta(days=2)
                    PedidoColectivo.objects.create(
                        fecha_apertura=fecha_apertura,
                        fecha_inicio_pedidos=fecha_inicio_pedidos_calculada, # Añadido
                        fecha_cierre=fecha_cierre,
                        fecha_entrega=fecha_entrega,
                        tipo='mensual',
                        estado='abierto',
                        categoria=comanda.categoria,
                        proveedor=comanda.proveedor,
                        socio=comanda.socio_asignado,
                        comanda=comanda
                    )
                    self.stdout.write(f"Pedido mensual (4 semanas) creado para comanda: {comanda.nombre}")
                    # Ya no actualizamos ultima_generacion aquí en el comando manual
                    # comanda.ultima_generacion = hoy
                    # comanda.save()

            elif comanda.frecuencia == 'esporadico':
                self.stdout.write(f"Comanda {comanda.nombre} (esporadico): Revisando si ya existe pedido.")
                # Genera el pedido esporádico solo si no existe ya uno ACTIVO ('abierto' o 'pendiente') para esta comanda
                if not PedidoColectivo.objects.filter(comanda=comanda, estado__in=['abierto', 'pendiente']).exists():
                    fecha_apertura = timezone.now()
                    # Duración: 7 días abierto (cierre offset 6), entrega +5 días desde cierre
                    fecha_cierre = fecha_apertura + timedelta(days=6)
                    fecha_entrega = fecha_apertura + timedelta(days=11) # 6 (cierre) + 5 = 11
                    # Calcular fecha inicio pedidos (apertura + 2 días)
                    fecha_inicio_pedidos_calculada = fecha_apertura + timedelta(days=2)
                    PedidoColectivo.objects.create(
                        fecha_apertura=fecha_apertura,
                        fecha_inicio_pedidos=fecha_inicio_pedidos_calculada, # Añadido
                        fecha_cierre=fecha_cierre,
                        fecha_entrega=fecha_entrega,
                        tipo='esporadico',
                        estado='abierto',
                        categoria=comanda.categoria,
                        proveedor=comanda.proveedor,
                        socio=comanda.socio_asignado,
                        comanda=comanda
                    )
                    self.stdout.write(f"Pedido esporádico creado para comanda: {comanda.nombre}")
                else:
                    self.stdout.write(f"Pedido esporádico para {comanda.nombre} ya existe, no se crea uno nuevo.")
                # Nota: No se actualiza ultima_generacion para esporádico

        self.stdout.write("=== [TEST] Proceso de generación completado ===")


# Comentarios del código original eliminados para brevedad