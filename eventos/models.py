from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _ # Importar gettext_lazy

class EventoCalendario(models.Model):
    titulo = models.CharField(_("Título"), max_length=200)
    descripcion = models.TextField(_("Descripción"), blank=True, null=True)
    fecha = models.DateTimeField(_("Fecha"))
    color = models.CharField(_("Color"), max_length=7, default='#007bff', help_text=_("Código hexadecimal del color (ej. #007bff)"))
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Creado por"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    compartir_api = models.BooleanField(
        _("Compartir a l'API"),
        default=False,
        help_text=_("Si està marcat, aquest event serà visible a l'API pública per altres cooperatives")
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = _("Evento de Calendario")
        verbose_name_plural = _("Eventos de Calendario")
        ordering = ['fecha']