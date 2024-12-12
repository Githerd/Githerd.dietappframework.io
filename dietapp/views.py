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
from django.db.models import Sum, F
from .models import Meal, Exercise, Weekly, JournalEntry, Profile
from .utils import calculate_tdee, calculate_weekly_totals, user_directory_path
from . models import Meal, Vitamin, Mineral, Exercise, Weekly, JournalEntry, User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# ========== Journal Views ==========
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
    template_name = 'dietapp/journal_form.html'

    def form_valid(self, form):
        """Set the author of the journal entry to the logged-in user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing journal entry."""
    model = JournalEntry
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

# ========== TDEE Calculation ==========
@method_decorator(login_required, name='dispatch')
class TDEEView(TemplateView):
    template_name = "dietapp/tdee.html"

    def post(self, request, *args, **kwargs):
        form = TDEEForm(request.POST)
        result = None

        if form.is_valid():
            result = calculate_tdee(
                form.cleaned_data['weight'],
                form.cleaned_data['height'],
                form.cleaned_data['age'],
                form.cleaned_data['gender'],
                form.cleaned_data['activity_level']
            )

        return render(request, self.template_name, {"form": form, "result": result})


# ========== Static Pages ==========
@login_required
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'dietapp/home.html', context)

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
    meals = Meal.objects.filter(mealcreator=request.user).select_related('mealcreator')
    exercises = Exercise.objects.filter(user=request.user).select_related('user')
    weekly_plan = Weekly.objects.filter(user=request.user).select_related('meal', 'user')

    context = {
        'meals': meals,
        'exercises': exercises,
        'weekly_plan': weekly_plan,
    }
    return render(request, 'dietapp/dashboard.html', context)

# ========== Profile Management ==========
@login_required
def profile(request):
    """View for displaying and updating the user profile."""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'dietapp/profile.html', context)

# ========== Meal Management ==========
@login_required
def singlemeal(request):
    """Create and view single meals."""
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['calories'] < 0:
                messages.error(request, "Calories cannot be negative.")
            else:
                meal = form.save(commit=False)
                meal.mealcreator = request.user
                meal.save()
                messages.success(request, "Meal successfully added!")
                return redirect('singlemeal')
    else:
        form = MealForm()

    meals = Meal.objects.filter(mealcreator=request.user)
    context = {'form': form, 'meals': meals}
    return render(request, "dietapp/single_meal.html", context)

@login_required
def deletemeal(request, meal_id):
    """Delete a specific meal."""
    meal = get_object_or_404(Meal, id=meal_id)
    if meal.mealcreator != request.user:
        messages.error(request, "You do not have permission to delete this meal.")
        return redirect('singlemeal')
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


# ========== Weekly Meal Planning ==========
@login_required
def weekly_plan(request):
    """Create and manage a weekly meal plan."""
    if request.method == "POST":
        day = request.POST.get('day')
        meal_id = request.POST.get('meal_select')

        if not day or not meal_id:
            messages.error(request, "Both day and meal selection are required.")
        else:
            try:
                meal = Meal.objects.get(id=meal_id, mealcreator=request.user)
                Weekly.objects.create(user=request.user, meal=meal, day=day)
                messages.success(request, f"Meal added to {day}'s plan!")
            except Meal.DoesNotExist:
                messages.error(request, "Selected meal does not exist or does not belong to you.")

        return redirect('weekly-plan')

    meals = Meal.objects.filter(mealcreator=request.user)
    weekly_meals = Weekly.objects.filter(user=request.user)
    context = {'meals': meals, 'weekly_meals': weekly_meals}
    return render(request, 'dietapp/weekly_plan.html', context)


# ========== tdee calculator ==========
def tdee(request):
    context = {
        "calories": "2000"
    }
    return render(request, "dietapp/tdee_calculate.html", context)

