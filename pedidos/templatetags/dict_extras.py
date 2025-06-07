from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Devuelve el valor de un diccionario para una clave dada."""
    return dictionary.get(key)

@register.filter
def resta(value, arg):
    """Resta el argumento al valor."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

# Alias para compatibilidad con plantillas que usan dict_get
register.filter('dict_get', get_item)
