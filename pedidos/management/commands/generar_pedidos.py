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
    help = 'Genera pedidos colectivos a partir de comandas recurrentes, con quincenal cada 2 semanas y "mensual" cada 4 semanas.'

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        self.stdout.write(f"=== Revisando comandas para el día {hoy} ===")

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
                    # Restauramos la comprobación de ultima_generacion para semanal
                    if not comanda.ultima_generacion or (hoy - comanda.ultima_generacion).days >= 7:
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
                            fecha_entrega=fecha_entrega, # Actualizado
                            tipo='semanal',
                            estado='abierto',
                            categoria=comanda.categoria,
                            proveedor=comanda.proveedor,
                            socio=comanda.socio_asignado,
                            comanda=comanda
                        )
                        self.stdout.write(f"{comanda.categoria.nombre if comanda.categoria else 'Sin categoría'} - {comanda.proveedor.nombre if comanda.proveedor else 'Sin proveedor'} - {comanda.socio_asignado.__str__() if comanda.socio_asignado else 'Sin responsable'} (comanda {comanda.frecuencia})")
                        # Restauramos la actualización de ultima_generacion
                        comanda.ultima_generacion = hoy
                        comanda.save(update_fields=['ultima_generacion'])

            elif comanda.frecuencia == 'quincenal':
                day_today_es = days_map[hoy.strftime('%A').lower()]
                self.stdout.write(
                    f"Comanda {comanda.nombre} (quincenal): dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
                )
                if day_today_es == (comanda.dia_semana or '').lower().strip():
                    # Restauramos la comprobación de ultima_generacion para quincenal
                    if not comanda.ultima_generacion or (hoy - comanda.ultima_generacion).days >= 14:
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
                            fecha_entrega=fecha_entrega, # Actualizado
                            tipo='quincenal',
                            estado='abierto',
                            categoria=comanda.categoria,
                            proveedor=comanda.proveedor,
                            socio=comanda.socio_asignado,
                            comanda=comanda
                        )
                        self.stdout.write(f"{comanda.categoria.nombre if comanda.categoria else 'Sin categoría'} - {comanda.proveedor.nombre if comanda.proveedor else 'Sin proveedor'} - {comanda.socio_asignado.__str__() if comanda.socio_asignado else 'Sin responsable'} (comanda {comanda.frecuencia})")
                        # Restauramos la actualización de ultima_generacion
                        comanda.ultima_generacion = hoy
                        comanda.save(update_fields=['ultima_generacion'])

            elif comanda.frecuencia == 'mensual':
                day_today_es = days_map[hoy.strftime('%A').lower()]
                self.stdout.write(
                    f"Comanda {comanda.nombre} (mensual): dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
                )
                if day_today_es == (comanda.dia_semana or '').lower().strip():
                    # Restauramos la comprobación de ultima_generacion para mensual
                    if not comanda.ultima_generacion or (hoy - comanda.ultima_generacion).days >= 28:
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
                            fecha_entrega=fecha_entrega, # Actualizado
                            tipo='mensual',
                            estado='abierto',
                            categoria=comanda.categoria,
                            proveedor=comanda.proveedor,
                            socio=comanda.socio_asignado,
                            comanda=comanda
                        )
                        self.stdout.write(f"{comanda.categoria.nombre if comanda.categoria else 'Sin categoría'} - {comanda.proveedor.nombre if comanda.proveedor else 'Sin proveedor'} - {comanda.socio_asignado.__str__() if comanda.socio_asignado else 'Sin responsable'} (comanda {comanda.frecuencia})")
                        # Restauramos la actualización de ultima_generacion
                        comanda.ultima_generacion = hoy
                        comanda.save(update_fields=['ultima_generacion'])

            elif comanda.frecuencia == 'esporadico':
                self.stdout.write(f"Comanda {comanda.nombre} (esporadico): Revisando si ya existe pedido.")
                # Genera el pedido esporádico solo si no existe ya uno para esta comanda
                if not PedidoColectivo.objects.filter(comanda=comanda).exists():
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
                        fecha_entrega=fecha_entrega, # Actualizado
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

        self.stdout.write("=== Proceso de generación completado ===")


# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# from django.db.models import Q
# from pedidos.models import PedidoColectivo, ComandaRecurrente
#
# # Diccionario para mapear días de la semana de inglés a español.
# days_map = {
#     "monday": "lunes",
#     "tuesday": "martes",
#     "wednesday": "miercoles",
#     "thursday": "jueves",
#     "friday": "viernes",
#     "saturday": "sabado",
#     "sunday": "domingo"
# }
#
# class Command(BaseCommand):
#     help = 'Genera pedidos colectivos a partir de comandas recurrentes.'
#
#     def handle(self, *args, **options):
#         hoy = timezone.now().date()
#         self.stdout.write(f"Revisando comandas para el día {hoy}...")
#
#         # Generar pedidos para las comandas activas y vigentes.
#         comandas = ComandaRecurrente.objects.filter(
#             estado='activa',
#             fecha_inicio__lte=hoy
#         ).filter(
#             Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=hoy)
#         )
#
#         for comanda in comandas:
#             if comanda.frecuencia == 'semanal':
#                 day_today_es = days_map[hoy.strftime('%A').lower()]
#                 self.stdout.write(
#                     f"Comanda {comanda.nombre}: dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
#                 )
#                 if day_today_es == (comanda.dia_semana or '').lower().strip():
#                     fecha_apertura = timezone.now()
#                     fecha_cierre = fecha_apertura + timedelta(days=7)
#                     fecha_entrega = fecha_cierre + timedelta(days=3)
#                     PedidoColectivo.objects.create(
#                         fecha_apertura=fecha_apertura,
#                         fecha_cierre=fecha_cierre,
#                         fecha_entrega=fecha_entrega,
#                         tipo='semanal',
#                         estado='abierto',
#                         categoria=comanda.categoria,
#                         proveedor=comanda.proveedor
#                     )
#                     self.stdout.write(f"Pedido semanal creado para comanda: {comanda.nombre}")
#                     comanda.ultima_generacion = hoy
#                     comanda.save()
#
#             elif comanda.frecuencia == 'mensual':
#                 if comanda.dia_mes and hoy.day == comanda.dia_mes:
#                     fecha_apertura = timezone.now()
#                     fecha_cierre = fecha_apertura + timedelta(days=7)
#                     fecha_entrega = fecha_cierre + timedelta(days=3)
#                     PedidoColectivo.objects.create(
#                         fecha_apertura=fecha_apertura,
#                         fecha_cierre=fecha_cierre,
#                         fecha_entrega=fecha_entrega,
#                         tipo='mensual',
#                         estado='abierto',
#                         categoria=comanda.categoria,
#                         proveedor=comanda.proveedor
#                     )
#                     self.stdout.write(f"Pedido mensual creado para comanda: {comanda.nombre}")
#                     comanda.ultima_generacion = hoy
#                     comanda.save()
#
#             elif comanda.frecuencia == 'quincenal':
#                 day_today_es = days_map[hoy.strftime('%A').lower()]
#                 self.stdout.write(
#                     f"Comanda {comanda.nombre}: dia_semana configurado = {comanda.dia_semana.lower().strip()}, día actual = {day_today_es}"
#                 )
#                 if day_today_es == (comanda.dia_semana or '').lower().strip():
#                     if not comanda.ultima_generacion or (hoy - comanda.ultima_generacion).days >= 14:
#                         fecha_apertura = timezone.now()
#                         fecha_cierre = fecha_apertura + timedelta(days=7)
#                         fecha_entrega = fecha_cierre + timedelta(days=3)
#                         PedidoColectivo.objects.create(
#                             fecha_apertura=fecha_apertura,
#                             fecha_cierre=fecha_cierre,
#                             fecha_entrega=fecha_entrega,
#                             tipo='quincenal',
#                             estado='abierto',
#                             categoria=comanda.categoria,
#                             proveedor=comanda.proveedor
#                         )
#                         self.stdout.write(f"Pedido quincenal creado para comanda: {comanda.nombre}")
#                         comanda.ultima_generacion = hoy
#                         comanda.save()
#
#         self.stdout.write("Proceso de generación completado.")
