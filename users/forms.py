from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile

User = get_user_model()  # Ensures compatibility with custom user models

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  
        fields = ['user', 'age', 'height', 'weight']


# Registration Form
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


# User Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'age', 'height', 'weight']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height in cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight in kg'}),
        }


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

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive value.")
        return weight

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height must be a positive value.")
        return height


# Health Data Form
class HealthDataForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight', 'height', 'age']


# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Enter your email address to search for your account."
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with the specified email address.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save'))


# Custom Set Password Form
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter a strong password.",
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as above for verification.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save'))
