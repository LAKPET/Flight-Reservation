from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    data = {}
    return render(request, 'index.html', data)

def login_page(request):
    data = {}
    return render(request, 'login.html', data)

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
        password= request.POST['password']
        user = User.objects.create_user(username = username , password = password , email = email)
        user.save()
        print('user created')
        return redirect('/custom')
    return render(request,'register.html')

def custom(request):
        return render(request, 'custom.html')

def home(request):
        return render(request, 'home.html')