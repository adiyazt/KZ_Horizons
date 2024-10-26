from django.shortcuts import render
from .models import City
from excursions.models import Excursion, Attraction
from excursions.views import Booking, User

def cities(request):
    auth = True if request.session.get('is_authorized') else False
    try:
        cities = City.objects.all()
        context = {
            'cities' : cities,
            'auth' : auth
        }
        return render(request, 'cities.html', context)
    except Exception as e:
        print(e)
        
        
def city(request, city_id=None):
    auth = True if request.session.get('is_authorized') else False
    if city_id:
        city = City.objects.get(id=city_id)    
        excursions = Excursion.objects.filter(city=city, is_available=True, is_past=False)
        excs = []
        for exc in excursions:
            excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
        
        context = {
            'city' : city,
            'attractions' : Attraction.objects.filter(city=city),
            'excursions' : excs,
            'auth' : auth
        }
        return render(request, 'city.html', context)
