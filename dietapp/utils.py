# utils.py
from django.utils.timezone import now

def calculate_tdee(weight, height, age, gender, activity_level):
    gender_value = 5 if gender == "male" else -161
    activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]
    return ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier
