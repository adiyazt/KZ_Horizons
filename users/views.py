from django.shortcuts import render, redirect
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound, 
    HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
)
from users.models import User, CaptchaForm, Booking, Update, Review
from .utils import send_confirmation_code
import json
from excursions.models import Excursion, Attraction


def register(request):
    
    template = 'register.html'
    if request.session.get('is_authorized'):
        return redirect('index')
    if not request.session.get('captcha'):
        return redirect('login_captcha')
    return render(request, template)


def login(request):
    template = 'login.html'
    if request.session.get('is_authorized'):
        return redirect('index')
    if not request.session.get('captcha'):
        return redirect('login_captcha')
    return render(request, template)


def deauth(request):
    if request.session.get('is_authorized'):
        request.session.clear()
    return redirect('index')


def api_auth(request):
    email   : str = request.POST.get('email')
    password: str = request.POST.get('password')

    print(f'{email=} {password=}')

    if email and password:
        if User.objects.filter(email=email, password=password).exists():
            user = User.objects.get(email=email, password=password)
            request.session['is_authorized'] = True
            request.session['email'] = user.email
            request.session['user_id'] = str(user.pk)
            request.session['status'] = user.status
            print(f'{user.pk=}')
            return redirect('index')
        else:
            return HttpResponseBadRequest('User does not exist')
    return HttpResponseBadRequest('Invalid data')


def api_reg(request):
    name: str = request.POST.get('name')
    phone   : str = request.POST.get('phone')
    email   : str = request.POST.get('email')
    password: str = request.POST.get('password')
    status  : str = request.POST.get('status')
    cpassword   : str = request.POST.get('cpassword')

    if name and email and password and phone and cpassword:
        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest('User exists')
        if password != cpassword:
            return HttpResponseBadRequest('Passwords do not match')

        user: User = User()
        user.email = email
        user.full_name = name
        user.password = password
        user.phone = phone
        user.status = status
        user.save()

        request.session['is_authorized'] = True
        request.session['email'] = user.email
        request.session['user_id'] = str(user.pk)
        request.session['status'] = user.status

        return redirect('index')
    return HttpResponse('Invalid data', status=403)
        
    
   
def cap(request):
    print(000000000000)
    print(request.POST)
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            request.session['captcha'] = True
            return redirect('login')
    form = CaptchaForm()
    context = {
        'form': form
    }
    return render(request, 'captcha.html', context)


def get_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        send_confirmation_code(chat_id)
        response = {'message': 'Code sent to Telegram bot successfully'}
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def profile(request):
        
    if request.method == 'POST':
        full_name : str = request.POST.get('full_name')
        phone     : str = request.POST.get('phone')
        email     : str = request.POST.get('email')
        info      : str = request.POST.get('info')
        print(full_name, info, phone, email)
        user = User.objects.get(pk=request.session.get('user_id'))
        user.full_name = full_name if user.full_name!=full_name else user.full_name
        user.phone = phone if user.phone!=phone else user.phone
        user.email = email if user.email!=email else user.email
        user.info = info if user.info!=info else user.info
        user.save()
        if request.FILES['photo']:
            id = user.id
            photo = request.FILES['photo']
            _filename = str(photo)
            if _filename.split('.')[-1] in ('jpg', 'png', 'jpeg'):
                short = f'img/images/users/{id}.{_filename.split(".")[-1]}'
                _path = f'users/static/{short}'

                with open(_path, 'wb+') as _file:
                    for chunk in photo.chunks():
                        _file.write(chunk)
                user.photo = short
                user.save()
            else:
                return HttpResponse('Wrong format')
        
    print(request.session.get('status'))
    
    if request.session.get('is_authorized'):
        client = True if request.session.get('status')=='client' else False
        user = User.objects.get(pk=request.session.get('user_id'))
        context = {
            'email' : user.email,
            'phone' : user.phone,
            'full_name' : user.full_name,
            'rating' : user.rating,
            'rating_number' : user.rating_number,
            'info' : user.info,
            'client' : client,
            'auth' : True,
            'photo' : user.photo
        }
        if client:
            bookings = Booking.objects.filter(user=user, is_past=False)
            prev_bookings = Booking.objects.filter(user=user, is_past=True)
            excursions = []
            for booking in bookings:
                excursions.append(Excursion.objects.get(pk=booking.excursion))
            prev_excs = []
            for booking in prev_bookings:
                prev_excs.append(Excursion.objects.get(pk=booking.excursion))
            context.update({
                'excursions' : excursions,
                'prev_excs' : prev_excs,
                'range' : range(len(excursions))
            })
        else:
            excursions = Excursion.objects.filter(guide=user.pk, is_past=False)
            excs = []
            for exc in excursions:
                excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
        
            excursions_past = Excursion.objects.filter(guide=user.pk, is_past=True)
            context.update({
                'excursions': excs,
                'excursions_past' : excursions_past
            })
        return render(request, 'profile.html', context)
    return redirect('login')



