from django.contrib import admin
from django.urls import path, include
from . import views 
from django.db import models
from django.contrib.auth import views as auth_views
from django.conf import settings  # For media files handling
from django.conf.urls.static import static
from django.http import HttpResponse

# Health check view
def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Health check
    path('health/', health_check, name='health_check'),

    # User management views
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),

    # Password reset views
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),

    # Application routes
    path('', include('dietapp.urls')),  # Default homepage routes
    path('dietapp/', include('dietapp.urls')),  # DietApp-specific routes
    path('polls/', include('polls.urls')),  # Polls app routes
    path('users/', include('users.urls')),  # Users app-specific routes
]

# Media files handling during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
