from django.db import models


# Create your models here.
class Booking(models.Model):
    booking_id = models.PositiveIntegerField(primary_key=True)
    user_id = models.PositiveIntegerField()
    booking_date = models.DateField()
    flight_id = models.CharField(max_length=100)

    class Meta:
        db_table = "booking"
        managed = False

    def __str__(self):
        return f"Booking {self.booking_id} - User {self.user_id}"

class Flight(models.Model):
    flight_id = models.CharField(max_length=100, primary_key=True)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)
    flight_class = models.CharField(max_length=10)
    flight_no = models.CharField(max_length=100)
    price = models.IntegerField()
    departure_date = models.DateField()
    arrival_date = models.DateField()

    class Meta:
        db_table = "flight"
        managed = False

    def __str__(self):
        return f"Flight {self.flight_id} - {self.airline} ({self.flight_no})"
    
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
        managed = False
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


