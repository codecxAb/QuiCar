from django import forms
from .models import RentalCar

class RentalCarForm(forms.ModelForm):
    class Meta:
        model = RentalCar
        fields = ['name', 'image', 'price', 'description', 'year', 'engine', 'availability_status', 'location', 'rental_rate', 'rental_duration', 'car_type']
