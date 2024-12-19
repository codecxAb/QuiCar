from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Dealer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure user field is present
    name = models.CharField(max_length=255)  # Dealer's name
    upi_id = models.CharField(max_length=255, unique=True, null=False, blank=False)  # Dealer's UPI ID (required)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Check if UPI ID is valid (you can also add a pattern check here for UPI format)
        if self.upi_id and len(self.upi_id) < 5:  # Example: length check
            # Instead of raising ValidationError, you can set a message to be passed to the form
            self.upi_id_error = "UPI ID should be at least 5 characters long"


    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures that the `clean()` method is called before saving
        super().save(*args, **kwargs)  # Call the parent class's save method