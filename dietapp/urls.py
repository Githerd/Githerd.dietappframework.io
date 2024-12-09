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
)
from . import views

urlpatterns = [
    # Journal-related views
    path('', JournalListView.as_view(), name='dietapp-home'),  # Homepage showing journal entries
    path('journal/<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),
    path('journal/new/', JournalCreateView.as_view(), name='journal-create'),
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal-update'),
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal-delete'),

    # TDEE and Weekly Calories
    path('tdee/', TDEEView.as_view(), name='tdee'),
    path('weekly-calories/', WeeklyCaloriesView.as_view(), name='weekly-calories'),

    # Meal Management
    path('singlemeal/', single_meal, name='singlemeal'),
    path('deletemeal/<int:meal_id>/', delete_meal, name='deletemeal'),

    # Weekly Plan Management
    path('weekly-plan/', weekly_plan, name='weekly_plan'),
    path('delete-weekly/<int:weekly_id>/', delete_weekly_plan, name='delete_weekly_plan'),

    # Static Pages
    path('about/', views.about, name='dietapp-about'),
    path('contact/', views.contact, name='dietapp-contact'),
]
