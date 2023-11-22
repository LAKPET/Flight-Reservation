from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Flight
from .models import seat
from django.views.generic import View
from django.http import JsonResponse


# Create your views here.

def index(request):
    data = {}
    return render(request, 'index.html', data)


def login_page(request):
    data = {}
    return render(request, 'login.html', data)


def page_login(request):
    return render(request, 'page_login.html')

def information(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'information.html', {'user': user})

def search_flights(request):
    # For simplicity, let's retrieve all flights for now
    flights = Flight.objects.all()

    data = {'flights': flights}
    return render(request, 'search_flights.html', data)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password =password  )
        if user is not None:
            auth.login(request , user)
            return redirect('page_login/')    
        else:
            messages.info(request, 'invalid username or password')
            return redirect("login_page")
    else:
        return render(request,'index.html')
    
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name)
        user.save()

        # Log in the user after registration
        auth.login(request, user)

        # Redirect to the information page with user data
        return redirect('information', user_id=user.id)

    return render(request, 'register.html')

def custom(request):
        return render(request, 'custom.html')

def home(request):
        return render(request, 'home.html')

class FlightList(View):
    def get(self, request, start, goal, date, seat_type):
        flight_id     = Flight.objects.filter(departure_airport=start,arrival_airport=goal).values()
        paths       = list(Flight.objects.filter(departure_airport=start,arrival_airport=goal).values())
        cities = list(Flight.objects.filter(departure_airport=start).values())
        cities2 = list(Flight.objects.filter(arrival_airport=goal).values())
        flights     = Flight.objects.all().select_related('flight_id').filter(flight_id=flight_id,departure_date=date,flight_id__seat_class=seat_type).values('flight_id','airline','departure_time','arrival_time','departure_date','duration','arrival_date','departure_airport','arrival_airport','flight_id__seat_class', 'flight_id__price')
        data = dict()
        data['paths'] = paths[0]
        data['flights'] = flights
        data['cities'] = cities[0] 
        data['cities2'] = cities2[0]
        return render(request, 'ticket_list.html', data)

class FlightDetail(View):
    def get(self, request, id):
        flight = list(Flight.objects.filter(flight_id=id).values('flight_id','airline','departure_time','arrival_time','duration','arrival_date', 'departure_date'))
        flight_detail = list(seat.objects.select_related("flight_id").filter(flight_id=id).values('flight_id','seat_class','price'))
        # paths = list(Path.objects.filter(path_id=Flight.objects.filter(flight_id=id).values('path_id')[0]["path_id"]).values())
        data = dict()
        data['flight'] = flight[0]
        data['flight_detail'] = flight_detail[0]
        # data['paths'] = paths[0]
        return JsonResponse(data)