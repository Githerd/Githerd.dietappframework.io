from django.urls import path
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

urlpatterns = [
    # Journal-related views
    path('', JournalListView.as_view(), name='dietapp-home'),  # Homepage listing journal entries
    path('journal/<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),  # Journal entry detail view
    path('journal/new/', JournalCreateView.as_view(), name='journal-create'),  # Create a new journal entry
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal-update'),  # Update a journal entry
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal-delete'),  # Delete a journal entry

    # TDEE and Weekly Calories Views
    path('tdee/', TDEEView.as_view(), name='tdee'),  # TDEE calculator view
    path('weekly-calories/', WeeklyCaloriesView.as_view(), name='weekly-calories'),  # Weekly calories intake/burn view

    # Additional static pages
    path('about/', views.about, name='dietapp-about'),  # About page
    path('contact/', views.contact, name='dietapp-contact'),  # Contact page
]
