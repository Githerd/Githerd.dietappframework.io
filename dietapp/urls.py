from django.urls import path, include
from django.contrib import admin
from users import views as user_views
from .views import (
    TDEEView,
    WeeklyCaloriesView,
    JournalListView,
    JournalDetailView,
    JournalCreateView,
    JournalUpdateView,
    JournalDeleteView,
    send_message,
    inbox,
    sent_messages,
    single_meal,
    delete_meal,
    weekly_plan,
    delete_weekly_plan,
    about,
    contact,
    index,
    login_view,
    logout_view,
    register,
    singlemeal,
    weekly,
    deletemeal,
    deletefromplan,
)

urlpatterns = [
    # ========== Home ==========
    path("", index, name="index"),  # Home page

    # ========== User Management ==========
    path("register/", user_views.register, name="register"),  # User registration
    path("login/", login_view, name="login"),  # Login page
    path("logout/", logout_view, name="logout"),  # Logout action
    path("profile/", user_views.profile, name="profile"),  # Profile page

    # ========== Journal Management ==========
    path("journal/", JournalListView.as_view(), name="dietapp-home"),  # List of journal entries
    path("journal/<int:pk>/", JournalDetailView.as_view(), name="journal-detail"),  # View a journal entry
    path("journal/new/", JournalCreateView.as_view(), name="journal-create"),  # Create a new journal entry
    path("journal/<int:pk>/update/", JournalUpdateView.as_view(), name="journal-update"),  # Update a journal entry
    path("journal/<int:pk>/delete/", JournalDeleteView.as_view(), name="journal-delete"),  # Delete a journal entry

    # ========== TDEE and Weekly Calories ==========
    path("tdee/", TDEEView.as_view(), name="tdee"),  # TDEE calculator
    path("weekly-calories/", WeeklyCaloriesView.as_view(), name="weekly-calories"),  # Weekly calories overview

    # ========== Messaging ==========
    path("messages/send/", send_message, name="send-message"),  # Send a message
    path("messages/inbox/", inbox, name="inbox"),  # View received messages
    path("messages/sent/", sent_messages, name="sent-messages"),  # View sent messages

    # ========== Meal Management ==========
    path("meals/single/", single_meal, name="single-meal"),  # Create or view single meals
    path("meals/delete/<int:meal_id>/", delete_meal, name="delete-meal"),  # Delete a meal
    path("meals/weekly/", weekly_plan, name="weekly-plan"),  # Weekly meal planning
    path("meals/weekly/delete/<int:meal_id>/", delete_weekly_plan, name="delete-weekly-plan"),  # Remove a meal from weekly plan

    # ========== Static Pages ==========
    path("about/", about, name="dietapp-about"),  # About page
    path("contact/", contact, name="dietapp-contact"),  # Contact page

    # ========== Admin Panel ==========
    path("admin/", admin.site.urls),  # Admin panel

    # ========== Polls App ==========
    path("polls/", include("polls.urls")),  # Polls app routes

    # ========== DietApp ==========
    path("dietapp/", include("dietapp.urls")),  # DietApp routes

    # ========== Exercise Management ==========
    path("dashboard/", include("dashboard.urls")),  # Dashboard routes
    path("add-exercise/", add_exercise, name="add-exercise"),  # Add exercise route

    # ========== Legacy Routes ==========
    # These routes are maintained for backward compatibility
    path("singlemeal/", singlemeal, name="singlemeal"),
    path("deletemeal/", deletemeal, name="deletemeal"),
    path("deletefromplan/", deletefromplan, name="deletefromplan"),
]
