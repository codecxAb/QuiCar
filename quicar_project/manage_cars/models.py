from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import random
from user_auth.models import CustomUser


def generate_random_car_id():
    return random.randint(100, 999)

# Dealer Model (now handled by the CustomUser model)
# No need for a separate Dealer model, as it's now part of the CustomUser model

# RentalCar Model (Car Rental)
class RentalCar(models.Model):
    car_id = models.AutoField(primary_key=True,default=generate_random_car_id )
    name = models.CharField(max_length=255)
    dealer = models.ForeignKey('user_auth.CustomUser', on_delete=models.CASCADE, related_name="cars", limit_choices_to={'user_type': 'dealer'})
    image = models.ImageField(upload_to='car_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    year = models.PositiveIntegerField()
    engine = models.CharField(max_length=255)
    availability_status = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    rental_rate = models.DecimalField(max_digits=10, decimal_places=2)
    rental_duration = models.PositiveIntegerField()

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
        return self.availability_status

    def save(self, *args, **kwargs):
        if not self.rental_rate:
            raise ValidationError("Rental rate is required")
        if not self.rental_duration:
            raise ValidationError("Rental duration is required")
        # Ensure the car_id is generated
        if not self.car_id:
            self.car_id = generate_random_car_id()
        super().save(*args, **kwargs)

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'})
    car = models.ForeignKey(RentalCar, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_duration = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

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

        # If the status is 'Completed' and payment is 'Paid', update car availability
        if self.status == 'Completed' and self.payment_status == 'Paid':
            self.car.availability_status = False  # Car is no longer available for rent
            self.car.save()

        super().save(*args, **kwargs)

    def initiate_payment(self):
        """Initiate the payment process by returning the dealer's UPI ID."""
        if self.car and self.car.dealer:
            return self.car.dealer.profile.upi_id  # Fetch UPI ID from the car's dealer
        return None

    def clean(self):
        if not self.start_date or not self.end_date:
            raise ValidationError("Start and end dates are required")
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date")

    @staticmethod
    def is_car_available(car, start_date, end_date):
        """Check if the car is available for rent during the requested period."""
        conflicting_transactions = Transaction.objects.filter(
            car=car,
            status='In Progress',  # Only consider transactions that are still in progress
            end_date__gte=start_date,  # Existing rental end date overlaps with the requested start date
            start_date__lte=end_date   # Existing rental start date overlaps with the requested end date
        )

        if conflicting_transactions.exists():
            return False  # Car is not available due to conflicting transactions

        return True  # Car is available for the requested period