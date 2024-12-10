from django.contrib import admin
from .models import (
    Meal, Carbs, Drinks, Fats, Vitamins, Proteins,
    User, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData, Profile
)

# Register your models
admin.site.register(User)
admin.site.register(Carbs)
admin.site.register(Fats)
admin.site.register(Proteins)
admin.site.register(Drinks)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(HealthData)
admin.site.register(Weekly)
admin.site.register(TDEE)
admin.site.register(JournalEntry)
admin.site.register(Profile)
