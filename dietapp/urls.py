from django.urls import path, include
from django.contrib import admin
from users import views as user_views
from . import views
from .views import JournalListView, JournalDetailView, JournalCreateView, JournalUpdateView, JournalDeleteView, TDEEView


urlpatterns = [
    # Home Page
    path("", views.home, name="home"),

    # User Management
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    # Journal Management
    path("journal/", views.JournalListView.as_view(), name="journal-list"),
    path("journal/<int:pk>/", views.JournalDetailView.as_view(), name="journal-detail"),
    path("journal/new/", views.JournalCreateView.as_view(), name="journal-create"),
    path("journal/<int:pk>/update/", views.JournalUpdateView.as_view(), name="journal-update"),
    path("journal/<int:pk>/delete/", views.JournalDeleteView.as_view(), name="journal-delete"),

    # TDEE and Weekly Calories
    path("tdee/", views.TDEEView.as_view(), name="tdee-calculate"),
    
    # Messaging
    path("messages/send/", views.send_messages, name="send-message"),
    path("messages/inbox/", views.inbox, name="inbox"),
    path("messages/sent/", views.sent_messages, name="sent-messages"),

    # Meal Management
    path("meals/single/", views.singlemeal, name="single-meal"),
    path("meals/delete/<int:meal_id>/", views.deletemeal, name="delete-meal"),
    path("meals/weekly/", views.weekly_plan, name="weekly-plan"),
    path("meals/weekly/delete/<int:plan_id>/", views.deletefromplan, name="delete-weekly-plan"),

    # Static Pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Admin Panel
    path("admin/", admin.site.urls),

    # Additional Apps
    path("polls/", include(("polls.urls", "polls"), namespace="polls")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Exercise Management
    path("add-exercise/", views.add_exercise, name="add-exercise"),
]
