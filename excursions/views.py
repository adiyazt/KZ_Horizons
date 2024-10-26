from django.shortcuts import render, redirect
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound, 
    HttpResponseBadRequest, HttpResponseNotAllowed, FileResponse
)
from excursions.models import (
                                Excursion, Attraction,
                                exc_kinds, exc_types, transport, User, Booking
                            )
from cities.models import City
from .utils import upload_photo, get_type, get_kind, get_transport
from datetime import datetime             
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from django.conf import settings
import os

TRANSPORT = ['Пешком', 'Машина', 'Автобус']


    
def index(request):
    auth = True if request.session.get('is_authorized') else False
    cities = City.objects.all()
    popular_cities = cities[:3]
    attractions = Attraction.objects.all()
    excursions = Excursion.objects.filter(is_past=False, is_available=True)
    excs = []
    for exc in excursions:
        excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
    print(excs)
        
    context = {
        'auth' : auth,
        'cities' : City.objects.all(),
        'exc_kinds' : exc_kinds,
        'exc_types' : exc_types,
        'populars' : [popular_cities, attractions, excs]
    }
    return render(request, 'index.html', context)

    
def add_excursion(request):
    auth = True if request.session.get('is_authorized') else False
    if not request.POST:
        session = request.session
        if session.get('is_authorized') and session.get('status') == 'guide':
            global transport, exc_kinds, exc_types
            context = {
                'user' : User.objects.get(pk=session.get('user_id')),
                'exc_kinds' : exc_kinds,
                'exc_types' : exc_types,
                'transport' : transport,
                'attractions' : Attraction.objects.all(),
                'cities' : City.objects.all(),
                'guide_id' : request.session.get('user_id'),
                'auth' : auth
            }
            print(request.session.get('user_id'))
            return render(request, 'add_excursion.html', context)
        else:
            return HttpResponseNotAllowed('You are not a guide')
    
    else:
        data = request.POST
        name = data.get('name')
        info = data.get('info')
        kind = data.get('kind')
        type = data.get('type')
        people_number = data.get('people_number')
        time = data.get('time')
        city = data.get('city')
        transport = data.get('transport')
        price = data.get('price')
        date = data.get('date')
        program = data.get('program')
        guide = data.get('guide')
        print(guide, 111)
        photo = request.FILES['photo']
        
        excursion: Excursion = Excursion(
            name=name, info=info, kind=kind, type=type, people_number=people_number,
            time=time, city=City.objects.get(id=city), guide=guide, transport=transport,
            price=price, program=program, datetime=date
        )
        excursion.save()
        print(date)
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        print(date, datetime.now())
        if date < datetime.now():
            return HttpResponseBadRequest()
        excursion.save()
        excursion.photo = upload_photo(photo=photo, id=excursion.id)
        excursion.save()
        
        return redirect('choose_attrs', excursion.id)
    

def choose_attrs(request, excursion_id=None):
    if request.POST:
        excursion_id = request.POST.get('excursion_id')
        attractions = request.POST.get('attractions')
        print(excursion_id, attractions)
        attractions = attractions.split(',')
        attractions.pop()
        print(attractions)
        excursion = Excursion.objects.get(id=excursion_id)
        for attr in attractions:
            print(attr)
            attraction = Attraction.objects.get(id=attr)
            print(attraction)
        excursion.save()
        return redirect('profile')
    if excursion_id:
        try:
            excursion = Excursion.objects.get(id=excursion_id)
            attractions = Attraction.objects.filter(city=excursion.city)
            context = {'attractions': attractions, 'excursion_id': excursion_id}
            return render(request, 'choose_attrs.html', context=context)
        except Exception as e:
            return HttpResponse(e)
  
  
def excursion(request, excursion_id=None):
    if excursion_id:
        if Excursion.objects.filter(id=excursion_id)[0]:
            excursion = Excursion.objects.get(id=excursion_id)
            guide = User.objects.get(id=excursion.guide)
            attractions = excursion.attractions.all()
            auth = True if request.session.get('is_authorized') else False
            context = {
                'excursion' : excursion,
                'guide' : guide,
                'attractions' : attractions,
                'auth' : auth
            }
            
            if request.session.get('user_id'):
                
                user = User.objects.get(pk=request.session.get('user_id'))
                if guide.id==user.id:
                    context.update({
                        'is_guide' : True,
                        'bookings' : Booking.objects.filter(excursion=excursion_id)
                    })
            
            return render(request, 'excursion.html', context)
    return HttpResponse(123)


