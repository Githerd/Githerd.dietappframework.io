# utils.py
from django.utils.timezone import now

def calculate_tdee(weight, height, age, gender, activity_level):
    gender_value = 5 if gender == "male" else -161
    activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]
    return ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier



def calculate_weekly_totals(user, week_number):
    weekly_meals = Meal.objects.filter(user=user, date__week=week_number)
    weekly_exercises = Exercise.objects.filter(user=user, date__week=week_number)
    
    total_calories_intake = sum(meal.calories for meal in weekly_meals)
    total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)

    return total_calories_intake, total_calories_burned



def user_directory_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'
