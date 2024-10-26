from django.db import models
import uuid
from users.models import User, Booking
from cities.models import City
from datetime import datetime
from django.utils import timezone



class CheckTimestamp(models.Model):
    last_checked = models.DateTimeField(default=timezone.now)
    
 
class Attraction(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    name = models.CharField(
        default='Attraction', max_length=32, blank=True
    )
    info = models.CharField(
        max_length=2048, verbose_name='Информация', blank=False
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='City',
    )
    photo = models.CharField(
        max_length=128, default='img/images/no-photo.jpg'
    )
    
    
exc_types = (
    ('1', 'Индивидуальная'),
    ('2', 'Групповая'),
)

exc_kinds = (
    ('1', 'Культурно-познавательная'),
    ('2', 'Лечевно-оздоровительная'),
    ('3', 'Спортивная и экстремальная'),
    ('4', 'Религиозная'),
    ('5', 'Природно-заповедные места'),
    ('6', 'Экотуризм')
)

transport = (
    ('1', 'Пешком'),
    ('2', 'Машина'),
    ('3', 'Автобус')
)
    
class Excursion(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    name = models.CharField(
        default='Excursion', max_length=32, blank=False
    )
    info = models.CharField(
        max_length=2048, verbose_name='Информация', blank=False
    )
    type = models.CharField(
        max_length=32, blank=False, default=exc_types[1], verbose_name='Тип экскурсии'
    )
    kind = models.CharField(
        max_length=32, blank=False, default=exc_kinds[1], verbose_name='Тип экскурсии'
    )
    people_number = models.IntegerField(
        blank=True
    )
    time = models.IntegerField(
        verbose_name='Duration', blank=False
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE
    )
    guide = models.CharField(
        max_length=64
    )
    transport = models.CharField(
        max_length=32, choices=transport, blank=False, default=transport[2], verbose_name='Транспорт'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    program = models.CharField(
        max_length=512, verbose_name='Программа', blank=False
    )
    attractions = models.ManyToManyField(
        Attraction
    )
    photo = models.CharField(
        max_length=128, default='img/images/no-photo.jpg'
    )
    datetime = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True
    )
    created = models.DateTimeField(
        auto_now=False, auto_now_add=True,
    )
    clients_count = models.IntegerField(
        default=0
    )
    is_available = models.BooleanField(
        default=True
    )
    is_past = models.BooleanField(
        default=False
    )
    
 