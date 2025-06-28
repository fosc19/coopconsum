from django.contrib import admin
from .models import Socio, CuentaSocio, MovimientoCuenta # Quitar RegistroCompraSocio

# Custom Admin for Socio
class SocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'user', 'gestiona_stock', 'gestiona_productos', 'puede_crear_comandas_esporadicas')
    list_filter = ('gestiona_stock', 'gestiona_productos', 'puede_crear_comandas_esporadicas')
    search_fields = ('nombre', 'apellido', 'email', 'user__username') # Campos de búsqueda
    # Opcional: Definir los campos en el formulario de edición
    fieldsets = (
        (None, {
            'fields': ('user', 'nombre', 'apellido', 'email', 'telefono', 'direccion')
        }),
        ('Permisos', { # Agrupar los campos de permiso
            'fields': ('gestiona_stock', 'gestiona_productos', 'puede_crear_comandas_esporadicas'),
        }),
    )
    # Si prefieres una lista simple de campos en lugar de fieldsets:
    # fields = ('user', 'nombre', 'apellido', 'email', 'telefono', 'direccion', 'gestiona_stock')

admin.site.register(Socio, SocioAdmin) # Registrar Socio con la clase personalizada

@admin.register(CuentaSocio)
class CuentaSocioAdmin(admin.ModelAdmin):
    list_display = ('socio', 'get_saldo_calculado_dinamicamente') # Mostrar solo el calculado
    readonly_fields = ('get_saldo_calculado_dinamicamente', 'saldo_actual') # Hacer saldo_actual readonly en el form de detalle
    fields = ('socio', 'get_saldo_calculado_dinamicamente', 'saldo_actual') # Orden en el form de detalle

    def get_saldo_calculado_dinamicamente(self, obj):
        # obj es una instancia de CuentaSocio
        from django.db.models import Sum
        saldo = MovimientoCuenta.objects.filter(
            cuenta=obj,
            estado="validado"
        ).aggregate(total_sum=Sum('monto'))['total_sum'] or 0
        return saldo
    get_saldo_calculado_dinamicamente.short_description = 'Saldo (€)' # Renombrar para la lista

@admin.register(MovimientoCuenta)
class MovimientoCuentaAdmin(admin.ModelAdmin):
    list_display = ('get_descripcion_movimiento', 'cuenta', 'fecha', 'get_tipo_movimiento_display', 'monto', 'estado', 'descripcion')
    list_filter = ('estado', 'tipo_movimiento', 'fecha', 'cuenta__socio')
    search_fields = ('cuenta__socio__nombre', 'cuenta__socio__apellido', 'descripcion', 'tipo_movimiento')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)
    
    def get_tipo_movimiento_display(self, obj):
        """Tradueix 'egreso' per 'compra' per a la visualització"""
        if obj.tipo_movimiento == "egreso":
            return "compra"
        return obj.tipo_movimiento
    get_tipo_movimiento_display.short_description = 'Tipo Movimiento'
    
    def get_descripcion_movimiento(self, obj):
        """Personalitza la descripció del moviment traduint 'egreso' per 'compra'"""
        tipo_display = "compra" if obj.tipo_movimiento == "egreso" else obj.tipo_movimiento
        return f"{tipo_display} - {obj.monto} en {obj.fecha}"
    get_descripcion_movimiento.short_description = 'Movimiento de Cuenta'


