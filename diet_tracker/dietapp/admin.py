from django.contrib import admin
from .models import UserProfile, Meal, Exercise, Healthdata, TDEE, Weekly

admin.site.register(UserProfile)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(Healthdata)
admin.site.register(TDEE)
admin.site.register(Weekly)
