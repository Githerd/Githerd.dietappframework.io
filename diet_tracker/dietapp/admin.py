from django.contrib import admin
from .models import Meal, UserProfile, Exercise, Healthdata

admin.site.register(Meal)
admin.site.register(UserProfile)
admin.site.register(Exercise)
admin.site.register(Healthdata)
