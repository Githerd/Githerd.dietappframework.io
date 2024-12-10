from django import forms
from django.db import models
from django.db.models import TextChoices
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Utility function for user file upload paths
def user_directory_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'

    
    @property
    def bmi(self):
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100, verbose_name="Meal Name")
    calories = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Calories (kcal)")
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Protein (g)")
    carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Carbs (g)")
    fat = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Fat (g)")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Meal"
        verbose_name_plural = "Meals"

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"

    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})

    def clean(self):
        """
        Custom validation to ensure the meal's nutritional values make sense.
        """
        if self.calories < 0:
            raise ValidationError("Calories cannot be negative.")
        if self.protein < 0 or self.carbs < 0 or self.fat < 0:
            raise ValidationError("Nutritional values cannot be negative.")

        # Validate calorie consistency: calories = 4 * (protein + carbs) + 9 * fat
        calculated_calories = (4 * self.protein) + (4 * self.carbs) + (9 * self.fat)
        if self.calories > calculated_calories:
            raise ValidationError(
                f"Calories exceed the calculated value from macros: {calculated_calories:.2f} kcal."
            )

    @property
    def macronutrient_distribution(self):
        """
        Returns the macronutrient distribution as a percentage.
        """
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



class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs', 'fat', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')
        if calories is not None and calories < 0:
            raise ValidationError("Calories cannot be negative.")
        return calories

    def clean_protein(self):
        protein = self.cleaned_data.get('protein')
        if protein is not None and protein < 0:
            raise ValidationError("Protein cannot be negative.")
        return protein

    def clean_carbs(self):
        carbs = self.cleaned_data.get('carbs')
        if carbs is not None and carbs < 0:
            raise ValidationError("Carbohydrates cannot be negative.")
        return carbs

    def clean_fat(self):
        fat = self.cleaned_data.get('fat')
        if fat is not None and fat < 0:
            raise ValidationError("Fat cannot be negative.")
        return fat



# Weekly Plan Model
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
        verbose_name="Day of the Week",
        default=DaysOfWeek.MONDAY  # Optional default value
    )
    meal = models.ForeignKey(
        'Meal',
        on_delete=models.CASCADE,
        related_name="weekly_meals",
        verbose_name="Meal"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="weekly_entries",
        verbose_name="User"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'user'], name='unique_weekly_meal_for_user'),
        ]
        ordering = ['day']
        verbose_name = "Weekly Plan"
        verbose_name_plural = "Weekly Plans"

    def __str__(self):
        return f"{self.meal.name} on {self.get_day_display()} for {self.user.username}"



# Vitamins for Meals
class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percentage__gte=0) & models.Q(percentage__lte=100),
                name="valid_percentage_range"
            ),
        ]

    def clean(self):
        if not (0 <= self.percentage <= 100):
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


# Minerals for Meals
class Mineral(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="minerals")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percentage__gte=0) & models.Q(percentage__lte=100),
                name="valid_percentage_range"
            ),
        ]

    def clean(self):
        if not 0 <= self.percentage <= 100:
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"



# Exercise Model
class Exercise(models.Model):
    class ExerciseType(TextChoices):
        CARDIO = 'cardio', _('Cardio')
        STRENGTH = 'strength', _('Strength')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ExerciseType.choices)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name="Duration (minutes)")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories Burned")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


# TDEE Model
class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee")
    calories = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal" 


# Journal Entry Model
class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('journal-detail', kwargs={'pk':self.pk})


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
