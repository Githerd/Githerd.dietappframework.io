from django.contrib import admin
from .models import UserProfile, Meal, Exercise, HealthData, TDEE, Weekly, Message

admin.site.register(UserProfile)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(HealthData)
admin.site.register(TDEE)
admin.site.register(Weekly)
admin.site.register(Message)
