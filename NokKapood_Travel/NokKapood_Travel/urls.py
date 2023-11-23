"""NokKapood_Travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from index import views 
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page' ),
    path('login', views.login, name='login' ),
    path('register', views.register, name='register' ),
    path('custom',views.custom , name= 'custom'),
    path('page_login/', views.page_login, name='page_login'),
    path('home',views.home , name= 'home'),
    path('search_flights',views.search_flights , name= 'search_flights'),
    path('payment',views.payment , name= 'payment'),
    path('finalreservation',views.finalreservation , name= 'finalreservation'),
    path('flight/list/<str:start>/<str:goal>/<str:date>/<str:seat_type>',views.FlightList.as_view(),name="FlightList"),
    path('flight/booking',views.bookingflight, name="bookpage"),
    path('mybooking',views.my_booking, name='mybooking'),
    path('search_results/',views.search_results, name='search_results'),
    
    path('information/<int:user_id>/',views.information, name='information'),
    
]
