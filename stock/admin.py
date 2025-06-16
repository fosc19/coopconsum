from django.contrib import admin
from .models import StockLocal, MovimientoStock, RegistroCompraStockProxy # Importar el Proxy
# Ya no necesitamos importar RegistroCompraSocio directamente aquí para el admin
# from socios.models import RegistroCompraSocio

admin.site.register(StockLocal)
admin.site.register(MovimientoStock)

# Custom Admin for RegistroCompraStockProxy
@admin.register(RegistroCompraStockProxy) # Registrar el PROXY
class RegistroCompraStockProxyAdmin(admin.ModelAdmin): # Cambiar nombre de la clase Admin
    list_display = ('fecha_registro', 'socio', 'producto', 'cantidad', 'estado', 'costo_total_calculado', 'registrado_por', 'movimiento_cuenta_link')
    list_filter = ('estado', 'socio', 'producto', 'fecha_registro')
    search_fields = ('socio__nombre', 'socio__apellido', 'producto__nombre', 'notas')
    list_per_page = 25
    date_hierarchy = 'fecha_registro'

    readonly_fields = ('fecha_registro', 'costo_total_calculado', 'movimiento_cuenta', 'registrado_por')

    def movimiento_cuenta_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        if obj.movimiento_cuenta:
            # Ajustar el namespace del reverse a 'admin:socios_movimientocuenta_change'
            # ya que el modelo MovimientoCuenta sigue en la app 'socios'
            link = reverse("admin:socios_movimientocuenta_change", args=[obj.movimiento_cuenta.id])
            return format_html('<a href="{}">Mov. #{}</a>', link, obj.movimiento_cuenta.id)
        return "-"
    movimiento_cuenta_link.short_description = 'Moviment Compte'

    def has_add_permission(self, request):
        return False

    # El verbose_name ya está definido en el Meta del proxy model.
    # No es necesario get_model_perms aquí para cambiar el nombre.

