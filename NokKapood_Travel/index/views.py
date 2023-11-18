from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    data = {}
    return render(request, 'index.html', data)

def my_booking(request):
    tickets = list(Ticket.objects.filter(username=request.user.username).order_by('-ticket_id').values('ticket_id','flight_id','departure_date',
                                                                                            'seat_class','total_amount','booking_date','status'))
    data=dict()
    data['tickets'] = tickets
    return render(request, 'my_booking.html', data)


def login_page(request):
    data = {}
    return render(request, 'login.html', data)

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