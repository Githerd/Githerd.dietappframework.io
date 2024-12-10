from django.contrib import admin
from django.utils.timezone import localtime
from users.models import (
    Profile,
    Meal,
    Weekly,
    Vitamin,
    Mineral,
    Exercise,
    TDEE,
    JournalEntry,
    Message,
)
    
# Custom Admin for Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'weight', 'height', 'bmi')
    search_fields = ('user__username', 'user__email')
    list_filter = ('age',)
    readonly_fields = ('bmi',)
    list_editable = ('age', 'weight', 'height')
    search_help_text = "Search by username or email"

    def bmi(self, obj):
        return obj.bmi
    bmi.short_description = 'BMI'


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


# Custom Admin for Meal
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'calories', 'protein', 'carbs', 'fat', 'date')
    list_filter = ('date', 'protein', 'carbs', 'fat')  # Add macronutrient filtering
    search_fields = ('name', 'user__username')
    inlines = [VitaminInline, MineralInline]
    list_select_related = ('user',)
    list_per_page = 25  # Enable pagination


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


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'formatted_date_posted')  # Use the formatted date
    search_fields = ('title', 'author__username')
    list_filter = ('date_posted', 'author')  # Allow filtering by author
    list_editable = ('title',)  # Allow editing title in the list view
    list_select_related = ('author',)
    list_per_page = 20  # Enable pagination
    search_help_text = "Search by title or author's username"

    def formatted_date_posted(self, obj):
        return localtime(obj.date_posted).strftime('%Y-%m-%d %H:%M:%S')
    formatted_date_posted.admin_order_field = 'date_posted'
    formatted_date_posted.short_description = 'Posted Date'


# Custom Admin for Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_select_related = ('sender', 'receiver')
