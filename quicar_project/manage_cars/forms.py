from django import forms
from .models import RentalCar

class RentalCarForm(forms.ModelForm):
    class Meta:
        model = RentalCar
        fields = ['name', 'image', 'price', 'description', 'year', 'engine']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            raise forms.ValidationError("Price is required and should be a valid decimal.")
        return price

    def clean_mileage(self):
        mileage = self.cleaned_data.get('mileage')
        if not mileage:
            raise forms.ValidationError("Mileage is required and should be a valid decimal.")
        return mileage
