# Generated by Django 5.0.1 on 2024-05-14 06:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('info', models.CharField(max_length=2048, verbose_name='Информация')),
                ('region', models.CharField(default='none', max_length=128)),
                ('photo', models.CharField(blank=True, max_length=128)),
            ],
        ),
    ]
