from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator, MinValueValidator


# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# UserProfile model
class UserProfile(models.Model):
    USER_GOALS = [
        ('lose_weight', 'Lose Weight'),
        ('gain_weight', 'Gain Weight'),
        ('maintain_weight', 'Maintain Weight'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    goal = models.CharField(max_length=50, choices=USER_GOALS, default='maintain_weight')
    image = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        """Calculate and return the Body Mass Index (BMI)."""
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None
