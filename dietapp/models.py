from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Age")
    weight = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Weight (kg)")
    height = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Height (cm)")
    dietary_preferences = models.TextField(blank=True, null=True, verbose_name="Dietary Preferences")

    def __str__(self):
        return f"Profile of {self.user.username}"


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

    def __str__(self):
        return f"Meal: {self.name} by {self.user.username}"

    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})


EXERCISE_TYPE_CHOICES = [
    ('cardio', 'Cardio'),
    ('strength', 'Strength'),
]


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100, verbose_name="Exercise Name")
    type = models.CharField(max_length=50, choices=EXERCISE_TYPE_CHOICES, verbose_name="Exercise Type")
    duration = models.IntegerField(validators=[MinValueValidator(0)], help_text="Duration in minutes")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


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

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg ({self.date})"

    @property
    def bmi(self):
        if self.height > 0:
            return round(self.weight / (self.height / 100) ** 2, 2)
        return None


class JournalEntry(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now, verbose_name="Date Posted")

    def __str__(self):
        return self.title


class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee")
    calories = models.PositiveIntegerField(default=0, verbose_name="Calories")
    date = models.DateField(auto_now_add=True, verbose_name="Date Recorded")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal"


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

    def __str__(self):
        return f"{self.meal.name} on {self.day} for {self.user.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(default=now, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
