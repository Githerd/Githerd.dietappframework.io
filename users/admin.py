from django.contrib import admin
from .models import User, UserProfile, Profile, DietApp


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
