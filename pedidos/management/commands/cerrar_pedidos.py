from django.core.management.base import BaseCommand
from django.utils import timezone
from pedidos.models import PedidoColectivo

class Command(BaseCommand):
    help = 'Cierra (marca como pendientes) los pedidos colectivos cuya fecha de cierre ya ha pasado.'

    def handle(self, *args, **options):
        hoy = timezone.now()
        pedidos_a_cerrar = PedidoColectivo.objects.filter(
            estado='abierto',
            fecha_cierre__lt=hoy
        )
        cantidad = pedidos_a_cerrar.count()
        if cantidad:
            pedidos_a_cerrar.update(estado='pendiente')
            self.stdout.write(f"{cantidad} pedidos se han marcado como pendientes.")
        else:
            self.stdout.write("No hay pedidos para cambiar a estado pendiente.")
        self.stdout.write("=== Proceso de cierre completado ===")
