from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Flight


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