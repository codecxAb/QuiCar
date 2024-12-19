from django import forms
from .models import RentalCar

class RentalCarForm(forms.ModelForm):
    class Meta:
        model = RentalCar
        fields = [
            'name', 'image', 'price', 'description', 'year', 
            'engine', 'location', 'rental_rate', 'rental_duration', 'car_type'
        ]
    
    def clean(self):
        cleaned_data = super().clean()  # This ensures the cleaned data is passed back
        
        price = cleaned_data.get('price')
        rental_rate = cleaned_data.get('rental_rate')
        rental_duration = cleaned_data.get('rental_duration')
        location = cleaned_data.get('location')
        engine = cleaned_data.get('engine')

        # Custom validations
        if price is None or price <= 0:
            self.add_error('price', "Price is required and should be a positive number.")
        
        if rental_rate is None or rental_rate <= 0:
            self.add_error('rental_rate', "Rental rate is required and should be a positive number.")
        
        if rental_duration is None or rental_duration <= 0:
            self.add_error('rental_duration', "Rental duration is required and should be a positive number.")
        
        if not location:
            self.add_error('location', "Location is required.")
        
        if not engine:
            self.add_error('engine', "Engine information is required.")
        
        # Return cleaned data to ensure form validation continues
        return cleaned_data

    # def clean_mileage(self):
    #     # Mileage validation, as this is a separate field and not in the clean() method
    #     mileage = self.cleaned_data.get('mileage')
    #     if mileage is not None and mileage < 0:
    #         raise forms.ValidationError("Mileage cannot be negative.")
    #     return mileage
