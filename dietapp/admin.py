from django.contrib import admin
from .models import (
    User,
    Carbs,
    Fats,
    Proteins,
    Drinks,
    Meal,
    Exercise,
    HealthData,
    Weekly,
    Message,
    TDEE,
    JournalEntry
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
admin.site.register(Message)
admin.site.register(TDEE)
admin.site.register(JournalEntry)
