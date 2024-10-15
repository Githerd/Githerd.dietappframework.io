from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Meal, HealthData, Goal
from .forms import MealForm, HealthDataForm, GoalForm
import openai
import os

# Dashboard view
@login_required
def dashboard(request):
    meals = Meal.objects.filter(user=request.user)
    health_data = HealthData.objects.filter(user=request.user).order_by('-date')
    goal = Goal.objects.filter(user=request.user).last()
    
    context = {
        'meals': meals,
        'health_data': health_data,
        'goal': goal
    }
    return render(request, 'dietapp/dashboard.html', context)

# View for adding a new meal
@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Meal added successfully.')
            return redirect('dashboard')
    else:
        form = MealForm()
    
    return render(request, 'dietapp/add_meal.html', {'form': form})

# View for adding health data
@login_required
def add_health_data(request):
    if request.method == 'POST':
        form = HealthDataForm(request.POST)
        if form.is_valid():
            health_data = form.save(commit=False)
            health_data.user = request.user
            health_data.save()
            messages.success(request, 'Health data added successfully.')
            return redirect('dashboard')
    else:
        form = HealthDataForm()
    
    return render(request, 'dietapp/add_health_data.html', {'form': form})

# View for setting or updating a health goal
@login_required
def set_goal(request):
    goal = Goal.objects.filter(user=request.user).last()
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal updated successfully.')
            return redirect('dashboard')
    else:
        form = GoalForm(instance=goal)
    
    return render(request, 'dietapp/set_goal.html', {'form': form})

# View for listing meals
@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user)
    return render(request, 'dietapp/meal_list.html', {'meals': meals})

# View for deleting a meal
@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, 'Meal deleted successfully.')
        return redirect('dashboard')
    
    return render(request, 'dietapp/confirm_delete.html', {'meal': meal})

# Load your OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@login_required
def ask_gpt(request):
    response_text = None

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input:
            try:
                # Call OpenAI GPT-3 API
                response = openai.Completion.create(
                    engine="text-davinci-003",  
                    prompt=user_input,
                    max_tokens=150
                )
                response_text = response.choices[0].text.strip()
            except Exception as e:
                response_text = f"An error occurred: {str(e)}"

    return render(request, 'ask_gpt.html', {'response': response_text})