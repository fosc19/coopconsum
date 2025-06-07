from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica si un usuario pertenece a un grupo específico.
    Uso en plantilla: {% if request.user|has_group:"NombreDelGrupo" %}
    """
    # Asegurarse de que el usuario está autenticado antes de verificar grupos
    if not user.is_authenticated:
        return False
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        # Si el grupo no existe, el usuario no puede pertenecer a él
        return False
    except Exception:
        # Capturar otros posibles errores (ej. si user no tiene 'groups')
        return False