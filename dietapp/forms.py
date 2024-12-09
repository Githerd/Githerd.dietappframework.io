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
from .models import (
    Meal, Vitamin, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData
)


# User Registration Form
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


# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight', 'dietary_preferences']


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
