from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()  # Correct way to reference the User model

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved."""
    instance.profile.save()
