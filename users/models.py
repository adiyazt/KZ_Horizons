from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django import forms
from captcha.fields import CaptchaField
from datetime import datetime

EMAILS = ('gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'hotmail.co.uk', 'hotmail.fr', 
          'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 'comcast.net', 'yahoo.co.uk', 
          'yahoo.com.br', 'yahoo.co.in', 'live.com', 'rediffmail.com', 'free.fr', 'gmx.de', 
          'web.de', 'yandex.ru', 'ymail.com', 'libero.it', 'outlook.com', 'uol.com.br', 
          'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 'sbcglobal.net', 'sfr.fr', 
          'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 'yahoo.es', 'ig.com.br', 
          'live.nl', 'bigpond.com', 'terra.com.br', 'yahoo.it', 'neuf.fr', 'yahoo.de', 
          'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 'facebook.com', 'bellsouth.net', 
          'yahoo.in', 'hotmail.es')

class MailExistsValidation:
    def __init__(self):
        self.mails: tuple = EMAILS

    def __call__(self, context: str):
        is_email = False
        for mail in self.mails:
            if mail not in context:
                is_email = True
        if not is_email:
            raise ValidationError(
                    '''
                    Введите настоящую почту.
                    ''',
                    code='mail_exception',
                    params={'mails': self.mails, 'current_mail': mail}
                )

class NumberValidation:
    def __init__(self):
        self.fixed=11

    def __call__(self, context: str):
        if len(context)!=self.fixed:
            raise ValidationError(
                '''
                It should be 11 numbers and start with 8.
                ''',
                code='phone_exception',
                params={'current': context}
            )

class User(models.Model):
    def check_num(self):
        if self.phone[0] == '8':
            self.phone = self.phone.replace('8', '+7', 1)
        
    def save(self, *args, **kwargs):
        self.check_num()
        super().save(*args, **kwargs)
    
    def number_validation(stroke: str):
        return NumberValidation()(context=stroke)
    
    def mail_validation(stroke: str):
        return MailExistsValidation()(context=stroke)

    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    photo = models.CharField(
        max_length=128, default='img/images/no-photo.jpg'
    )
    email = models.CharField(
        max_length=50, db_index=True, verbose_name='Email', blank=False, validators=[mail_validation]
    )
    password = models.CharField(
        max_length=32, db_index=True, verbose_name='Пароль', blank=False
    )
    phone = models.CharField(
        max_length=12, verbose_name='Номер телефона', blank=False, validators=[number_validation]
    )
    full_name = models.CharField(
        max_length=64, verbose_name='Имя Фамилия', blank=False
    )
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, verbose_name='Рейтинг', blank=True, default=0
    )
    rating_number = models.IntegerField(
        null=True, verbose_name='Кол-ва рейтингов', blank=True, default=0
    )
    info = models.CharField(
        max_length=512, verbose_name='Информация о себе', null=True, blank=True
    )
    status = models.CharField(
        max_length=32, blank=False, default='guide', verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email',]
        
        
class Captcha(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )

class CaptchaForm(forms.ModelForm):
    captcha = CaptchaField(
        label='Введите текст нарисованный на картинке',
        error_messages={'invalid': 'Неправильный текст'}

    )
    class Meta:
        model = Captcha
        fields = ('captcha',)
        

   
class Booking(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    excursion = models.CharField(
        max_length=64, blank=False
    )
    is_past = models.BooleanField(
        default=False
    )
    
   
    
    
class Update(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    excursion = models.CharField(
        max_length=64, blank=False
    )
    header = models.CharField(
        max_length=32, blank=False
    )
    text = models.TextField(
        max_length=512, blank=False
    )
    datetime = models.DateTimeField(
        default=datetime.now()
    )
    is_review = models.BooleanField(
        default=False
    )
    
 
class Review(models.Model):
    id = models.CharField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID', max_length=128
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    object_id = models.CharField(
        max_length=64, blank=False
    )
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, verbose_name='Рейтинг', blank=True
    )
    text = models.TextField(
        max_length=512, blank=False
    )
    datetime = models.DateTimeField(
        default=datetime.now()
    )