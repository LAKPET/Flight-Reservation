from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.db.models import Max
import re
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from datetime import datetime
from .models import Passenger,Flight,seat,Ticket


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

def payment2(request):
    data = {}
    return render(request, 'payment2.html', data)

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
        # Merge the dictionaries into a single dictionary
        data = {'flights': flights, 'seats': seats}
        # print(data)

        return render(request, 'search_results2.html', data)
    else:
        # Handle other HTTP methods if needed
        pass

def booking(request):
    if request.method == 'GET':
        # Retrieve data from the URL parameters
        flight_id = request.GET.get('flight_id')
        airline = request.GET.get('airline')
        departure_airport = request.GET.get('departure_airport')
        arrival_airport = request.GET.get('arrival_airport')
        flight_class = request.GET.get('flight_class')
        seat_class = request.GET.get('seat_class')
        seat_id = request.GET.get('seat_id')
        departure_date = request.GET.get('departure_date')
        departure_time = request.GET.get('departure_time')
        arrival_date = request.GET.get('arrival_date')
        arrival_time = request.GET.get('arrival_time')
        duration = request.GET.get('duration')
        price = request.GET.get('price')

        # Example: Perform additional logic with the retrieved data
        # Here, we'll simply pass the data to the template
        data = {
            'flight_id': flight_id,
            'airline': airline,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'flight_class': flight_class,
            'seat_class': seat_class,
            'seat_id': seat_id,
            'departure_date': departure_date,
            'departure_time': departure_time,
            'arrival_date': arrival_date,
            'arrival_time': arrival_time,
            'duration': duration,
            'price': price,
        }
        return render(request, 'booking.html', data)
    else:
        # Handle other HTTP methods if needed
        return render(request, 'booking.html')

def createticket(flight_id, seat_class, total_amount, username, booking_date, departure_date):  
    if Ticket.objects.count() != 0:
        ticket_id_max = Ticket.objects.aggregate(Max('ticket_id'))['ticket_id__max']
        last_ticket_number = int(ticket_id_max[6:]) if ticket_id_max else 1000
        next_ticket_number = last_ticket_number + 1
        next_ticket_id = f'TICKET{next_ticket_number:04}'
    else:
        next_ticket_id = "TICKET1001"

    ticket_id = next_ticket_id
    booking_date = reFormatDateYYYYMMDDV2(booking_date)

    ticket = Ticket.objects.create(
        ticket_id=ticket_id,
        flight_id=flight_id,
        seat_class=seat_class,
        total_amount=total_amount,
        username=username,
        booking_date=booking_date,
        departure_date=departure_date,
        status='PENDING'
    )
    ticket.save()
    return ticket
 
def passenger(request):
    if request.method == 'POST':
        if Passenger.objects.count() != 0:
            id_no_max = Passenger.objects.aggregate(Max('id_no'))['id_no__max']
            print(id_no_max)
            id_no_matches = re.findall(r'(\w+?)(\d+)', id_no_max)
            if id_no_matches:
                id_no_temp = id_no_matches[0]
                next_id_no = id_no_temp[0] + str(int(id_no_temp[1]) + 1)
            else:
                next_id_no = "7201"
        else:
            next_id_no = "7201"
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']

        flight_id       =   request.POST['flight_id']
        seat_class      =   request.POST['seat_class']
        total_amount    =   request.POST['price']
        username        =   request.POST['username']
        booking_date    =   request.POST['booking_date']
        departure_date  =   request.POST['departure_date']
        ticket = createticket(flight_id,seat_class,total_amount,username,booking_date,departure_date)
        ticket.save()
        # Create a new Passenger instance
        passenger = Passenger.objects.create(
                id_no=next_id_no,
                first_name=first_name, 
                last_name=last_name, 
                email=email,
                phone_no=phone_no,
                ticket_id=ticket)
        ticket_id = ticket.ticket_id
        print(passenger)
        # Save the Passenger instance to the database
        try:passenger.save()
            
        except: redirect('/')
    return render(request,'payment.html',{'ticket_id':ticket_id,'total_amount':total_amount})

def reFormatDateYYYYMMDDV2(yyyymmdd):
    if (yyyymmdd == ''):
        return ''
    return yyyymmdd[:4] + "-" + yyyymmdd[5:7] + "-" + yyyymmdd[8:10]
