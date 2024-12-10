from django.contrib import admin
from .models import (
    UserProfile,
    Meal,
    Weekly,
    Vitamin,
    Mineral,
    Exercise,
    TDEE,
    JournalEntry,
    Message,
)

models_to_register = [
    UserProfile,
    Meal,
    Weekly,
    Vitamin,
    Mineral,
    Exercise,
    TDEE,
    JournalEntry,
    Message,
]

# Register all models
for model in models_to_register:
    admin.site.register(model)
