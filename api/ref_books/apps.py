from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DirectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ref_books'
    verbose_name = _('Справочники')