def send_update(request, excursion_id=None):
    if request.method == 'POST' and excursion_id:
        data = request.POST
        header = data.get('header')
        text = data.get('text')
        print(header, text)
        update = Update(header=header, text=text, excursion=excursion_id)
        update.save()
        return redirect('profile')
    else:
        return HttpResponse('nah')



def updates(request):
    if request.session.get('is_authorized'):
        user = User.objects.get(id=request.session.get('user_id'))
        bookings = Booking.objects.filter(user=user)
        updates = Update.objects.all()
        ups = []
        for update in updates:
            for booking in bookings:
                if booking.excursion==update.excursion:
                    print(booking.excursion, update.excursion, update)
                    exc = Excursion.objects.get(id=update.excursion)
                    ups.append([update, exc])
                    print(exc)
        context = {
            'updates' : ups,
            'auth' : True
        }
    else:
        context = {
            'message' : 'Here you will see all updates on your bookings!'
        }
    return render(request, 'updates.html', context)


def review(request, excursion_id=None):
    if excursion_id:
        if request.method == "POST":
            rating = int(request.POST.get('rating'))
            print(rating)
            review = request.POST.get('review')
            update = request.POST.get('update')
            
            update = Update.objects.get(id=update)
            excursion = Excursion.objects.get(id=excursion_id)
            guide = User.objects.get(id=excursion.guide)
            guide.rating = (guide.rating * guide.rating_number + rating)/(guide.rating_number+1)
            guide.save()
            review_ = Review(
                user = User.objects.get(id=request.session.get('user_id')),
                object_id = guide.id,
                rating = rating,
                text = review
            )
            review_.save()
            update.delete()
            
            return redirect('updates')
            
    return HttpResponse("Invalid request")


def guides(request):
    auth = True if request.session.get('is_authorized') else False
    guides_ = User.objects.filter(status='guide')
    ratings = [int(i.rating*20) for i in guides_]
    print(ratings)
    guides = []
    for i in range(len(ratings)):
        guides.append([guides_[i], ratings[i], len(Review.objects.filter(object_id=guides_[i].id))])
    print(guides)
    return render(request, 'guides.html', {'guides' : guides, 'auth' : auth})


def guide(request, guide_id = None):
    auth = True if request.session.get('is_authorized') else False
    guide = User.objects.get(id=guide_id)
    rating = int(guide.rating*20)
    print(guide.rating, guide.photo, rating)
    excursions = Excursion.objects.filter(guide=guide_id, is_available=True, is_past=False)
    excs = []
    for exc in excursions:
        excs.append([exc, int(User.objects.get(id=exc.guide).rating)*20, len(Booking.objects.filter(excursion=exc.id))])
    reviews = Review.objects.filter(object_id=guide_id)
    return render(request, 'guide.html',{
                                            'guide' : guide, 
                                            'rating' : rating, 
                                            'excursions' : excs,
                                            'reviews' : reviews,
                                            'auth' : auth
                                        })
    