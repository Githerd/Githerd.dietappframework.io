from django.shortcuts import render, redirect
from django.contrib import messages  # For flash messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TDEEForm
from .models import Weekly, Meals

# Helper function for calculating total calories
def calculate_total_calories(weekly_meals):
    """
    Calculate total calories from weekly meal entries.
    """
    return sum(entry.meal.calories for entry in weekly_meals)


class TDEEView(View):
    """
    Handles GET and POST requests for TDEE calculation.
    """
    def get(self, request):
        form = TDEEForm()
        return render(request, 'dietapp/tdee.html', {'form': form})

    def post(self, request):
        form = TDEEForm(request.POST)
        tdee_result = None
        if form.is_valid():
            # Extract form data
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # TDEE calculation
            gender_factor = 5 if gender == "male" else -161
            activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
            activity_multiplier = activity_multipliers[int(activity_level) - 1]
            tdee_result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_factor) * activity_multiplier

        return render(request, 'dietapp/tdee.html', {'form': form, 'tdee_result': tdee_result})


@method_decorator(login_required, name='dispatch')
class WeeklyCaloriesView(View):
    """
    Handles weekly calories tracking for logged-in users.
    """
    def get(self, request):
        user = request.user
        weekly_meals = Weekly.objects.filter(user=user)
        total_calories = calculate_total_calories(weekly_meals)
        return render(request, 'dietapp/weekly_calories.html', {
            'weekly_meals': weekly_meals,
            'total_calories': total_calories
        })


def register(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'The account {username} was created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """
    Handles user profile updates.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
