from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.apps import apps
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from .models import Meal, Carbs, Drinks, Fats, Meal, Vitamins, Proteins, User, Mineral, Exercise, Weekly, JournalEntry, UserProfile, TDEE, HealthData, Profile
from .forms import TDEEForm, MealForm, UserProfileForm, TDEEForm, JournalEntryForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm, RegisterForm, MealForm, CustomPasswordResetForm, HealthDataForm, WeeklyCaloriesView, TDEEView, TDEEForm, JournalEntryForm, WeeklyMealForm, ExerciseForm, MineralForm, VitaminForm

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


class TDEEView(LoginRequiredMixin, FormView):
    template_name = "dietapp/tdee.html"
    form_class = TDEEForm
    success_url = reverse_lazy("tdee")  # Redirect back to TDEE page on success

    def form_valid(self, form):
        weight = form.cleaned_data['weight']
        height = form.cleaned_data['height']
        age = form.cleaned_data['age']
        gender = form.cleaned_data['gender']
        activity_level = form.cleaned_data['activity_level']

        # Calculate TDEE
        gender_value = 5 if gender == "male" else -161
        activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]
        tdee_value = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier

        # Save the TDEE to the database
        TDEE.objects.update_or_create(
            user=self.request.user,
            defaults={'calories': tdee_value}
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tdee_record = TDEE.objects.filter(user=self.request.user).first()
        context['tdee'] = tdee_record.calories if tdee_record else 0
        return context


# Weekly Calories
class WeeklyCaloriesView(LoginRequiredMixin, TemplateView):
    template_name = "dietapp/weekly_calories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current week's meals and exercises
        current_week = now().isocalendar()[1]
        weekly_meals = Meal.objects.filter(user=self.request.user, date__week=current_week)
        weekly_exercises = Exercise.objects.filter(user=self.request.user, date__week=current_week)
        
        # Calculate total calories
        total_calories_intake = sum(meal.calories for meal in weekly_meals)
        total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)
        
        context['total_calories_intake'] = total_calories_intake
        context['total_calories_burned'] = total_calories_burned
        context['calories_net'] = total_calories_intake - total_calories_burned  # Net calories
        return context


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
