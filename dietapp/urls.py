from django.urls import path
from .views import (
    MealListView, MealDetailView, MealCreateView, MealUpdateView, MealDeleteView
)
from . import views

urlpatterns = [
    # Meal views
    path('', MealListView.as_view(), name='dietapp-home'),  # Homepage listing meals
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),  # Meal detail view
    path('meal/new/', MealCreateView.as_view(), name='meal-create'),  # Create a new meal
    path('meal/<int:pk>/update/', MealUpdateView.as_view(), name='meal-update'),  # Update a meal
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),  # Delete a meal
    
    # Additional static pages
    path('about/', views.about, name='dietapp-about'),  # About page
    path('contact/', views.contact, name='dietapp-contact'),  # Contact page
]
