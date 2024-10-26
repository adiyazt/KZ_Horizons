from django.urls import path
from .views import (
                    cities, city
                    )

urlpatterns = [
    path('cities/', cities, name='cities'),
    path('city/<str:city_id>/', city, name='city'),
]