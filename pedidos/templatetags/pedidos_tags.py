from django import template

register = template.Library()

@register.filter
def format_cantidad(cantidad, unidad_venta):
    """
    Formatea la cantidad según la unidad de venta.
    Si es 'ud', muestra como entero, si es 'kg' o 'g', muestra con decimales.
    """
    try:
        if unidad_venta == 'ud':
            return int(cantidad)
        else:  # 'kg' o 'g'
            return float(cantidad)
    except (ValueError, TypeError):
        return cantidad

@register.filter
def multiply(value, arg):
    """
    Multiplica el valor por el argumento.
    Útil para calcular subtotales (cantidad * precio).
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0