from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, MealForm
from .models import Meal, UserProfile, Message, Exercise, TDEE
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JournalEntryForm
from .models import JournalEntry


# Basic Views

def home(request):
    """
    Renders the home page.
    """
    return HttpResponse('<h1>DietApp Home</h1>')


def about(request):
    """
    Renders the about page.
    """
    return HttpResponse('<h1>About DietApp</h1>')


def contact(request):
    """
    Renders the contact page.
    """
    return HttpResponse('<h1>Contact DietApp</h1>')


# User Management

def register(request):
    """
    Handles user registration and profile creation.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to DietApp.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()
    
    return render(request, 'dietapp/register.html', {'form': form, 'profile_form': profile_form})


# Dashboard

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'dietapp/dashboard.html', {'user': user_profile})


# Meal Management

@login_required
def journal_create(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('journal-list')
    else:
        form = JournalEntryForm()
    return render(request, 'journal_entry_form.html', {'form': form})

@login_required
def journal_update(request, pk):
    journal = get_object_or_404(JournalEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('journal-detail', pk=journal.pk)
    else:
        form = JournalEntryForm(instance=journal)
    return render(request, 'journal_entry_form.html', {'form': form})

@login_required
def journal_delete(request, pk):
    journal = get_object_or_404(JournalEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        journal.delete()
        return redirect('journal-list')
    return render(request, 'journal_confirm_delete.html', {'object': journal})


def submit_user_details(request):
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        meals = request.POST['meals']
        calories_consumed = request.POST['calories_consumed']
        calories_burned = request.POST['calories_burned']

        user_profile = UserProfile(
            user=request.user,
            name=name,
            age=age,
            height=height,
            weight=weight,
            meals=meals,
            calories_consumed=calories_consumed,
            calories_burned=calories_burned,
        )
        user_profile.save()
        return redirect('dashboard')
    return render(request, 'dietapp/home.html')
    

class TDEEView(TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tdee = TDEE.objects.filter(user=self.request.user).first()
        context['tdee'] = tdee.calories if tdee else 0
        return context

class WeeklyCaloriesView(TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        weekly_meals = Meal.objects.filter(user=user, date__week=timezone.now().isocalendar()[1])
        weekly_exercises = Exercise.objects.filter(user=user, date__week=timezone.now().isocalendar()[1])
        total_calories_intake = sum(meal.calories for meal in weekly_meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)
        context.update({
            'total_calories_intake': total_calories_intake,
            'total_calories_burned': total_calories_burned,
        })
        return context


def send_message(request):
    if request.method == "POST":
        receiver_username = request.POST['receiver']
        content = request.POST['content']
        try:
            receiver = User.objects.get(username=receiver_username)
            message = Message(sender=request.user, receiver=receiver, content=content)
            message.save()
            return redirect('inbox')  # Redirect to inbox after sending
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'User not found'})
    return render(request, 'messaging/send_message.html')


def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})


def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'messages': messages})
