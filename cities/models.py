from django.db import models
import uuid

   
class City(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    name = models.CharField(
        max_length=32, blank=False
    )
    info = models.CharField(
        max_length=2048, verbose_name='Информация', blank=False
    )
    region = models.CharField(
        max_length=128, blank=False, default='none'
    )
    photo = models.CharField(
        max_length=128, blank=True
    )
