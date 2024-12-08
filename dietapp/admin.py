from django.contrib import admin
from .models import User, UserProfile, Meal, Exercise, HealthData, TDEE, Weekly, Message, JournalEntry


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(HealthData)
admin.site.register(TDEE)
admin.site.register(Weekly)
admin.site.register(Message)
admin.site.register(JournalEntry)
