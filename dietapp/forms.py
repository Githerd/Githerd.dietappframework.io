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
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import (
    Meal, Vitamin, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData, Profile
)
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.apps import apps
from .models import Profile  # Directly import the Profile model


User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information including image, age, height, weight, and goal.
    """
    class Meta:
        model = Profile  # Directly referencing the Profile model
        fields = ['image', 'age', 'height', 'weight', 'goal']  # Include all necessary fields
        widgets = {
            'goal': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for goal
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height in cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight in kg'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating additional user profile information.
    """
    class Meta:
        model = UserProfile  # Directly reference the model
        fields = ['image', 'age', 'height', 'weight', 'goal']
        widgets = {
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }

# Registration Form
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}), 
        required=True, 
        label="Your Message"
    )




# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight', 'dietary_preferences']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

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
        

# Meal Form
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs', 'fat', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# Vitamin Form
class VitaminForm(forms.ModelForm):
    class Meta:
        model = Vitamin
        fields = ['name', 'percentage']


# Mineral Form
class MineralForm(forms.ModelForm):
    class Meta:
        model = Mineral
        fields = ['name', 'percentage']


# Exercise Form
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'type', 'duration', 'calories_burned']


# Weekly Meal Plan Form
class WeeklyMealForm(forms.ModelForm):
    class Meta:
        model = Weekly
        fields = ['day', 'meal']


# Journal Entry Form
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your thoughts...'}),
        }


# TDEE Form
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


# Health Data Form
class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ['weight', 'height', 'age', 'calories_intake', 'calories_burned']


# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Enter your email address to search for your account."
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("There is no user registered with the specified email address."))
        return email


# Custom Set Password Form
class CustomSetPasswordForm(SetPasswordForm):
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
