from django.contrib import admin
from .models import User, UserProfile, Profile, DietApp, Meal, Exercise, HealthData, TDEE, Weekly, Message, JournalEntry


# Register the custom User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined']
    search_fields = ['username', 'email']
    list_filter = ['date_joined', 'is_active']
    ordering = ['-date_joined']


# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'height', 'weight']
    search_fields = ['user__username']
    list_filter = ['age']


# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    search_fields = ['user__username']


# Register the DietApp model
@admin.register(DietApp)
class DietAppAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_level', 'goal', 'created_at']
    list_filter = ['activity_level', 'goal']
    search_fields = ['user__username', 'goal']


# Register the Meal model
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'calories', 'date']
    list_filter = ['date']
    search_fields = ['name', 'user__username']


# Register the Exercise model
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'type', 'duration', 'calories_burned', 'date']
    list_filter = ['type', 'date']
    search_fields = ['name', 'user__username']


# Register the HealthData model
@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'height', 'calories_intake', 'calories_burned', 'date']
    search_fields = ['user__username']
    list_filter = ['date']


# Register the TDEE model
@admin.register(TDEE)
class TDEEAdmin(admin.ModelAdmin):
    list_display = ['user', 'calories', 'date']
    search_fields = ['user__username']
    list_filter = ['date']


# Register the Weekly model
@admin.register(Weekly)
class WeeklyAdmin(admin.ModelAdmin):
    list_display = ['meal', 'day', 'mealuser']
    search_fields = ['meal__name', 'mealuser__username']
    list_filter = ['day']


# Register the Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']
    list_filter = ['timestamp']


# Register the JournalEntry model
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted']
    search_fields = ['title', 'author__username']
    list_filter = ['date_posted']
