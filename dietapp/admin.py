from django.contrib import admin
from users.models import Profile
from .models import (
    Meal,
    Weekly,
    Vitamin,
    Mineral,
    Exercise,
    TDEE,
    JournalEntry,
    Message,
)


# Inline Admin for Vitamins and Minerals in Meals
class VitaminInline(admin.TabularInline):
    model = Vitamin
    extra = 1
    verbose_name = "Vitamin"
    verbose_name_plural = "Vitamins"


class MineralInline(admin.TabularInline):
    model = Mineral
    extra = 1
    verbose_name = "Mineral"
    verbose_name_plural = "Minerals"


# Custom Admin for Profile (formerly UserProfile)
@admin.register(Profile)  # Update to use Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height', 'weight')  # Remove 'bmi' if not in Profile
    search_fields = ('user__username',)


# Custom Admin for Meal
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'calories', 'protein', 'carbs', 'fat', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'user__username')
    inlines = [VitaminInline, MineralInline]
    list_select_related = ('user',)


# Custom Admin for Weekly Plan
@admin.register(Weekly)
class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'meal')
    list_filter = ('day',)
    search_fields = ('user__username', 'meal__name')
    list_select_related = ('user', 'meal')


# Custom Admin for Exercise
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'type', 'duration', 'calories_burned', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'name')
    list_select_related = ('user',)


# Custom Admin for TDEE
@admin.register(TDEE)
class TDEEAdmin(admin.ModelAdmin):
    list_display = ('user', 'calories', 'date')
    list_filter = ('date',)
    search_fields = ('user__username',)
    list_select_related = ('user',)


# Custom Admin for JournalEntry
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'author__username')
    list_filter = ('date_posted',)
    list_select_related = ('author',)


# Custom Admin for Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_select_related = ('sender', 'receiver')
