from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# Utility function for user file upload paths
def user_directory_path(instance, filename):
    return f'profile_pics/{instance.username}/{filename}'

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        default='default.jpg',
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    dietary_preferences = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def bmi(self):
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None
