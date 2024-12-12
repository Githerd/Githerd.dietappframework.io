from django.urls import path, include
from django.contrib import admin
from users import views as user_views
from . import views
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    # Home Page
    path("", views.index, name="index"),

    # User Management
    path("register/", user_views.register, name="register"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    path("profile/", user_views.profile, name="profile"),

    # Journal Management
    path("journal/", dietapp_views.JournalListView.as_view(), name="journal-list"),
    path("journal/<int:pk>/", dietapp_views.JournalDetailView.as_view(), name="journal-detail"),
    path("journal/new/", dietapp_views.JournalCreateView.as_view(), name="journal-create"),
    path("journal/<int:pk>/update/", dietapp_views.JournalUpdateView.as_view(), name="journal-update"),
    path("journal/<int:pk>/delete/", dietapp_views.JournalDeleteView.as_view(), name="journal-delete"),

    # TDEE and Weekly Calories
    path("tdee/", dietapp_views.TDEEView.as_view(), name="tdee"),
    path("weekly-calories/", dietapp_views.WeeklyCaloriesView.as_view(), name="weekly-calories"),

    # Messaging
    path("messages/send/", dietapp_views.send_message, name="send-message"),
    path("messages/inbox/", dietapp_views.inbox, name="inbox"),
    path("messages/sent/", dietapp_views.sent_messages, name="sent-messages"),

    # Meal Management
    path("meals/single/", dietapp_views.singlemeal, name="single-meal"),
    path("meals/delete/<int:meal_id>/", dietapp_views.deletemeal, name="delete-meal"),
    path("meals/weekly/", dietapp_views.weekly_plan, name="weekly-plan"),
    path("meals/weekly/delete/<int:plan_id>/", dietapp_views.deletefromplan, name="delete-weekly-plan"),

    # Static Pages
    path("about/", dietapp_views.about, name="about"),
    path("contact/", dietapp_views.contact, name="contact"),

    # Admin Panel
    path("admin/", admin.site.urls),

    # Additional Apps
    path("polls/", include(("polls.urls", "polls"), namespace="polls")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Exercise Management
    path("add-exercise/", dietapp_views.add_exercise, name="add-exercise"),
]
