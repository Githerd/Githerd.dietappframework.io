from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Meal, Exercise, TDEE
from datetime import datetime, timedelta

# TDEE Calculator View
@method_decorator(login_required, name='dispatch')
class TDEEView(TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tdee_entry = TDEE.objects.filter(user=self.request.user).order_by('-date').first()
        context['tdee'] = tdee_entry.calories if tdee_entry else 0
        return context

    def post(self, request, *args, **kwargs):
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        activity_level = float(request.POST.get('activity_level'))

        gender_modifier = 5 if gender == "male" else -161
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + gender_modifier
        tdee = bmr * activity_level

        # Save TDEE to database
        TDEE.objects.create(user=request.user, calories=int(tdee), date=datetime.now())

        return render(request, self.template_name, {'tdee': int(tdee)})


# Weekly Calories View
@method_decorator(login_required, name='dispatch')
class WeeklyCaloriesView(TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get meals and exercises for the current week
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
        weekly_meals = Meal.objects.filter(user=user, date__gte=start_of_week)
        weekly_exercises = Exercise.objects.filter(user=user, date__gte=start_of_week)

        # Calculate total intake and burn
        total_calories_intake = sum(meal.calories for meal in weekly_meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)

        context['weekly_meals'] = weekly_meals
        context['weekly_exercises'] = weekly_exercises
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['net_calories'] = total_calories_intake - total_calories_burned

        return context
