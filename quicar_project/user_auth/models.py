from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
import random
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    # USER_TYPE_CHOICES = (
    #     ('customer', 'Customer'),
    #     ('dealer', 'Dealer'),
    # )
    user_type = models.CharField(max_length=50, choices=[('customer', 'Customer'), ('dealer', 'Dealer')], default='customer')

    # user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    contact_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='Contact Number')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Full Name')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default.jpg', verbose_name='Profile Picture')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)