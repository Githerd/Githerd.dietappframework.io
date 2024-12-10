from django.urls import path, include
from django.contrib import admin
from users import views as user_views
from dietapp import views as dietapp_views
from dashboard import views as dashboard_views

urlpatterns = [
    # ========== Home ==========
    path("", dietapp_views.index, name="index"),  # Home page

    # ========== User Management ==========
    path("register/", user_views.register, name="register"),  # User registration
    path("login/", user_views.login_view, name="login"),  # Login page
    path("logout/", user_views.logout_view, name="logout"),  # Logout action
    path("profile/", user_views.profile, name="profile"),  # Profile page

    # ========== Journal Management ==========
    path("journal/", dietapp_views.JournalListView.as_view(), name="journal-list"),  # List of journal entries
    path("journal/<int:pk>/", dietapp_views.JournalDetailView.as_view(), name="journal-detail"),  # View a journal entry
    path("journal/new/", dietapp_views.JournalCreateView.as_view(), name="journal-create"),  # Create a new journal entry
    path("journal/<int:pk>/update/", dietapp_views.JournalUpdateView.as_view(), name="journal-update"),  # Update a journal entry
    path("journal/<int:pk>/delete/", dietapp_views.JournalDeleteView.as_view(), name="journal-delete"),  # Delete a journal entry

    # ========== TDEE and Weekly Calories ==========
    path("tdee/", dietapp_views.TDEEView.as_view(), name="tdee"),  # TDEE calculator
    path("weekly-calories/", dietapp_views.WeeklyCaloriesView.as_view(), name="weekly-calories"),  # Weekly calories overview

    # ========== Messaging ==========
    path("messages/send/", dietapp_views.send_message, name="send-message"),  # Send a message
    path("messages/inbox/", dietapp_views.inbox, name="inbox"),  # View received messages
    path("messages/sent/", dietapp_views.sent_messages, name="sent-messages"),  # View sent messages

    # ========== Meal Management ==========
    path("meals/single/", dietapp_views.singlemeal, name="single-meal"),  # Create or view single meals
    path("meals/delete/<int:meal_id>/", dietapp_views.deletemeal, name="delete-meal"),  # Delete a meal
    path("meals/weekly/", dietapp_views.weekly_plan, name="weekly-plan"),  # Weekly meal planning
    path("meals/weekly/delete/<int:plan_id>/", dietapp_views.deletefromplan, name="delete-weekly-plan"),  # Remove a meal from weekly plan

    # ========== Static Pages ==========
    path("about/", dietapp_views.about, name="about"),  # About page
    path("contact/", dietapp_views.contact, name="contact"),  # Contact page

    # ========== Admin Panel ==========
    path("admin/", admin.site.urls),  # Admin panel

    # ========== Additional Apps ==========
    path("polls/", include("polls.urls")),  # Polls app routes
    path("dashboard/", include("dashboard.urls")),  # Dashboard routes

    # ========== Exercise Management ==========
    path("add-exercise/", dietapp_views.add_exercise, name="add-exercise"),  # Add exercise route

    # ========== Legacy Routes (for backward compatibility) ==========
    path("singlemeal/", dietapp_views.singlemeal, name="singlemeal"),  # Legacy singlemeal route
    path("deletemeal/", dietapp_views.deletemeal, name="deletemeal"),  # Legacy deletemeal route
    path("deletefromplan/", dietapp_views.deletefromplan, name="deletefromplan"),  # Legacy deletefromplan route
]
