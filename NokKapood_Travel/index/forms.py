# forms.py
from django import forms

class FlightSearchForm(forms.Form):
    TRIP_CHOICES = [
        ('roundTrip', 'Round Trip'),
        ('oneWay', 'One Way'),
    ]

    SEAT_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('firstClass', 'First Class'),
    ]

    trip_type = forms.ChoiceField(choices=TRIP_CHOICES, label='Trip Type')
    seat_class = forms.ChoiceField(choices=SEAT_CLASS_CHOICES, label='Seat Class')
    departure = forms.CharField(label='Departure Airport')
    destination = forms.CharField(label='Destination Airport')
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
