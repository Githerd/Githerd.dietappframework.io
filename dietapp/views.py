from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Meal, Exercise, TDEE
from .forms import TDEEForm
from django.utils.timezone import now


# ========== TDEE View ==========
@method_decorator(login_required, name='dispatch')
class TDEEView(TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TDEEForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TDEEForm(request.POST)
        result = None
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # Gender constant: 5 for male, -161 for female
            gender_value = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]

            # Calculate TDEE
            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier

            # Save TDEE data for the user
            TDEE.objects.update_or_create(
                user=request.user,
                defaults={"calories": round(result)},
            )

        return render(request, self.template_name, {'form': form, 'result': round(result) if result else None})


# ========== Weekly Calories View ==========
@method_decorator(login_required, name='dispatch')
class WeeklyCaloriesView(TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch all meals and exercises for the current week
        weekly_meals = Meal.objects.filter(user=user, date__week=now().isocalendar()[1])
        weekly_exercises = Exercise.objects.filter(user=user, date__week=now().isocalendar()[1])

        # Calculate total intake and burned calories
        total_calories_intake = sum(meal.calories for meal in weekly_meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)

        # Add data to context
        context['weekly_meals'] = weekly_meals
        context['weekly_exercises'] = weekly_exercises
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['net_calories'] = total_calories_intake - total_calories_burned  # Net calorie balance

        return context
