# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Dealer

@receiver(post_save, sender=User)
def create_dealer(sender, instance, created, **kwargs):
    if created:
        # Create a dealer linked to the newly created user
        Dealer.objects.create(
            # user=instance,
            name=instance.username,  # Default name, you can customize this
            upi_id="default_upi_id"  # You can use a default or custom logic to set the UPI ID
        )

# Connect the signal
post_save.connect(create_dealer, sender=User)
