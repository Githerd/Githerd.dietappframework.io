from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Meal, Carbs, Drinks, Fats, Meals, Vitamins, Proteins, User, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData, Profile
from .forms import TDEEForm, MealForm, UserProfileForm, TDEEForm, JournalEntryForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm, RegisterForm, MealForm, CustomPasswordResetForm, HealthDataForm, WeeklyCaloriesView, TDEEView, TDEEForm, JournalEntryForm, WeeklyMealForm, ExerciseForm, MineralForm, VitaminForm


# ========== Static Pages ==========
def about(request):
    """Render the About page."""
    return render(request, 'dietapp/about.html')


def contact(request):
    """Render the Contact page."""
    return render(request, 'dietapp/contact.html')


# ========== Dashboard ==========
@login_required
def dashboard(request):
    """Render the dashboard with user details and health summary."""
    meals = Meals.objects.filter(mealcreator=request.user)
    exercises = Exercise.objects.filter(user=request.user)
    weekly_plan = Weekly.objects.filter(user=request.user)

    context = {
        'meals': meals,
        'exercises': exercises,
        'weekly_plan': weekly_plan,
    }
    return render(request, 'dietapp/dashboard.html', context)


# ========== Meal Management ==========
@login_required
def singlemeal(request):
    """Create and view single meals."""
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, "Meal successfully added!")
            return redirect('singlemeal')
    else:
        form = MealForm()

    meals = Meals.objects.filter(mealcreator=request.user)
    context = {'form': form, 'meals': meals}
    return render(request, "dietapp/single_meal.html", context)


@login_required
def deletemeal(request, meal_id):
    """Delete a specific meal."""
    meal = get_object_or_404(Meals, id=meal_id, mealcreator=request.user)
    meal.delete()
    messages.success(request, "Meal successfully deleted!")
    return redirect('singlemeal')


# ========== Exercise Management ==========
@login_required
def add_exercise(request):
    """Add an exercise entry."""
    if request.method == "POST":
        name = request.POST.get('name')
        type = request.POST.get('type')
        duration = request.POST.get('duration')
        calories_burned = request.POST.get('calories_burned')

        Exercise.objects.create(
            user=request.user,
            name=name,
            type=type,
            duration=duration,
            calories_burned=calories_burned,
        )
        messages.success(request, "Exercise added successfully!")
        return redirect('dashboard')
    return render(request, "dietapp/add_exercise.html")


# ========== TDEE Calculation ==========
def tdee_calculate(request):
    """TDEE Calculation."""
    result = None
    if request.method == "POST":
        form = TDEEForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # Gender constant: 5 for male, -161 for female
            gender_value = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]

            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier

            # Save TDEE for user
            TDEE.objects.create(user=request.user, calories=result)

            messages.success(request, f"Your TDEE is {result:.0f} kcal.")
    else:
        form = TDEEForm()

    return render(request, "dietapp/tdee_calculate.html", {"form": form, "result": result})


# ========== Weekly Meal Planning ==========
@login_required
def weekly_plan(request):
    """Create and manage a weekly meal plan."""
    if request.method == "POST":
        day = request.POST.get('day')
        meal_id = request.POST.get('meal_select')
        meal = get_object_or_404(Meals, id=meal_id)

        Weekly.objects.create(user=request.user, meal=meal, day=day)
        messages.success(request, f"Meal added to {day}'s plan!")
        return redirect('weekly_plan')

    meals = Meals.objects.filter(mealcreator=request.user)
    weekly_meals = Weekly.objects.filter(user=request.user)

    context = {
        'meals': meals,
        'weekly_meals': weekly_meals,
    }
    return render(request, 'dietapp/weekly_plan.html', context)


@login_required
def deletefromplan(request, plan_id):
    """Delete a meal from the weekly plan."""
    weekly_entry = get_object_or_404(Weekly, id=plan_id, user=request.user)
    weekly_entry.delete()
    messages.success(request, "Meal removed from the weekly plan.")
    return redirect('weekly_plan')


# ========== Utility Functions ==========
def calculate_macros(weekly_meals):
    """Calculate macros for weekly meals."""
    total_carbs = sum(meal.meal.totalcarb for meal in weekly_meals)
    total_fats = sum(meal.meal.totalfat for meal in weekly_meals)
    total_proteins = sum(meal.meal.totalprotein for meal in weekly_meals)
    total_calories = sum(meal.meal.calories for meal in weekly_meals)

    macros = {
        "carbs": total_carbs,
        "fats": total_fats,
        "proteins": total_proteins,
        "calories": total_calories,
    }
    return macros