def singlemeal(request):

    if request.method == "GET":

        # Query that user's meals
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(mealcreator = request.user)
            no_user = False
        else:
            all_meals = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user
        }

        return render(request, "dietapp/singlemeal.html", context)

    else:

        # Get inputs from form
        mealtitle = request.POST["mealtitle"]
        carb_source = request.POST.get("carbsource")
        carb_grams = request.POST.get("carbgrams")
        fat_source = request.POST.get("fatsource")
        fat_grams = request.POST.get("fatgrams")
        protein_source = request.POST.get("proteinsource")
        protein_grams = request.POST.get("proteingrams")
        drink_source = request.POST.get("drinksource")
        drinkmililiters = request.POST.get("drinkmililiters")
        #print(carb_grams)

        # Default quantities are 0
        if not carb_grams:
            carb_grams = 0
        if not fat_grams:
            fat_grams = 0
        if not protein_grams:
            protein_grams = 0
        if not drinkmililiters:
            drinkmililiters = 0
        #print(carb_grams)

        # Prepare variables to save in meal model
        mealcreator = request.user
        name = mealtitle

        # Get foods from models
        mealcarb = Carbs.objects.get(id=carb_source)
        mealfat = Fats.objects.get(id=fat_source)
        mealprotein = Proteins.objects.get(id=protein_source)
        mealdrink = Drinks.objects.get(id=drink_source)

        # Calculate total meal macros
        totalcarbs = round((int(getattr(mealcarb, "gcarb")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gcarb")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gcarb")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gcarb")) / 100 * int(drinkmililiters)))
        totalfats = round((int(getattr(mealcarb, "gfat")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gfat")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gfat")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gfat")) / 100 * int(drinkmililiters)))
        totalproteins = round((int(getattr(mealcarb, "gprotein")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gprotein")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gprotein")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gprotein")) / 100 * int(drinkmililiters)))
        #print(totalcarbs, totalfats, totalproteins)

        # Calculate total calories
        calories = (totalcarbs * 4) + (totalfats * 9) + (totalproteins * 4)
        #print(calories)

        # Make ingredients list
        carb_name = (getattr(mealcarb, "name"))
        fat_name = (getattr(mealfat, "name"))
        protein_name = (getattr(mealprotein, "name"))
        drink_name = (getattr(mealdrink, "name"))

        # Check for empty inputs
        if carb_name != "No Carb Source":
            there_is_carb = True
        else:
            there_is_carb = False
        if fat_name != "No Fat Source":
            there_is_fat = True
        else:
            there_is_fat = False
        if protein_name != "No Protein Source":
            there_is_protein = True
        else:
            there_is_protein = False
        if drink_name != "No Drink":
            there_is_drink = True
        else:
            there_is_drink = False

        # Format string quantity and macro name
        if there_is_carb:
            carb_ingredient = f'{carb_grams}g of {carb_name} '
        else:
            carb_ingredient = ""

        if there_is_fat:
            fat_ingredient = f'| {fat_grams}g of {fat_name} '
        else:
            fat_ingredient = ""

        if there_is_protein:
            protein_ingredient = f'| {protein_grams}g of {protein_name} '
        else:
            protein_ingredient = ""

        if there_is_drink:
            drink_ingredient = f'| {drinkmililiters}ml of {drink_name}'
        else:
            drink_ingredient = ""

        # Full ingredients list
        ingredients_list = f"{carb_ingredient}{fat_ingredient}{protein_ingredient}{drink_ingredient}"
        #print(ingredients_list)

        # Save meal
        meal = Meals(name = name, totalcarb = totalcarbs, totalfat = totalfats, totalprotein = totalproteins, calories = calories, mealcreator = mealcreator, ingredients = ingredients_list)
        meal.save()

        # Query that user's meals
        all_meals = Meals.objects.filter(mealcreator = request.user)
        #print(all_meals)

        context = {
            "all_meals": all_meals
        }

        return render(request, "dietapp/single_meal.html", context)

# ========== Register ==========
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mealplanmaker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mealplanmaker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mealplanmaker/register.html")

    
