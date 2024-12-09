from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now, timedelta
from .forms import TDEEForm
from .models import Profile, Meal


# TDEEView
class TDEEView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TDEEForm()
        result = None

        # Pre-fill the form with user profile data, if available
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile:
            form.initial['weight'] = profile.weight
            form.initial['height'] = profile.height
            form.initial['age'] = getattr(profile, 'age', 30)  # Default to 30 if age is not set

        context['form'] = form
        context['result'] = result
        return context

    def post(self, request, *args, **kwargs):
        form = TDEEForm(request.POST)
        result = None

        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # Gender constant
            gender_constant = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]

            # TDEE calculation formula
            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_constant) * activity_multiplier

        return render(request, self.template_name, {'form': form, 'result': result})


# WeeklyCaloriesView
class WeeklyCaloriesView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get meals from the last 7 days
        start_of_week = now() - timedelta(days=7)
        meals = Meal.objects.filter(user=self.request.user, date__gte=start_of_week)

        # Calculate total calorie intake
        total_calories_intake = sum(meal.calories for meal in meals)

        # Calories burned calculation (example logic)
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile and profile.goal == 'lose_weight':
            calories_burned_per_day = 500
        elif profile and profile.goal == 'gain_weight':
            calories_burned_per_day = 200
        else:
            calories_burned_per_day = 300  # Default value for maintaining weight
        total_calories_burned = calories_burned_per_day * 7

        # Context data
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['net_calories'] = total_calories_intake - total_calories_burned
        context['meals'] = meals
        return context


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    """
    Changes here explained below
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
		


class User(AbstractUser):
    pass


# Choices
EXERCISE_TYPE_CHOICES = [
    ('cardio', 'Cardio'),
    ('strength', 'Strength'),
]


#Jornal Entry
class JournalEntry(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now, verbose_name="Date Posted")

    def __str__(self):
        return self.title


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


class Carbs(models.Model):
	name = models.TextField(max_length=50)
	gfat = models.PositiveIntegerField(default=0)
	gcarb = models.PositiveIntegerField(default=0)
	gprotein = models.PositiveIntegerField(default=0)


class Fats(models.Model):
	name = models.TextField(max_length=50)
	gfat = models.PositiveIntegerField(default=0)
	gcarb = models.PositiveIntegerField(default=0)
	gprotein = models.PositiveIntegerField(default=0)


class Proteins(models.Model):
	name = models.TextField(max_length=50)
	gfat = models.PositiveIntegerField(default=0)
	gcarb = models.PositiveIntegerField(default=0)
	gprotein = models.PositiveIntegerField(default=0)


class Drinks(models.Model):
	name = models.TextField(max_length=50)
	gfat = models.PositiveIntegerField(default=0)
	gcarb = models.PositiveIntegerField(default=0)
	gprotein = models.PositiveIntegerField(default=0)

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


#TDEE
class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee")
    calories = models.PositiveIntegerField(default=0, verbose_name="Calories")
    date = models.DateField(auto_now_add=True, verbose_name="Date Recorded")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal"


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
