from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # Height in centimeters
    weight = models.FloatField(null=True, blank=True)  # Weight in kilograms
    goal = models.CharField(
        max_length=100,
        choices=[
            ('lose_weight', 'Lose Weight'),
            ('gain_weight', 'Gain Weight'),
            ('maintain_weight', 'Maintain Weight')
        ],
        default='maintain_weight'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    """
    Changes here explained below
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
