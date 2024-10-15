from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='polls-dashboard'),  # Dashboard view
    path('add-meal/', views.add_meal, name='polls-add_meal'),  # Add meal view
    path('add-health-data/', views.add_health_data, name='polls-add_health_data'),  # Add health data view
    path('set-goal/', views.set_goal, name='polls-set_goal'),  # Set or update goal view
    path('meals/', views.meal_list, name='polls-meal_list'),  # Meal list view
    path('meals/delete/<int:meal_id>/', views.delete_meal, name='polls-delete_meal'),  # Delete meal view
]