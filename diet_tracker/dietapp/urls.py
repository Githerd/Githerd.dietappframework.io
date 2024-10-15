from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dietapp-home'),
    path('dashboard/', views.dashboard, name='dietapp-dashboard'),
]