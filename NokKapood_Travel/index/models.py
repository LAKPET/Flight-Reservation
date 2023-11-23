from django.db import models


# Create your models here.
class booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    booking_date = models.DateField(null=True)
    flight_id = models.CharField(max_length=100)
    class Meta:
        db_table = "booking"
        managed = False
    def __str__(self):
        return self.booking_id

from django.db import models

class Flight(models.Model):
    flight_id = models.CharField(max_length=100, primary_key=True)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)
    flight_class = models.CharField(max_length=10)
    flight_no = models.CharField(max_length=100)
    price = models.IntegerField()
    departure_date = models.DateField(null=True)
    arrival_date = models.DateField(null=True)
    departure_time = models.TimeField(null=True)
    arrival_time = models.TimeField(null=True)
    duration = models.TimeField(null=True)

    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):

        return self.flight_id

class payment(models.Model):
    booking_id = models.IntegerField()
    payment_id = models.IntegerField(primary_key=True)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "payment"
        managed = False
    def __str__(self):
        return self.payment_id

class register(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "register"
        managed = False
    def __str__(self):
        return self.name

class seat(models.Model):
    seat_id = models.CharField(max_length=10, primary_key=True)
    flight_id = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    seat_class = models.CharField(max_length=100)

    class Meta:
        db_table = "seat"
        managed = True  # Set to True if you want Django to manage the table

    def __str__(self):
        return self.seat_id
        

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.payment_method
    
class users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100,null=True )
    password = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = "users"
        managed = False
    def __str__(self):
        return self.user_id
    
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    flight_id = models.CharField(max_length=5)
    username = models.CharField(max_length=100)
    seat_class = models.CharField(max_length=10)
    total_amount = models.FloatField(null=True, blank=True)
    departure_date = models.DateField()
    booking_date = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=10)
    class Meta:
        db_table = "ticket"
        managed = False
    def __str__(self):
        return str(self.ticket_id)


