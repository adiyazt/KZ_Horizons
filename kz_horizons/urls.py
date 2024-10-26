from django.contrib import admin
from django.urls import path, include
from excursions.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('users/', include('users.urls')),
    path('cities/', include('cities.urls')),
    path('excursions/', include('excursions.urls')),
    path('captcha/', include('captcha.urls')),
]