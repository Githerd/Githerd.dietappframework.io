from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

User = get_user_model()

# Food Components Models
class FoodComponent(models.Model):
    name = models.CharField(max_length=50)
    gfat = models.PositiveIntegerField(default=0, verbose_name="Fat (g)")
    gcarb = models.PositiveIntegerField(default=0, verbose_name="Carbs (g)")
    gprotein = models.PositiveIntegerField(default=0, verbose_name="Protein (g)")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Carbs(FoodComponent):
    pass


class Fats(FoodComponent):
    pass


class Proteins(FoodComponent):
    pass


class Drinks(FoodComponent):
    pass


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

    @property
    def macronutrient_distribution(self):
        total_calories = self.calories
        if total_calories == 0:
            return {"protein": 0, "carbs": 0, "fat": 0}

        protein_calories = self.protein * 4
        carb_calories = self.carbs * 4
        fat_calories = self.fat * 9

        return {
            "protein": round((protein_calories / total_calories) * 100, 2),
            "carbs": round((carb_calories / total_calories) * 100, 2),
            "fat": round((fat_calories / total_calories) * 100, 2),
        }


class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def clean(self):
        if not (0 <= self.percentage <= 100):
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


class Mineral(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="minerals")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def clean(self):
        if not (0 <= self.percentage <= 100):
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


class Exercise(models.Model):
    class ExerciseType(TextChoices):
        CARDIO = 'cardio', _('Cardio')
        STRENGTH = 'strength', _('Strength')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises", db_index=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ExerciseType.choices)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name="Duration (minutes)")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee", db_index=True)
    calories = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal"


class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('journal-detail', kwargs={'pk': self.pk})


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class DaysOfWeek(models.TextChoices):
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
