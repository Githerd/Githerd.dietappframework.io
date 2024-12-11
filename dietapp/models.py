from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import TextChoices

User = get_user_model()  # Use this dynamically to reference the custom user model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
        
class FoodComponent(models.Model):
    name = models.CharField(max_length=50)
    gfat = models.PositiveIntegerField(default=0, verbose_name="Fat (g)")
    gcarb = models.PositiveIntegerField(default=0, verbose_name="Carbs (g)")
    gprotein = models.PositiveIntegerField(default=0, verbose_name="Protein (g)")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals", db_index=True)
    name = models.CharField(max_length=100)
    calories = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    protein = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    carbs = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    fat = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"


# Define other models similarly, ensuring no direct cross-imports

class DaysOfWeek(TextChoices):
    MONDAY = 'Monday', _('Monday')
    TUESDAY = 'Tuesday', _('Tuesday')
    WEDNESDAY = 'Wednesday', _('Wednesday')
    THURSDAY = 'Thursday', _('Thursday')
    FRIDAY = 'Friday', _('Friday')
    SATURDAY = 'Saturday', _('Saturday')
    SUNDAY = 'Sunday', _('Sunday')


class Weekly(models.Model):
    day = models.CharField(
        max_length=10,
        choices=DaysOfWeek.choices,
        default=DaysOfWeek.MONDAY,
    )
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name="weekly_meals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_entries")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'user'], name='unique_weekly_meal_for_user'),
        ]
        ordering = ['day']

    def __str__(self):
        return f"{self.meal.name} on {self.get_day_display()} for {self.user.username}"
