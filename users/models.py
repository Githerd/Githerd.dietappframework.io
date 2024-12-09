from django.db import models
from django.contrib.auth.models import User
from PIL import Image


from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now, timedelta
from .forms import TDEEForm
from .models import Profile, Meal


# TDEEView
class TDEEView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TDEEForm()
        result = None

        # Pre-fill the form with user profile data, if available
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile:
            form.initial['weight'] = profile.weight
            form.initial['height'] = profile.height
            form.initial['age'] = getattr(profile, 'age', 30)  # Default to 30 if age is not set

        context['form'] = form
        context['result'] = result
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

            # Gender constant
            gender_constant = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]

            # TDEE calculation formula
            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_constant) * activity_multiplier

        return render(request, self.template_name, {'form': form, 'result': result})


# WeeklyCaloriesView
class WeeklyCaloriesView(LoginRequiredMixin, TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get meals from the last 7 days
        start_of_week = now() - timedelta(days=7)
        meals = Meal.objects.filter(user=self.request.user, date__gte=start_of_week)

        # Calculate total calorie intake
        total_calories_intake = sum(meal.calories for meal in meals)

        # Calories burned calculation (example logic)
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile and profile.goal == 'lose_weight':
            calories_burned_per_day = 500
        elif profile and profile.goal == 'gain_weight':
            calories_burned_per_day = 200
        else:
            calories_burned_per_day = 300  # Default value for maintaining weight
        total_calories_burned = calories_burned_per_day * 7

        # Context data
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['net_calories'] = total_calories_intake - total_calories_burned
        context['meals'] = meals
        return context


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    """
    Changes here explained below
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
