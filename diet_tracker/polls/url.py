from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='polls-dashboard'),  # Dashboard view
    path('add-meal/', views.add_meal, name='polls-add_meal'),  # Add meal view
    path('add-health-data/', views.add_health_data, name='polls-add_health_data'),  # Add health data view
    path('set-goal/', views.set_goal, name='polls-set_goal'),  # Set or update goal view
    path('meals/', views.meal_list, name='polls-meal_list'),  # Meal list view
    path('meals/delete/<int:meal_id>/', views.delete_meal, name='polls-delete_meal'),  # Delete meal view
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),  # Poll detail view
    path('poll/<int:poll_id>/results/', views.poll_results, name='poll_results'),  # Poll results view
    path('create/', views.create_poll, name='create_poll'),  # Create poll view
    path('poll/<int:poll_id>/add_choices/', views.add_choices, name='add_choices'),  # Add choices to poll
]
