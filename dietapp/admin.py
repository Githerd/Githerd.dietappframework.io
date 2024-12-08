from django.contrib import admin
from .models import User, UserProfile, Profile, DietApp, Exercise, HealthData, TDEE, Weekly, Message, JournalEntry
from dietapp.models import Meal  

admin.site.register(UserProfile)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(HealthData)
admin.site.register(TDEE)
admin.site.register(Weekly)
admin.site.register(Message)
