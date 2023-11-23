from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Flight
from .models import seat
from .models import Ticket
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime


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

def bookingflight(request):
    return render(request, 'ticket_info.html')

def my_booking(request):
    tickets = list(Ticket.objects.filter(username=request.user.username).order_by('-ticket_id').values('ticket_id','flight_id','departure_date',
                                                                                            'seat_class','total_amount','booking_date','status'))
    data=dict()
    data['tickets'] = tickets
    return render(request, 'my_booking.html', data)

def finalreservation(request):
    data = {}
    return render(request, 'finalreservation.html', data)

def payment(request):
    data = {}
    return render(request, 'payment.html', data)

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
        flight = Flight.objects.filter(departure_airport=start, arrival_airport=goal).first()

        if flight:
            paths = list(Flight.objects.filter(departure_airport=start, arrival_airport=goal).values())
            cities = list(Flight.objects.filter(departure_airport=start).values())
            cities2 = list(Flight.objects.filter(arrival_airport=goal).values())

            flights = Flight.objects.filter(flight_id=flight.flight_id, departure_date=date, flight_class=seat_type).values(
                'flight_id', 'airline', 'departure_time', 'arrival_time', 'departure_date', 'duration', 'arrival_date',
                'departure_airport', 'arrival_airport', 'flight_class', 'price'
            )

            data = {
                'paths': paths,
                'flights': flights,
                'cities': cities,
                'cities2': cities2,
            }
            return render(request, 'ticket_list.html', data)
        # else:
        #     # Handle the case when no flight is found
        #     return render(request, 'no_flight_found.html')


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
    
from datetime import datetime

def search_results(request):
    if request.method == 'GET':
        departure_airport = request.GET.get('select_start')
        arrival_airport = request.GET.get('select_goal')
        filght_class = request.GET.get('filght_class')
        seat_class = request.GET.get('seatClass')
        flight_date_str = request.GET.get('txt_flightDate')
        print(departure_airport)
        print(arrival_airport)
        print(seat_class)
        print(flight_date_str)

        # Check if flight_date_str is not None before parsing
        if flight_date_str:
            flight_date = datetime.strptime(flight_date_str, '%Y-%m-%d').date()
            # Continue with your logic using flight_date
        else:
            # Handle the case when flight_date_str is None (e.g., set a default value or return an error response)
            return HttpResponse("Invalid or missing flight date")

        # Use the input values to query the database
        flights = Flight.objects.filter(
            departure_airport__icontains=departure_airport,
            arrival_airport__icontains=arrival_airport,
            flight_class__icontains=filght_class,
            departure_date=flight_date
        )
        seats = seat.objects.filter(
            seat_class__icontains=seat_class,
        )
        print(flights)
        print(seats)
        # Merge the dictionaries into a single dictionary
        data = {'flights': flights, 'seats': seats}
        print(data)

        return render(request, 'search_results.html', data)
    else:
        # Handle other HTTP methods if needed
        pass

