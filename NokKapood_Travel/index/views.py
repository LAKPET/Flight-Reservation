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

from .models import Booking

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
    return render(request, 'finalreservation.html')

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
            print(user)
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

def qrcode(request):
        return render(request, 'qrcode.html')

def search_results(request):
    if request.method == 'GET':
        departure_airport = request.GET.get('select_start')
        arrival_airport = request.GET.get('select_goal')
        filght_class = request.GET.get('filght_class')
        seat_class = request.GET.get('seatClass')
        flight_date_str = request.GET.get('txt_flightDate')
        print(departure_airport,flight_date_str)
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
        ).values()
        seats = seat.objects.filter(
            seat_class__icontains=seat_class,
        ).values()
        print('flights:',flights)
        print('seats:',seats)
        # Merge the dictionaries into a single dictionary
        data = {'flights': flights, 'seats': seats}
        # print(data)

        return render(request, 'search_results.html', data)
    else:
        # Handle other HTTP methods if needed
        pass

def search_results2(request):
    if request.method == 'GET':
        departure_airport = request.GET.get('select_start')
        arrival_airport = request.GET.get('select_goal')
        filght_class = request.GET.get('filght_class')
        seat_class = request.GET.get('seatClass')
        flight_date_str = request.GET.get('txt_flightDate')
        print(departure_airport,flight_date_str)
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
        ).values()
        seats = seat.objects.filter(
            seat_class__icontains=seat_class,
        ).values()
        print('flights:',flights)
        print('seats:',seats)
        # Merge the dictionaries into a single dictionary
        data = {'flights': flights, 'seats': seats}
        # print(data)

        return render(request, 'search_results2.html', data)
    else:
        # Handle other HTTP methods if needed
        pass

def booking(request):
    if request.method == 'GET':
        departure_airport = request.GET.get('select_start')
        arrival_airport = request.GET.get('select_goal')
        filght_class = request.GET.get('filght_class')
        seat_class = request.GET.get('seatClass')
        flight_date_str = request.GET.get('txt_flightDate')
        print(departure_airport,flight_date_str)
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
        ).values()
        seats = seat.objects.filter(
            seat_class__icontains=seat_class,
        ).values()
        print('flights:',flights)
        print('seats:',seats)
        # Merge the dictionaries into a single dictionary
        data = {'flights': flights, 'seats': seats}
        # print(data)

        return render(request, 'booking.html', data)
    else:
        # Handle other HTTP methods if needed
        pass

