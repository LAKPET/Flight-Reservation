from django.db import models


# Create your models here.
class Booking(models.Model):
    booking_id = models.PositiveIntegerField(primary_key=True)
    user_id = models.PositiveIntegerField()
    booking_date = models.DateField()
    flight_id = models.CharField(max_length=100)

    class Meta:
        db_table = "booking"
        managed = True

    def __str__(self):
        return f"Booking {self.booking_id} - User {self.user_id}"
    
class seat(models.Model):
    seat_id = models.CharField(max_length=200, primary_key=True)
    flight_id = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=100)
    seat_class = models.CharField(max_length=100)
    price = models.IntegerField()

    class Meta:
        db_table = "seat"
        unique_together = (("flight_id", "seat_class"),)
        managed = True  # Set to True if you want Django to manage the table

    def __str__(self):
        return self.seat_id

class Flight(models.Model):
    flight_id = models.ForeignKey(seat,on_delete=models.CASCADE, db_column='flight_id')
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)
    flight_class = models.CharField(max_length=100)
    flight_no = models.CharField(max_length=100)
    price = models.IntegerField()
    departure_date = models.DateField()
    arrival_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=200)

    class Meta:
        db_table = "flight"
        managed = True

    def __str__(self):
        return self.flight_id
    
class payment(models.Model):
    booking_id = models.IntegerField()
    payment_id = models.IntegerField(primary_key=True)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "payment"
        managed = True
    def __str__(self):
        return self.payment_id

class register(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "register"
        managed = True
    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        db_table = "payment_method"
        managed = True
    def __str__(self):
        return self.payment_method
    
class users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100,null=True )
    password = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = "users"
        managed = True
    def __str__(self):
        return self.user_id


class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10, primary_key=True, unique=True)
    flight_id = models.CharField(max_length=5)
    username = models.CharField(max_length=100)
    seat_class = models.CharField(max_length=100)
    total_amount = models.FloatField(null=True, blank=True)
    departure_date = models.DateField()
    booking_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200)
    
    class Meta:
        db_table = "ticket"
        managed = True

    def __str__(self):
        return str(self.ticket_id)
    
class Passenger(models.Model):
    id_no = models.CharField(max_length=200, primary_key=True)  # เลขบัตรประชาชน/หมายเลขพาสปอร์ต
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    ticket_id = models.OneToOneField(Ticket, on_delete=models.CASCADE, db_column='ticket_id')

    class Meta:
        db_table = "passenger"
        managed = True

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name} {self.email}"
    
    




