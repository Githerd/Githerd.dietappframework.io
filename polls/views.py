from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Meal
from .forms import MealForm  # Assuming a MealForm is created for meal creation/updating


@login_required
def index(request):
    """
    Displays the latest meals added by the user.
    """
    latest_meal_list = Meal.objects.filter(user=request.user).order_by("-date")[:5]
    context = {"latest_meal_list": latest_meal_list}
    return render(request, "dietapp/home.html", context)


def about(request):
    """
    Renders the About page for the Diet App.
    """
    return render(request, 'dietapp/about.html', {'title': 'About'})


def contact(request):
    """
    Renders the Contact page for the Diet App.
    """
    return render(request, 'dietapp/contact.html', {'title': 'Contact'})


@login_required
def detail(request, meal_id):
    """
    Displays the details of a specific meal.
    """
    meal = get_object_or_404(Meal, pk=meal_id, user=request.user)
    return render(request, "dietapp/detail.html", {"meal": meal})


@login_required
def results(request, meal_id):
    """
    Placeholder view for displaying the results of a meal analysis.
    """
    meal = get_object_or_404(Meal, pk=meal_id, user=request.user)
    return render(request, "dietapp/results.html", {"meal": meal})


@login_required
def vote(request, meal_id):
    """
    Placeholder view for handling meal voting or rating.
    """
    return HttpResponse("You're rating the meal %s." % meal_id)


@login_required
def create_meal(request):
    """
    Allows the user to create a new meal.
    """
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('dietapp-home')
    else:
        form = MealForm()
    return render(request, "dietapp/create_meal.html", {"form": form})


@login_required
def edit_meal(request, meal_id):
    """
    Allows the user to edit an existing meal.
    """
    meal = get_object_or_404(Meal, pk=meal_id, user=request.user)
    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal-detail', meal_id=meal.id)
    else:
        form = MealForm(instance=meal)
    return render(request, "dietapp/edit_meal.html", {"form": form})


@login_required
def delete_meal(request, meal_id):
    """
    Deletes a meal for the logged-in user.
    """
    meal = get_object_or_404(Meal, pk=meal_id, user=request.user)
    if request.method == "POST":
        meal.delete()
        return redirect('dietapp-home')
    return render(request, "dietapp/delete_meal.html", {"meal": meal})
