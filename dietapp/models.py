from django import forms
from django.db import models
from django.db.models import TextChoices
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Utility function for user file upload paths
def user_directory_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'


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
        if self.calories < 0:
            raise ValidationError("Calories cannot be negative.")
        if self.protein < 0 or self.carbs < 0 or self.fat < 0:
            raise ValidationError("Nutritional values cannot be negative.")
        calculated_calories = (4 * self.protein) + (4 * self.carbs) + (9 * self.fat)
        if self.calories > calculated_calories:
            raise ValidationError(
                f"Calories exceed the calculated value from macros: {calculated_calories:.2f} kcal."
            )

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
