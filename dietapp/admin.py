from django.contrib import admin
from .models import Meal, Exercise, HealthData, TDEE, Weekly, Message, JournalEntry


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'calories', 'protein', 'carbs', 'fat', 'date']
    search_fields = ['name', 'user__username']
    list_filter = ['date', 'user']
    ordering = ['-date']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'type', 'duration', 'calories_burned', 'date']
    search_fields = ['name', 'user__username']
    list_filter = ['type', 'date']
    ordering = ['-date']


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'height', 'calories_intake', 'calories_burned', 'date']
    search_fields = ['user__username']
    list_filter = ['date']
    ordering = ['-date']


@admin.register(TDEE)
class TDEEAdmin(admin.ModelAdmin):
    list_display = ['user', 'calories', 'date']
    search_fields = ['user__username']
    list_filter = ['date']
    ordering = ['-date']


@admin.register(Weekly)
class WeeklyAdmin(admin.ModelAdmin):
    list_display = ['meal', 'day', 'user']
    search_fields = ['meal__name', 'user__username']
    list_filter = ['day']
    ordering = ['day']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']
    list_filter = ['timestamp']
    ordering = ['-timestamp']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted']
    search_fields = ['title', 'author__username']
    list_filter = ['date_posted']
    ordering = ['-date_posted']
