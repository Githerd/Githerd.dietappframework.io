from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
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

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
        
    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        try:
            if self.height and self.weight:
                return round(self.weight / ((self.height / 100) ** 2), 2)
        except ZeroDivisionError:
            pass
        return None
        
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

class Vitamin(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='vitamins')
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Mineral(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='minerals')
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee", db_index=True, verbose_name=_("User"))
    calories = models.PositiveIntegerField(default=0, verbose_name=_("Calories"))
    date = models.DateField(auto_now_add=True, verbose_name=_("Date"))

    def clean(self):
        if self.calories < 500 or self.calories > 5000:
            raise ValidationError(_("Calories must be between 500 and 5000."))

    class Meta:
        verbose_name = _("TDEE")
        verbose_name_plural = _("TDEEs")

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal"

class Message(models.Model):
    """
    Represents a message sent between users.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-timestamp']

class Exercise(models.Model):
    """
    Represents an exercise activity for a user.
    """
    class ExerciseType(TextChoices):
        CARDIO = 'cardio', _('Cardio')
        STRENGTH = 'strength', _('Strength')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ExerciseType.choices)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name="Duration (minutes)")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        ordering = ['-date']

class JournalEntry(models.Model):
    """
    Represents a journal entry written by a user.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('journal-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
        ordering = ['-date_posted']
