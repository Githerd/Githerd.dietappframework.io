from django.urls import path
from .views import (
    JournalListView,
    JournalDetailView,
    JournalCreateView,
    JournalUpdateView,
    JournalDeleteView,
    TDEEView,
    WeeklyCaloriesView,
    single_meal,
    delete_meal,
    weekly_plan,
    delete_weekly_plan,
    send_message,
    inbox,
    sent_messages,
)
from . import views

urlpatterns = [
    # Journal-related views
    path('', JournalListView.as_view(), name='dietapp-home'),  # Homepage showing journal entries
    path('journal/<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),  # Journal entry detail
    path('journal/new/', JournalCreateView.as_view(), name='journal-create'),  # Create a new journal entry
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal-update'),  # Update journal entry
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal-delete'),  # Delete journal entry

    # TDEE and weekly calories views
    path('tdee/', TDEEView.as_view(), name='tdee'),  # TDEE calculator view
    path('weekly-calories/', WeeklyCaloriesView.as_view(), name='weekly-calories'),  # Weekly calorie stats

    # Messaging views
    path('messages/send/', send_message, name='send-message'),  # Send a message
    path('messages/inbox/', inbox, name='inbox'),  # Inbox for received messages
    path('messages/sent/', sent_messages, name='sent-messages'),  # Sent messages

    # Meal-related views
    path('meals/single/', single_meal, name='single-meal'),  # Create or view single meals
    path('meals/delete/<int:meal_id>/', delete_meal, name='delete-meal'),  # Delete a specific meal
    path('meals/weekly/', weekly_plan, name='weekly-plan'),  # Manage weekly meal plan
    path('meals/weekly/delete/<int:meal_id>/', delete_weekly_plan, name='delete-weekly-plan'),  # Remove meal from plan

    # Static pages
    path('about/', views.about, name='dietapp-about'),  # About page
    path('contact/', views.contact, name='dietapp-contact'),  # Contact page
]
