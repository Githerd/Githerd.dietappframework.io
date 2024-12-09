from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import User, Meals, Weekly, JournalEntry, TDEE, Message, UserProfile
from .forms import RegisterForm, UserProfileForm, MealForm, JournalEntryForm, TDEEForm

# ========== User Management ==========
def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to DietApp.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'dietapp/register.html', {'form': form, 'profile_form': profile_form})


def login_view(request):
    """Log in the user."""
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "dietapp/login.html")


@login_required
def logout_view(request):
    """Log out the user."""
    logout(request)
    return redirect('login')


# ========== Dashboard ==========
@login_required
def dashboard(request):
    """Display the user's dashboard."""
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'dietapp/dashboard.html', {'user': user_profile})


# ========== TDEE Calculator ==========
def tdee_calculate(request):
    """TDEE Calculation."""
    result = None
    if request.method == 'POST':
        form = TDEEForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']
            gender_value = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]
            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier
    else:
        form = TDEEForm()
    return render(request, "dietapp/meal_plan.html", {"form": form, "result": result})


# ========== Journal Management ==========
class JournalListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'dietapp/journal_list.html'
    context_object_name = 'journals'


class JournalDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = 'dietapp/journal_entry_detail.html'


class JournalCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_entry_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_entry_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author


class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JournalEntry
    template_name = 'dietapp/journal_confirm_delete.html'
    success_url = reverse_lazy('journal-list')

    def test_func(self):
        return self.request.user == self.get_object().author


# ========== Meal Management ==========
@login_required
def single_meal(request):
    """Manage single meals."""
    if request.method == "GET":
        meals = Meals.objects.filter(mealcreator=request.user)
        return render(request, "dietapp/single_meal.html", {"meals": meals})

    if request.method == "POST":
        # Logic to add meals
        ...
        return redirect('single_meal')


# ========== Weekly Planning ==========
@login_required
def weekly_plan(request):
    """Manage weekly meal plans."""
    if request.method == "GET":
        meals = Meals.objects.filter(mealcreator=request.user)
        weekly_meals = Weekly.objects.filter(mealuser=request.user)
        macros = calculate_macros(weekly_meals)
        percentages = calculate_percentage(macros)
        context = {"meals": meals, "weekly_meals": weekly_meals, "macros": macros, "percentages": percentages}
        return render(request, "dietapp/weekly_plan.html", context)

    if request.method == "POST":
        # Logic to handle weekly meal addition
        ...
        return redirect('weekly_plan')
