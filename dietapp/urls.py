from django.urls import path, include
from .views import (
    JournalListView,
    JournalDetailView,
    JournalCreateView,
    JournalUpdateView,
    JournalDeleteView,
    TDEEView,
    WeeklyCaloriesView,
)
from . import views
from django.contrib import admin

urlpatterns = [
    # ========== Journal Management ==========
    path('', JournalListView.as_view(), name='dietapp-home'),  # Homepage listing journal entries
    path('journal/<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),  # Journal entry detail
    path('journal/new/', JournalCreateView.as_view(), name='journal-create'),  # Create new journal entry
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal-update'),  # Update journal entry
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal-delete'),  # Delete journal entry

    # ========== TDEE and Weekly Calories ==========
    path('tdee/', TDEEView.as_view(), name='tdee'),  # TDEE calculator
    path('weekly-calories/', WeeklyCaloriesView.as_view(), name='weekly-calories'),  # Weekly calories overview

    # ========== Messaging ==========
    path('messages/send/', send_message, name='send-message'),  # Send a new message
    path('messages/inbox/', inbox, name='inbox'),  # Inbox for received messages
    path('messages/sent/', sent_messages, name='sent-messages'),  # Sent messages overview

    # ========== Meal Management ==========
    path('meals/single/', single_meal, name='single-meal'),  # Create or view single meals
    path('meals/delete/<int:meal_id>/', delete_meal, name='delete-meal'),  # Delete a specific meal
    path('meals/weekly/', weekly_plan, name='weekly-plan'),  # Manage weekly meal plan
    path('meals/weekly/delete/<int:meal_id>/', delete_weekly_plan, name='delete-weekly-plan'),  # Remove meal from weekly plan

    # ========== Static Pages ==========
    path('about/', views.about, name='dietapp-about'),  # About page
    path('contact/', views.contact, name='dietapp-contact'),  # Contact page

    # ========== Admin Panel ==========
    path('admin/', admin.site.urls),  # Django admin panel

    # ========== Polls App ==========
    path('polls/', include('polls.urls')),  # Polls app URLs (if applicable)
]
