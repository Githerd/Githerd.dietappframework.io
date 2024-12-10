from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import admin
from .models import UserProfile, Meal, Weekly, Exercise, TDEE, JournalEntry, Vitamin, Mineral


User = get_user_model()

user = User.objects.get(username='example')
user.meals.all()  # Returns all meals related to this user

def clean(self):
    if self.percentage < 0 or self.percentage > 100:
        raise ValidationError("Percentage must be between 0 and 100.")
# Utility function for user file upload paths
def user_directory_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'


# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        default='default.jpg',
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    goal = models.CharField(
        max_length=100,
        choices=[
            ('lose_weight', 'Lose Weight'),
            ('gain_weight', 'Gain Weight'),
            ('maintain_weight', 'Maintain Weight'),
        ],
        default='maintain_weight'
    )

    def clean(self):
        if self.age and (self.age <= 0 or self.age > 150):
            raise ValidationError("Age must be between 1 and 150.")
        if self.height and self.height <= 0:
            raise ValidationError("Height must be a positive value.")
        if self.weight and self.weight <= 0:
            raise ValidationError("Weight must be a positive value.")

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def bmi(self):
        if self.height and self.weight:
            return round(self.weight / (self.height / 100) ** 2, 2)
        return None


# Meal Model
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Protein (g)")
    carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Carbs (g)")
    fat = models.FloatField(default=0.0, validators=[MinValueValidator(0)], verbose_name="Fat (g)")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})


# Carbs Model
class Carbs(models.Model):
    name = models.CharField(max_length=50)
    gfat = models.PositiveIntegerField(default=0)
    gcarb = models.PositiveIntegerField(default=0)
    gprotein = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# Fats Model
class Fats(models.Model):
    name = models.CharField(max_length=100)
    fat_content = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Fat Content (g)")

    def __str__(self):
        return self.name


# Proteins Model
class Proteins(models.Model):
    name = models.CharField(max_length=50)
    gfat = models.PositiveIntegerField(default=0)
    gcarb = models.PositiveIntegerField(default=0)
    gprotein = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# Drinks Model
class Drinks(models.Model):
    name = models.CharField(max_length=50)
    gfat = models.PositiveIntegerField(default=0)
    gcarb = models.PositiveIntegerField(default=0)
    gprotein = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'date', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('date', 'user')
    ordering = ['-date']
    filter_horizontal = ('vitamins', 'minerals')  # If Many-to-Many is used

@admin.register(Vitamin)
class VitaminAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'meal')
    search_fields = ('name', 'meal__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'timestamp')
    
# Vitamins for Meals
class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


# Minerals for Meals
class Mineral(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="minerals")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


# Weekly Meal Plan
# Weekly Plan
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
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="weekly_meals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_entries")

    class Meta:
        ordering = ['day']
        unique_together = ['day', 'user']  # Prevent duplicate meals on the same day for a user

    def __str__(self):
        return f"{self.meal.name} on {self.day} for {self.user.username}"

    def total_calories_for_week(self):
        return sum(weekly.meal.calories for weekly in self.user.weekly_entries.all())


# Messaging System
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)  # To track read/unread status

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"


# Vitamin and Mineral Validation
class Vitamin(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="vitamins")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def clean(self):
        if not 0 <= self.percentage <= 100:
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"


class Mineral(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="minerals")
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=0)

    def clean(self):
        if not 0 <= self.percentage <= 100:
            raise ValidationError("Percentage must be between 0 and 100.")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) in {self.meal.name}"

# Exercise Model
EXERCISE_TYPE_CHOICES = [
    ('cardio', 'Cardio'),
    ('strength', 'Strength'),
]

class Weekly(models.Model):
    ...
    def total_calories_for_day(self, day):
        meals = self.filter(day=day)
        return sum(meal.meal.calories for meal in meals)
        
class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=EXERCISE_TYPE_CHOICES)
    duration = models.IntegerField(validators=[MinValueValidator(0)], help_text="Duration in minutes")
    calories_burned = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.calories_burned} kcal)"


# Journal Entry Model
class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


# TDEE Model
class TDEE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tdee")
    calories = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"TDEE for {self.user.username}: {self.calories} kcal"


class TDEE(models.Model):
    ...
    def recommended_calories(self, goal):
        if goal == "lose_weight":
            return self.calories - 500
        elif goal == "gain_weight":
            return self.calories + 500
        return self.calories

# Messaging System
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
