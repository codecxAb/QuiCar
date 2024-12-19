from django.db import models
from django.contrib.auth.models import User
import random
from django.core.exceptions import ValidationError

# Dealer Model to store UPI details
from django.db import models
from user_auth.models import Dealer


# Car Model (RentalCar)
class RentalCar(models.Model):
    car_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='car_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    year = models.PositiveIntegerField()
    engine = models.CharField(max_length=255)
    availability_status = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    rental_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rental_duration = models.PositiveIntegerField(null=True, blank=True)
    CAR_TYPES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Sports Car', 'Sports Car'),
        ('Luxury', 'Luxury'),
        ('Convertible', 'Convertible'),
    ]
    car_type = models.CharField(max_length=100, choices=CAR_TYPES)
    
    # dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="cars")  # Reference to the Dealer
  # Set a default dealer for existing records
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="cars", default=1)  # Default to a dealer with id=1

    def __str__(self):
        return f"{self.name} ({self.car_type})"

    def available_for_rent(self):
        return self.availability_status

    def save(self, *args, **kwargs):
        if self.car_id is None:
            self.car_id = random.randint(0, 100)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.rental_rate:
            raise ValidationError("Rental rate is required")
        if not self.rental_duration:
            raise ValidationError("Rental duration is required")

# Transaction Model to store rental transactions
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(RentalCar, on_delete=models.CASCADE,default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_duration = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Paid', 'Paid'),
    ]
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    # payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    status = models.CharField(max_length=20, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='In Progress')
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} rented car {self.car.name}"

    def calculate_total_cost(self):
        if self.car and self.car.rental_rate and self.rental_duration:
            return self.car.rental_rate * self.rental_duration
        return 0.00

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.calculate_total_cost()
        
        if self.status == 'Completed' and self.payment_status == 'Paid':
            self.car.availability_status = False
            self.car.save()

        super().save(*args, **kwargs)

    def initiate_payment(self):
        """ Initiate the payment process by returning the dealer's UPI ID. """
        if self.car and self.car.dealer:
            return self.car.dealer.upi_id  # Fetch UPI ID from the car's dealer
        return None

    def clean(self):
        if not self.start_date or not self.end_date:
            raise ValidationError("Start and end dates are required")
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date")
        
        