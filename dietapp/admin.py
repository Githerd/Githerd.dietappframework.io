from django.contrib import admin
from .models import (
    Meal, Carbs, Drinks, Fats, Vitamin, Proteins,
    User, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE
)

# Register all models in a single call for better clarity
models_to_register = [
    User, Carbs, Fats, Proteins, Drinks, Meal, Exercise,
 Weekly, TDEE, JournalEntry, Vitamin, UserProfile, Mineral, Message
]

# Register models in the admin panel
for model in models_to_register:
    admin.site.register(model)
