from django.contrib import admin
from django.urls import path
from .views import (
                    add_excursion, excursion, book, download_booking,
                    excursions, attractions, attraction, choose_attrs
                    )

urlpatterns = [
    path('add_excursion/', add_excursion, name='add_excursion'),
    path('excursion/<str:excursion_id>/', excursion, name='excursion'),
    path('book/<str:excursion_id>/', book, name='book'),
    path('download_booking/<str:excursion_id>/', download_booking, name='download_booking'),
    path('excursions/', excursions, name='excursions'),
    path('attractions/', attractions, name='attractions'),
    path('attraction/<str:attraction_id>/', attraction, name='attraction'),
    path('choose_attrs/<str:excursion_id>/', choose_attrs, name='choose_attrs'),
    
]