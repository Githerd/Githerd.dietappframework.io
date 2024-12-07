from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now  


# Utility function for dynamic file paths
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profile_pics/<username>/<filename>
    return f'profile_pics/{instance.user.username}/{filename}'


# Custom User model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


# UserProfile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        default='default.jpg',
        upload_to=user_directory_path,
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
        """Custom validation for age, height, and weight."""
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
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path)

    def __str__(self):
        return f'{self.user.username} Profile Image'

    def save(self, *args, **kwargs):
        """Resize the image to reduce file size and maintain uniformity."""
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except Exception as e:
            # Log the error or handle it as per your requirements
            pass


class JournalEntry(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now, verbose_name="Date Posted")

    def __str__(self):
        return self.title


# Signal to create UserProfile and Profile automatically
@receiver(post_save, sender=User)
def create_and_save_user_profiles(sender, instance, created, **kwargs):
    """Create and save UserProfile and Profile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        instance.profile_image.save()


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
