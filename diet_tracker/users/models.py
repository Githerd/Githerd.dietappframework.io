from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User


# Custom User model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


# User Profile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return f'{self.user.username} Profile'

    @property
    def bmi(self):
        """Calculate and return the Body Mass Index (BMI)."""
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None


# Profile model for storing user profile images
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


# DietApp model for tracking user's diet-related information
class DietApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_level = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
        ],
        default='moderate'
    )
    dietary_preferences = models.TextField(blank=True, null=True, help_text="Dietary preferences or restrictions")
    food_allergies = models.TextField(blank=True, null=True, help_text="Any food allergies")
    goal = models.CharField(
        max_length=100,
        choices=[
            ('weight_loss', 'Weight Loss'),
            ('muscle_gain', 'Muscle Gain'),
            ('maintain', 'Maintain Weight'),
        ],
        default='maintain'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Diet Data"
