from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserRegisterForm(UserCreationForm):
    """Form for registering a new user."""
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email


class UserLoginForm(AuthenticationForm):
    """Form for logging in a user."""
    username = forms.CharField(max_length=254, help_text="Enter your username or email.")

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    """Form for updating a user's information."""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.exclude(pk=user_id).filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating additional user profile information."""
    class Meta:
        model = Profile
        fields = [
            'age', 'height', 'weight', 'sex', 'activity_level', 
            'dietary_preferences', 'food_allergies', 
            'medical_conditions', 'goal'
        ]
        widgets = {
            'dietary_preferences': forms.Textarea(attrs={'rows': 2}),
            'food_allergies': forms.Textarea(attrs={'rows': 2}),
            'medical_conditions': forms.Textarea(attrs={'rows': 2}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """Form for resetting the user's password."""
    email = forms.EmailField(max_length=254, help_text="Enter your email address to search for your account.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("There is no user registered with the specified email address."))
        return email


class CustomSetPasswordForm(SetPasswordForm):
    """Form for setting a new password for a user."""
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter a strong password."),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as above for verification."),
    )