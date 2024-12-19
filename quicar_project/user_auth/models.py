from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Dealer(models.Model):
    name = models.CharField(max_length=255)  # Dealer's name
    upi_id = models.CharField(max_length=255, unique=True)  # Dealer's UPI ID (optional)
    
    # Other fields for the dealer, like contact info
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return self.name


    def clean(self):
        if not self.upi_id:
            raise ValidationError("UPI ID is required")