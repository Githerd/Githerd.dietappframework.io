from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TDEE, Meal, Exercise
from django.utils.timezone import now

# ========== TDEE View ==========
class TDEEView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tdee = TDEE.objects.filter(user=self.request.user).order_by('-date').first()

        if tdee:
            context['tdee'] = tdee.calories
        else:
            context['tdee'] = 0  # Default value if no TDEE record exists

        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission for calculating TDEE
        weight = float(request.POST.get('weight', 0))
        height = float(request.POST.get('height', 0))
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender', 'male')
        activity_level = int(request.POST.get('activity_level', 1))

        # Gender constant: 5 for male, -161 for female
        gender_constant = 5 if gender == 'male' else -161
        activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
        multiplier = activity_multipliers[activity_level - 1]

        # TDEE calculation
        tdee_calories = ((10 * weight) + (6.25 * height) - (5 * age) + gender_constant) * multiplier

        # Save the TDEE result
        TDEE.objects.create(user=request.user, calories=tdee_calories, date=now())

        return render(request, self.template_name, {'tdee': tdee_calories})


# ========== Weekly Calories View ==========
class WeeklyCaloriesView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get meals and exercises for the current week
        current_week = now().isocalendar()[1]
        weekly_meals = Meal.objects.filter(user=self.request.user, date__week=current_week)
        weekly_exercises = Exercise.objects.filter(user=self.request.user, date__week=current_week)

        # Calculate total calories intake and burned
        total_calories_intake = sum(meal.calories for meal in weekly_meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)

        # Pass data to the context
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['net_calories'] = total_calories_intake - total_calories_burned
        context['weekly_meals'] = weekly_meals
        context['weekly_exercises'] = weekly_exercises

        return context
