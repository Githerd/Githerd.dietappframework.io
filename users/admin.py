from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'weight', 'height', 'bmi')  # Display additional fields
    search_fields = ('user__username', 'user__email')  # Enable search by username or email
    list_filter = ('age',)  # Add filtering by age
    readonly_fields = ('bmi',)  # Make BMI read-only

    def bmi(self, obj):
        return obj.bmi
    bmi.short_description = 'BMI' 
