from django.contrib import admin
from .models import (
    Meal, Carbs, Drinks, Fats, Vitamin, Proteins,
    User, Minerals, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData, Profile
)

# Register all models in a single call for better clarity
models_to_register = [
    User, Carbs, Fats, Proteins, Drinks, Meal, Exercise,
    HealthData, Weekly, TDEE, JournalEntry, Profile, Vitamin, UserProfile, Minerals
]

# Register models in the admin panel
for model in models_to_register:
    admin.site.register(model)
