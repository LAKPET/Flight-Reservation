from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Flight
from .forms import FlightSearchForm
# Create your views here.

def index(request):
    data = {}
    return render(request, 'index.html', data)


def login_page(request):
    data = {}
    return render(request, 'login.html', data)

def search_flights(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            trip_type = form.cleaned_data['trip_type']
            seat_class = form.cleaned_data['seat_class']
            departure = form.cleaned_data['departure']
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the database based on the user input
            flights = Flight.objects.filter(
                flight_class=seat_class,
                departure_airport=departure,
                arrival_airport=destination,
                departure_date__gte=start_date,
                arrival_date__lte=end_date
            )

            return render(request, 'search_results.html', {'flights': flights})

    else:
        form = FlightSearchForm()

    return render(request, 'search_flights.html', {'form': form})


def a(request):
    data = {}
    return render(request, 'a.html', data)

def information(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'a.html', {'user': user})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password =password  )
        if user is not None:
            auth.login(request , user)
            return redirect('/custom')    
        else:
            messages.info(request, 'invalid username or password')
            return redirect("login_page")
    else:
        return render(request,'home.html')
    
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
        return redirect('a', user_id=user.id)

    return render(request, 'register.html')

def custom(request):
        return render(request, 'custom.html')

def home(request):
        return render(request, 'home.html')