def book(request, excursion_id=None):
    if excursion_id:
        user = User.objects.get(id=request.session.get('user_id'))
        print(user.status)
        if Excursion.objects.filter(id=excursion_id)[0] and user.status=='client':
            excursion = Excursion.objects.get(id=excursion_id)
            booking = Booking(excursion=excursion_id, user=user)
            excursion.clients_count = excursion.clients_count+1
            if excursion.clients_count==excursion.people_number:
                excursion.is_available = False
            excursion.save()
            booking.save()
            return redirect('profile')


def download_booking(request, excursion_id=None):
    if excursion_id:
        if Excursion.objects.filter(id=excursion_id).exists():
            user = User.objects.get(pk=request.session.get('user_id'))
            if Booking.objects.filter(excursion=excursion_id, user=user).exists():
                excursion = Excursion.objects.get(id=excursion_id)

                excursion_info = [
                    f"Excursion Name: {excursion.name}",
                    f"City: {excursion.city.name}",
                    f"Type: {excursion.type}",
                    f"Kind: {excursion.kind}",
                    f"People Number: {excursion.people_number}",
                    f"Duration: {excursion.time} hours",
                    f"Guide: {User.objects.get(pk=excursion.guide).full_name}",
                    f"Transport: {TRANSPORT[int(excursion.transport)-1]}",
                    f"Price: {excursion.price} euro",
                    f"Program: {excursion.program}",
                    f"Attractions: {', '.join(str(attraction.name) for attraction in excursion.attractions.all())}",
                    f"Date: {excursion.datetime}"
                ]

                user_info = [
                    f"Email: {user.email}",
                    f"Phone: {user.phone}"
                ]

                buffer = BytesIO()

                p = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter

                font_path = os.path.join(settings.BASE_DIR, 'users', 'static', 'fonts', 'Arial.ttf')
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                p.setFont("Arial", 12)

                p.drawString(100, height - 50, "-----------User----------")
                y = height - 70
                for line in user_info:
                    p.drawString(100, y, line)
                    y -= 20

                p.drawString(100, y - 10, "---------Excursion--------")
                y -= 30
                for line in excursion_info:
                    p.drawString(100, y, line)
                    y -= 20

                p.showPage()
                p.save()

                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename='excursion_info.pdf')

    return HttpResponse("Excursion not found.", status=404)



def excursions(request):
    auth = True if request.session.get('is_authorized') else False
    context = {
        'cities' : City.objects.all(),
        'auth' : auth,
        'exc_kinds' : exc_kinds,
        'exc_types' : exc_types,
    }
    if request.method == 'POST':
        exc_type = request.POST.get('exc_type')
        print(exc_type)
        exc_kind = request.POST.get('exc_kind')
        city = request.POST.get('city')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        excursions = Excursion.objects.filter(kind=exc_kind, type=exc_type, city=City.objects.get(id=city), is_past=False, is_available=True)
        exs = Excursion.objects.all()
        print(exs)
        print(exs[0].type, exs[0].kind, exs[0].city)
        print(excursions)
        excs = []
        for exc in excursions:
            print(exc.datetime, date_from, date_to)
            if exc.datetime and exc.type==exc_type and exc.kind==exc_kind and exc.city.pk==city and date_from <= exc.datetime.date() <= date_to:
                excs.append(exc)
        
        excursions = []
        for exc in excs:
            excursions.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
        context.update({
            'excursions' : excursions
        })
        print(excs)
    else:
        excursions = Excursion.objects.filter(is_available=True, is_past=False)
        excs = []
        for exc in excursions:
            excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
        context.update({
            'excursions' : excs,
        })
    return render(request, 'excursions.html', context)


def attractions(request):
    context = {
        'cities' : City.objects.all(),
        'attractions' : Attraction.objects.all()
    }
    if request.POST:
        city_id = request.POST.get('city')
        city = City.objects.get(id=city_id)
        attractions = Attraction.objects.filter(city=city)
        context.update({
            'attractions' : attractions
        })
    return render(request, 'attractions.html', context)


def attraction(request, attraction_id=None):
    if attraction_id:
        attraction = Attraction.objects.get(id=attraction_id)
        excursions = Excursion.objects.filter(attractions=attraction, is_available=True, is_past=False)
        excs = []
        for exc in excursions:
            excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
        
        context = {
            'attraction' : attraction,
            'excursions' : excs
        }
        return render(request, 'attraction.html', context)
        
 
 
