from django.urls import path
from . import views

urlpatterns = [
    path('validar_propuesta/<int:propuesta_id>/', views.validar_propuesta_correccion, name='validar_propuesta_correccion'),
    path('seleccionar/<int:pedido_id>/', views.seleccionar_pedido, name='seleccionar_pedido'),
    path('pedidos_abiertos/', views.pedidos_abiertos, name='pedidos_abiertos'),
    path('panel_principal/', views.panel_principal, name='panel_principal'),
    path('gestionar_comanda/<int:comanda_id>/', views.gestionar_comanda, name='gestionar_comanda'),
    path('gestionar_pedidos_esporadicos/', views.gestionar_pedidos_esporadicos, name='gestionar_pedidos_esporadicos'),
    path('seleccionar_comanda/', views.seleccionar_comanda, name='seleccionar_comanda'),

    # URLs para la funcionalidad de "Desitjos"
    path('desitjos/', views.listar_cartas_deseo_view, name='listar_cartas_deseo'),
    path('desitjos/carta/<int:carta_id>/', views.detalle_carta_deseo_view, name='detalle_carta_deseo'),
    path('desitjos/registrar_interes/<int:carta_id>/', views.registrar_interes_en_carta_view, name='registrar_interes_en_carta'),
    path('desitjos/gestio/', views.panel_gestio_desitjos_view, name='panel_gestio_desitjos'),
    
    # Nueva URL para la vista Master Control
    path('master/', views.master_control_view, name='master_control'),
    # Nueva URL para la API de resumen por socio
    path('api/resumen_socios/<int:pedido_id>/', views.api_resumen_pedido_socios, name='api_resumen_pedido_socios'),
    # Nueva URL para guardar anotaciones de stock
    path('master/guardar_anotacion/', views.guardar_anotacion_stock, name='guardar_anotacion_stock'),
    # Nueva URL para corregir cantidades de socios en la comanda
    path('corregir_cantidades_socios/<int:comanda_id>/', views.corregir_cantidades_socios, name='corregir_cantidades_socios'),
    # Notificación de recepción de productos por el master
    path('notificar_recepcion_comanda/<int:pedido_id>/', views.notificar_recepcion_comanda, name='notificar_recepcion_comanda'),
    # Nueva URL para finalizar comanda y descontar monederos
    path('finalizar_comanda/<int:comanda_id>/', views.finalizar_comanda, name='finalizar_comanda'),
    # Nueva URL para guardar cambios sin finalizar (solo si está pendiente)
    path('guardar_cambios_pendiente/<int:comanda_id>/', views.guardar_cambios_comanda_pendiente, name='guardar_cambios_comanda_pendiente'),
    # Nueva URL para la vista de historial de pedidos del socio
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    # Nueva URL para que los socios creen comandas esporádicas
    path('comandas/crear_esporadica/', views.crear_comanda_esporadica_socio, name='crear_comanda_esporadica_socio'),
]
