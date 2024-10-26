from django.apps import AppConfig
import os
from django.core.management import call_command


class ExcursionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'excursions'
    
    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            call_command('start_background_task')

