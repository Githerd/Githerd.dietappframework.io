from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    dietary_preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    fat = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[('cardio', 'Cardio'), ('strength', 'Strength')])
    duration = models.IntegerField(validators=[MinValueValidator(0)], help_text="Duration in minutes")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_data")
    weight = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    age = models.IntegerField(validators=[MinValueValidator(0)])
    calories_intake = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    calories_burned = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg ({self.date})"

    @property
    def bmi(self):
        if self.height > 0:
            return self.weight / (self.height / 100) ** 2
        return None