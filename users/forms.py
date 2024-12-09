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
from .models import Meal, UserProfile, JournalEntry, DietApp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# ===================== User Forms =====================
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


# ===================== Profile Forms =====================
class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile details.
    """
    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight', 'dietary_preferences']
        widgets = {
            'dietary_preferences': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


# ===================== Meal Forms =====================
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs', 'fat', 'description']


# ===================== TDEE Calculator Form =====================
class TDEEForm(forms.Form):
    weight = forms.FloatField(label="Weight (kg)", required=True)
    height = forms.FloatField(label="Height (cm)", required=True)
    age = forms.IntegerField(label="Age", required=True)
    gender = forms.ChoiceField(
        choices=[("male", "Male"), ("female", "Female")],
        widget=forms.RadioSelect,
        required=True
    )
    activity_level = forms.ChoiceField(
        choices=[
            (1, "Sedentary"),
            (2, "Lightly Active"),
            (3, "Moderately Active"),
            (4, "Very Active"),
            (5, "Super Active"),
        ],
        label="Activity Level",
        required=True
    )


# ===================== Journal Forms =====================
class JournalEntryForm(forms.ModelForm):
    """
    Form for managing journal entries.
    """
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your thoughts...'}),
        }


# ===================== Password Management Forms =====================
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
