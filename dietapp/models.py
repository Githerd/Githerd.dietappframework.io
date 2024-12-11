from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import get_user_model here
from dietapp.models import Meal

User = get_user_model()  # Use get_user_model to fetch the custom user model


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals", db_index=True)
    name = models.CharField(max_length=100, verbose_name=_("Meal Name"))
    calories = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0, verbose_name=_("Calories"))
    protein = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0, verbose_name=_("Protein (g)"))
    carbs = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0, verbose_name=_("Carbohydrates (g)"))
    fat = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0, verbose_name=_("Fat (g)"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"

    @property
    def calculated_calories(self):
        return round((self.protein * 4) + (self.carbs * 4) + (self.fat * 9), 2)


class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins", verbose_name=_("Meal"))
    name = models.CharField(max_length=50, verbose_name=_("Vitamin Name"))
    percentage = models.PositiveIntegerField(default=0, verbose_name=_("Daily Value Percentage"))

    class Meta:
        unique_together = ('meal', 'name')
        verbose_name = _("Vitamin")
        verbose_name_plural = _("Vitamins")

    def clean(self):
        if not (0 <= self.percentage <= 100):
            raise ValidationError(_("Percentage must be between 0 and 100."))

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


class DaysOfWeek(models.TextChoices):
    MONDAY = 'MON', _('Monday')
    TUESDAY = 'TUE', _('Tuesday')
    WEDNESDAY = 'WED', _('Wednesday')
    THURSDAY = 'THU', _('Thursday')
    FRIDAY = 'FRI', _('Friday')
    SATURDAY = 'SAT', _('Saturday')
    SUNDAY = 'SUN', _('Sunday')


class Weekly(models.Model):
    day = models.CharField(
        max_length=3,
        choices=DaysOfWeek.choices,
        default=DaysOfWeek.MONDAY,
        verbose_name=_("Day of the Week")
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="weekly_meals", verbose_name=_("Meal"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_entries", verbose_name=_("User"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'user'], name='unique_weekly_meal_for_user'),
        ]
        ordering = ['day']
        verbose_name = _("Weekly Plan")
        verbose_name_plural = _("Weekly Plans")

    def clean(self):
        if Weekly.objects.filter(day=self.day, user=self.user).exists():
            raise ValidationError(_("A meal for this day is already assigned to this user."))

    def __str__(self):
        return f"{self.meal.name} on {self.get_day_display()} for {self.user.username}"
