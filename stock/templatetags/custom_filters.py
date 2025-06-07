# stock/templatetags/custom_filters.py
import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='parse_json')
def parse_json(value):
    """
    Intenta parsear una cadena JSON a un objeto Python (lista/diccionario).
    Devuelve None si falla el parseo o el tipo no es string.
    """
    if not isinstance(value, str):
        # Si ya es un objeto Python (p.ej., JSONField lo deserializó), devolverlo
        if isinstance(value, (list, dict)):
            return value
        print(f"WARN: parse_json recibió un tipo no esperado: {type(value)}")
        return None # O devolver [], o loggear error si no es string ni objeto esperado
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        print(f"Error parsing JSON in template filter: {value}") # Log para depuración
        return None # O devolver []