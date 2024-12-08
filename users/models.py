from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


# Custom User model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


# Signal to create and save UserProfile and Profile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    instance.profile.save()


# UserProfile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
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

    def clean(self):
        if self.age and (self.age <= 0 or self.age > 150):
            raise ValidationError("Age must be between 1 and 150.")
        if self.height and self.height <= 0:
            raise ValidationError("Height must be a positive value.")
        if self.weight and self.weight <= 0:
            raise ValidationError("Weight must be a positive value.")

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_image")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile Image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


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
        default='moderate',
        db_index=True
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
        default='maintain',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_calories(self, meals):
        """Calculate total calories from a list of meals."""
        return sum(meal.calories for meal in meals if meal.user == self.user)

    def __str__(self):
        return f"{self.user.username}'s Diet Data"
