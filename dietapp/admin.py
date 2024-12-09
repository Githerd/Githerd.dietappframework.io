from django.contrib import admin
from .models import Meal, Exercise, HealthData, TDEE, Weekly, Message, JournalEntry

# Register your models here
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(HealthData)
admin.site.register(TDEE)
admin.site.register(Weekly)
admin.site.register(Message)
admin.site.register(JournalEntry)



