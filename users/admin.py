from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


# Extend UserAdmin to include custom fields if needed
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# Customize the User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    # Adding custom profile fields to the user list
    def profile_bio(self, instance):
        return instance.profile.bio if hasattr(instance, 'profile') else ''
    profile_bio.short_description = 'Profile Bio'


# Unregister the default User Admin
admin.site.unregister(User)

# Register the Custom User Admin
admin.site.register(User, CustomUserAdmin)


# Register the Profile Model Separately
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date')
    search_fields = ('user__username', 'bio', 'location')
    list_filter = ('location', 'birth_date')
