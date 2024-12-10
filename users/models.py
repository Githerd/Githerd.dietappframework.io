from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

# User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    dietary_preferences = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
