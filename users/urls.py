from django.contrib import admin
from django.urls import path
from .views import (register, login, api_auth, 
                    api_reg, deauth, cap, get_code,
                    profile, send_update, updates, review,
                    guides, guide
                    )

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('deauth/', deauth, name='deauth'),
    path('api/v1/authorization', api_auth, name='api_login'),
    path('api/v1/registration', api_reg, name='api_register'),
    path('deauth/', deauth, name='deauth'),
    path('login_captcha/', cap, name='login_captcha'),
    path('get_code/', get_code, name='get_code'),
    path('profile/', profile, name='profile'),
    path('send_update/<str:excursion_id>/', send_update, name='send_update'),
    path('review/<str:excursion_id>/', review, name='review'),
    path('updates/', updates, name='updates'),
    path('guides/', guides, name='guides'),
    path('guide/<str:guide_id>/', guide, name='guide'),
]
