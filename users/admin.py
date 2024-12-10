from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

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
