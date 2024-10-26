# tasks.py
import threading
import time
from django.utils import timezone
from .models import Excursion 
from django.core.management.base import BaseCommand
from users.models import Update, Booking

def check_for_expired_excursions():
    while True:
        now = timezone.now()
        excursions = Excursion.objects.filter(datetime__lt=now, is_past=False) 
        print(excursions)
        for excursion in excursions:
            excursion.is_past = True
            update = Update(excursion=excursion.id, 
                                header='С возвращением с экскурсии!',
                                text='Оцените гида и напишите отзыв, чтобы мы могли улучшить наши услуги.',
                                is_review=True)
            update.save()
            excursion.save()
            bookings = Booking.objects.filter(excursion=excursion.id)
            for booking in bookings:
                booking.is_past=True
                booking.save()
        time.sleep(3600) 
        
