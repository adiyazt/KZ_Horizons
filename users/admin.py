from django.contrib import admin
from .models import User, Booking, Update


admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Update)
