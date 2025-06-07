from django.http import JsonResponse
from .models import EventoCalendario
from django.utils import timezone

def api_eventos_calendario(request):
    """
    Vista API para devolver eventos de calendario en formato JSON.
    """
    # Obtener eventos (puedes filtrar por rango de fechas si es necesario)
    eventos = EventoCalendario.objects.all()

    # Formatear eventos para FullCalendar (u otra librería)
    eventos_data = []
    for evento in eventos:
        eventos_data.append({
            'title': evento.titulo,
            'start': evento.fecha.isoformat(), # Formato ISO 8601
            'description': evento.descripcion,
            'color': evento.color,
            # Puedes añadir más campos si tu modelo o librería de calendario los soporta
        })

    return JsonResponse(eventos_data, safe=False)