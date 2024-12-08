from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Meal, UserProfile, DietApp, JournalEntry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'date']


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile details."""
    class Meta:
        model = UserProfile
        fields = ['image', 'age', 'height', 'weight', 'goal']


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user with username, email, and password validation.
    """
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """
        Ensure the email is unique across all users.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email


class UserLoginForm(AuthenticationForm):
    """
    Form for logging in a user using username or email and password.
    """
    username = forms.CharField(
        max_length=254,
        help_text="Enter your username or email."
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating a user's information including unique email validation.
    """
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        """
        Ensure the updated email is unique across all users except the current one.
        """
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.exclude(pk=user_id).filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating additional user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['image', 'age', 'height', 'weight', 'goal']
        widgets = {
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }


class DietAppForm(forms.ModelForm):
    """
    Form for managing DietApp-related data including activity level, dietary preferences, etc.
    """
    class Meta:
        model = DietApp
        fields = ['activity_level', 'dietary_preferences', 'food_allergies', 'goal']
        widgets = {
            'dietary_preferences': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'food_allergies': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your thoughts...'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """
    Form for initiating a password reset using the user's email address.
    """
    email = forms.EmailField(
        max_length=254,
        help_text="Enter your email address to search for your account."
    )

    def clean_email(self):
        """
        Ensure the email exists in the database.
        """
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("There is no user registered with the specified email address."))
        return email


class CustomSetPasswordForm(SetPasswordForm):
    """
    Form for setting a new password for the user during password reset.
    """
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter a strong password."),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as above for verification."),
    )
