from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

# Signal to create user profile after user is created
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check user_type and perform actions accordingly
        if instance.user_type == "dealer":
            # If the user is a dealer, handle dealer-specific logic
            # For example, you can set a default UPI ID or any other default value
            instance.name = instance.username  # Set name to username, can be customized
            instance.contact_number = instance.contact_number or "Not provided"
            instance.save()

        elif instance.user_type == "customer":
            # If the user is a customer, handle customer-specific logic
            # For example, you can add a default name or any other customer-related action
            instance.name = instance.username  # Set name to username, can be customized
            instance.contact_number = instance.contact_number or "Not provided"
            instance.save()

# Connect the signal
post_save.connect(create_user_profile, sender=CustomUser)
