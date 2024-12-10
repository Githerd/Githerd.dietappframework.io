from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile, UserProfile


# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


# User Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


# Profile Update Form (for Profile images)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


# Extended User Profile Form (for additional user details)
class UserProfileForm(forms.ModelForm):
    """Form for updating user profile details."""
    class Meta:
        model = UserProfile
        fields = ['image', 'age', 'height', 'weight', 'goal']
        widgets = {
            'goal': forms.Select(attrs={'class': 'form-control'}),  # Dropdown styling for 'goal'
            'image': forms.FileInput(attrs={'class': 'form-control'}),  # Styling for file input
        }
        labels = {
            'image': 'Profile Picture',
            'age': 'Age (years)',
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'goal': 'Goal',
        }
        help_texts = {
            'age': 'Enter your age in years.',
            'height': 'Enter your height in centimeters.',
            'weight': 'Enter your weight in kilograms.',
            'goal': 'Select your fitness goal.',
        }
        

# Login Form (customized if needed)
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, help_text="Enter your username or email.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Login'))


