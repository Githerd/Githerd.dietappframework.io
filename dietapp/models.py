from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Choices
EXERCISE_TYPE_CHOICES = [
    ('cardio', 'Cardio'),
    ('strength', 'Strength'),
]

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Age")
    weight = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Weight (kg)")
    height = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Height (cm)")
    dietary_preferences = models.TextField(blank=True, null=True, verbose_name="Dietary Preferences")

    def __str__(self):
        return f"Profile of {self.user.username}"


# Meal Model
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100, verbose_name="Meal Name")
    calories = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Calories")
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Protein (g)")
    carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Carbs (g)")
    fat = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Fat (g)")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Meal"
        verbose_name_plural = "Meals"

    def __str__(self):
        return f"Meal: {self.name} by {self.user.username}"

    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})


# Vitamins and Minerals for Meal
class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins")
    name = models.CharField(max_length=50, verbose_name="Vitamin Name")
    percentage = models.PositiveIntegerField(default=0, verbose_name="Percentage (%)")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


class Mineral(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="minerals")
    name = models.CharField(max_length=50, verbose_name="Mineral Name")
    percentage = models.PositiveIntegerField(default=0, verbose_name="Percentage (%)")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


# Exercise Model
class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100, verbose_name="Exercise Name")
    type = models.CharField(max_length=50, choices=EXERCISE_TYPE_CHOICES, verbose_name="Exercise Type")
    duration = models.IntegerField(validators=[MinValueValidator(0)], help_text="Duration in minutes")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


# Health Data
class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_data")
    weight = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Weight (kg)")
    height = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Height (cm)")
    age = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Age")
    calories_intake = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Calories Intake")
    calories_burned = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Health Data"
        verbose_name_plural = "Health Data"

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg ({self.date})"

    @property
    def bmi(self):
        if self.height > 0:
            return round(self.weight / (self.height / 100) ** 2, 2)
        return None


# Weekly Meal Plan
class Weekly(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, verbose_name="Day of the Week")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="weekly_meals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_entries")

    class Meta:
        ordering = ['day']
        verbose_name = "Weekly Meal Plan"
        verbose_name_plural = "Weekly Meal Plans"

    def __str__(self):
        return f"{self.meal.name} on {self.day} for {self.user.username}"


# Messaging System
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(default=now, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
