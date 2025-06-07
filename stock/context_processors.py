from socios.models import RegistroCompraSocio

def registros_compra_pendientes_processor(request):
    """
    Añade el número de registros de compra manual pendientes de validación al contexto.
    """
    count = 0
    try:
        # Contar todos los registros de compra con estado 'pendiente'
        count = RegistroCompraSocio.objects.filter(estado='pendiente').count()
    except Exception:
        # En caso de cualquier error, simplemente dejamos count en 0.
        pass
    return {'registros_compra_pendientes_count': count}