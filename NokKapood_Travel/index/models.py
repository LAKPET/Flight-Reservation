from django.db import models


# Create your models here.

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
    
    




