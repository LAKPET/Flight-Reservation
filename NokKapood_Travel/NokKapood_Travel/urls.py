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
    path('search_results/', views.search_results, name='search_results'),
    path('search_results2/', views.search_results2, name='search_results2'),
    path('payment',views.payment , name= 'payment'),
    path('payment2',views.payment2 , name= 'payment2'),
    path('finalreservation/', views.finalreservation, name='finalreservation'),
    path('qrcode',views.qrcode , name= 'qrcode'),
    path('search_results2/booking/',views.booking , name= 'booking'),
    path('search_results2/booking/passenger',views.passenger , name= 'passenger'),
    path('information/<int:user_id>/',views.information, name='information'),
    path('cancel_reservation/', views.cancel_reservation, name='cancel_reservation'),
    
]
