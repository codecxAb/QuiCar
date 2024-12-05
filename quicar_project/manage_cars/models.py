from django.db import models
from django.contrib.auth.models import User  # Importing the User model

import random
from django.db import models
from django.contrib.auth.models import User

class RentalCar(models.Model):
    # Car Information
    car_id = models.PositiveIntegerField(unique=True, null=True, blank=True)  # Custom car ID
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='car_images/')  # Image upload field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    year = models.PositiveIntegerField()
    engine = models.CharField(max_length=255)
    # mileage = models.PositiveIntegerField(null=True)  # Mileage field as integer

    # Rental Specific Information
    availability_status = models.BooleanField(default=True)  # Whether car is available for rent
    location = models.CharField(max_length=255)
    rental_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # E.g., daily rate
    rental_duration = models.PositiveIntegerField(null=True, blank=True)  # Duration in days (numeric value)

    # Car Type Choices
    CAR_TYPES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Sports Car', 'Sports Car'),
        ('Luxury', 'Luxury'),
        ('Convertible', 'Convertible'),
    ]
    car_type = models.CharField(max_length=100, choices=CAR_TYPES)

    def __str__(self):
        return f"{self.name} ({self.car_type})"

    def available_for_rent(self):
        """ Returns whether the car is available for rent. """
        return self.availability_status

    def save(self, *args, **kwargs):
        # Generate a random car_id between 0 and 100 if it's not already set
        if self.car_id is None:
            self.car_id = random.randint(0, 100)  # Random ID between 0 and 100
        super().save(*args, **kwargs)

class Transaction(models.Model):
    # User who rented the car
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Car rented (using car_id)
    car_id = models.PositiveIntegerField()
    
    # Rental information
    start_date = models.DateField()
    end_date = models.DateField()
    rental_duration = models.PositiveIntegerField()  # Duration in days
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Transaction status
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Paid', 'Paid'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    
    # Payment details (optional, can be expanded based on payment gateway integration)
    payment_status = models.CharField(max_length=20, choices=[ 
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ], default='Pending')
    
    # Created and modified timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} rented car ID {self.car_id}"

    # Method to calculate the rental cost based on rental rate and duration
    def calculate_total_cost(self):
        """ Calculate the total rental cost. """
        car = RentalCar.objects.filter(car_id=self.car_id).first()
        if car and car.rental_rate and self.rental_duration:
            return car.rental_rate * self.rental_duration
        return 0.00

    def save(self, *args, **kwargs):
        """ Ensure total cost is calculated before saving the transaction. """
        if not self.total_cost:
            self.total_cost = self.calculate_total_cost()
        
        # Handle availability update after transaction completion
        if self.status == 'Completed' and self.payment_status == 'Paid':
            car = RentalCar.objects.filter(car_id=self.car_id).first()
            if car:
                # Mark car as unavailable for the duration of the rental
                car.availability_status = False
                car.save()

        super().save(*args, **kwargs)