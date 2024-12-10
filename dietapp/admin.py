from django.contrib import admin
from dietapp.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height', 'weight')

# Register all models in a single call for better clarity
models_to_register = [
    UserProfile,
    Meal,
    Weekly,
    Vitamin,
    Mineral,
    Exercise,
    TDEE,
    JournalEntry,
    Message
]

# Register models in the admin panel
for model in models_to_register:
    admin.site.register(model)
