from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.timezone import now, timedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meal, Exercise, Weekly, TDEE, UserProfile, JournalEntry
from .forms import MealForm, TDEEForm, UserProfileForm, JournalEntryForm, UserUpdateForm, ProfileUpdateForm


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


@login_required
def profile(request):
    """
    View for displaying and updating the user profile.
    """
    if request.method == 'POST':
        # Bind forms with POST data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # Save updated user and profile
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to prevent re-posting the form
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        # Populate forms with the current user's data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)



# ========== Meal Management ==========
@login_required
def singlemeal(request):
    """Create and view single meals."""
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.mealcreator = request.user
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



# Journal Entry Views

class JournalListView(LoginRequiredMixin, ListView):
    """View to list all journal entries."""
    model = JournalEntry
    template_name = 'dietapp/journal_list.html'
    context_object_name = 'journals'
    paginate_by = 5

    def get_queryset(self):
        """Return only journal entries created by the logged-in user."""
        return JournalEntry.objects.filter(author=self.request.user).order_by('-date_posted')


class JournalDetailView(LoginRequiredMixin, DetailView):
    """View to display a single journal entry."""
    model = JournalEntry
    template_name = 'dietapp/journal_detail.html'
    context_object_name = 'journal'


class JournalCreateView(LoginRequiredMixin, CreateView):
    """View to create a new journal entry."""
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_form.html'

    def form_valid(self, form):
        """Set the author of the journal entry to the logged-in user."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing journal entry."""
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_form.html'

    def test_func(self):
        """Ensure the user updating the journal entry is the author."""
        journal = self.get_object()
        return self.request.user == journal.author


class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a journal entry."""
    model = JournalEntry
    template_name = 'dietapp/journal_confirm_delete.html'
    success_url = reverse_lazy('dietapp-home')

    def test_func(self):
        """Ensure the user deleting the journal entry is the author."""
        journal = self.get_object()
        return self.request.user == journal.author


@login_required
def about(request):
    """Static About Page."""
    return render(request, 'dietapp/about.html')


@login_required
def contact(request):
    """Static Contact Page."""
    return render(request, 'dietapp/contact.html')



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


@method_decorator(login_required, name='dispatch')
class TDEEView(TemplateView):
    template_name = "dietapp/tdee.html"

    def get(self, request, *args, **kwargs):
        form = TDEEForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = TDEEForm(request.POST)
        result = None

        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = int(form.cleaned_data['activity_level'])

            # Gender value adjustment: 5 for male, -161 for female
            gender_value = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][activity_level - 1]

            # TDEE formula
            result = ((weight * 10) + (height * 6.25) - (age * 5) + gender_value) * activity_multiplier

        return render(request, self.template_name, {"form": form, "result": result})


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


@method_decorator(login_required, name='dispatch')
class WeeklyCaloriesView(TemplateView):
    template_name = "dietapp/weekly_calories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get meals and exercises for the current week
        week_start = now().date() - timedelta(days=now().date().weekday())
        meals = Meal.objects.filter(user=user, date__date__gte=week_start)
        exercises = Exercise.objects.filter(user=user, date__date__gte=week_start)

        # Calculate totals
        total_calories_intake = sum(meal.calories for meal in meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in exercises)

        # Add to context
        context['meals'] = meals
        context['exercises'] = exercises
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned

        return context


# ========== Utility Functions ==========
@login_required
def weekly(request):
    """
    Manage weekly meal plans, including adding meals to specific days, 
    calculating macros, and displaying weekly data.
    """
    user = request.user

    if request.method == "POST":
        # Handle adding a meal to the weekly plan
        day = request.POST.get("day")
        meal_id = request.POST.get("meal_select")
        
        try:
            meal = Meals.objects.get(id=meal_id, mealcreator=user)
            Weekly.objects.create(day=day, meal=meal, user=user)
            messages.success(request, f"Meal '{meal.name}' added to {day}.")
        except Meals.DoesNotExist:
            messages.error(request, "The selected meal does not exist or is not yours.")
        return redirect('weekly')

    # Handle GET request to display weekly meals
    all_meals = Meals.objects.filter(mealcreator=user)
    weekly_meals = Weekly.objects.filter(user=user)

    # Calculate macros and percentages
    macros = calculate_macros(weekly_meals)
    percentages = calculate_percentage(macros)

    context = {
        "all_meals": all_meals,
        "weekly_meals": weekly_meals,
        "macros": macros,
        "percentages": percentages,
    }
    return render(request, "dietapp/weekly_plan.html", context)


def calculate_macros(weekly_meals):
    """
    Calculate the total and average macros (carbs, fats, proteins, and calories) 
    from the user's weekly meals.
    """
    total_fat = 0
    total_carb = 0
    total_protein = 0
    total_calories = 0

    for entry in weekly_meals:
        total_fat += entry.meal.totalfat
        total_carb += entry.meal.totalcarb
        total_protein += entry.meal.totalprotein
        total_calories += entry.meal.calories

    average_fat = round(total_fat / 7, 2) if weekly_meals else 0
    average_carb = round(total_carb / 7, 2) if weekly_meals else 0
    average_protein = round(total_protein / 7, 2) if weekly_meals else 0
    average_calories = round(total_calories / 7, 2) if weekly_meals else 0

    return {
        "average_fat": average_fat,
        "average_carb": average_carb,
        "average_protein": average_protein,
        "average_calories": average_calories,
    }


def calculate_percentage(macros):
    """
    Calculate the percentage of calories coming from carbs, fats, and proteins.
    """
    if not macros["average_calories"]:
        return {"fat": 0, "carb": 0, "protein": 0}

    calories_from_fat = macros["average_fat"] * 9
    calories_from_carb = macros["average_carb"] * 4
    calories_from_protein = macros["average_protein"] * 4
    total_calories = macros["average_calories"]

    fat_percentage = round((calories_from_fat / total_calories) * 100, 2)
    carb_percentage = round((calories_from_carb / total_calories) * 100, 2)
    protein_percentage = round((calories_from_protein / total_calories) * 100, 2)

    return {
        "fat": fat_percentage,
        "carb": carb_percentage,
        "protein": protein_percentage,
    }
