from django.urls import path
from .views import (
    MealListView, 
    MealDetailView, 
    MealCreateView, 
    MealUpdateView, 
    MealDeleteView,
    TDEEView,
    WeeklyCaloriesView
)
from . import views

urlpatterns = [
    # Meal-related views
    path('', MealListView.as_view(), name='dietapp-home'),  # Homepage listing meals
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),  # Meal detail view
    path('meal/new/', MealCreateView.as_view(), name='meal-create'),  # Create a new meal
    path('journal/<int:pk>/update/', views.journal_update, name='journal-update'),
    path('journal/<int:pk>/delete/', views.journal_delete, name='journal-delete'),
    
    # TDEE and Weekly Calories Views
    path('tdee/', TDEEView.as_view(), name='tdee'),  # TDEE calculator view
    path('weekly-calories/', WeeklyCaloriesView.as_view(), name='weekly-calories'),  # Weekly calories intake/burn view
