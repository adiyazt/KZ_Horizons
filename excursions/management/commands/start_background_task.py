
from django.core.management.base import BaseCommand
from excursions.tasks import check_for_expired_excursions
import threading

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        thread = threading.Thread(target=check_for_expired_excursions)
        thread.start()
        self.stdout.write(self.style.SUCCESS('Started background thread'))
