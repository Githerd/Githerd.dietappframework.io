from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm, MealForm
from .models import Meal, UserProfile, Message
from django.contrib.auth.models import User


# Basic Views

def home(request):
    """Renders the home page."""
    return HttpResponse('<h1>DietApp Home</h1>')


def about(request):
    """Renders the about page."""
    return HttpResponse('<h1>About DietApp</h1>')


def contact(request):
    """Renders the contact page."""
    return HttpResponse('<h1>Contact DietApp</h1>')


# User Management

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Dashboard

@login_required
def dashboard(request):
    """Displays the user's dashboard."""
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'dietapp/dashboard.html', {'user_profile': user_profile})


# Meal Management

@login_required
def log_meal(request):
    """Allows the user to log a new meal."""
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Meal logged successfully!')
            return redirect('dashboard')
    else:
        form = MealForm()
    return render(request, 'dietapp/meal_form.html', {'form': form})


@login_required
def meal_detail(request, meal_id):
    """Displays the details of a specific meal."""
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    return render(request, 'dietapp/meal_detail.html', {'meal': meal})


@login_required
def delete_meal(request, meal_id):
    """Handles the deletion of a specific meal."""
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, 'Meal deleted successfully.')
        return redirect('dashboard')
    return render(request, 'dietapp/meal_confirm_delete.html', {'meal': meal})


# User Details Submission

@login_required
def submit_user_details(request):
    """Allows users to submit or update profile details."""
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        meals = request.POST['meals']
        calories_consumed = request.POST['calories_consumed']
        calories_burned = request.POST['calories_burned']

        user_profile, created = UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'name': name,
                'age': age,
                'height': height,
                'weight': weight,
                'meals': meals,
                'calories_consumed': calories_consumed,
                'calories_burned': calories_burned,
            }
        )
        messages.success(request, 'User details updated successfully!')
        return redirect('dashboard')
    return render(request, 'dietapp/user_details_form.html')


# Messaging System

@login_required
def send_message(request):
    """Allows users to send messages to other users."""
    if request.method == 'POST':
        receiver_username = request.POST['receiver']
        content = request.POST['content']
        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('send-message')
    return render(request, 'messaging/send_message.html')


@login_required
def inbox(request):
    """Displays messages received by the user."""
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': received_messages})


@login_required
def sent_messages(request):
    """Displays messages sent by the user."""
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'messages': sent_messages})
