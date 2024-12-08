from django.contrib import admin
from .models import Meal, Exercise, UserProfile, HealthData


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Meal model.
    """
    list_display = ('name', 'user', 'calories', 'date')
    search_fields = ('name', 'user__username')
    list_filter = ('date', 'user')
    ordering = ('-date',)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Exercise model.
    """
    list_display = ('name', 'user', 'calories_burned', 'duration', 'date')
    search_fields = ('name', 'user__username')
    list_filter = ('date', 'user')
    ordering = ('-date',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfile model.
    """
    list_display = ('user', 'age', 'weight', 'height', 'dietary_preferences')
    search_fields = ('user__username', 'dietary_preferences')
    list_filter = ('age', 'weight', 'height')


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for the HealthData model.
    """
    list_display = ('user', 'weight', 'height', 'age', 'calories_intake', 'calories_burned', 'date')
    search_fields = ('user__username',)
    list_filter = ('date', 'weight', 'calories_intake', 'calories_burned')
    ordering = ('-date',)
