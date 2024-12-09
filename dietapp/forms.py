from django import forms
from .models import Meal, UserProfile, JournalEntry, TDEE


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs', 'fat', 'description']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'age', 'height', 'weight', 'goal']


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']


class TDEEForm(forms.Form):
    weight = forms.FloatField(label="Weight (kg)")
    height = forms.FloatField(label="Height (cm)")
    age = forms.IntegerField(label="Age")
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    activity_level = forms.ChoiceField(
        choices=[
            (1, "Sedentary"),
            (2, "Lightly Active"),
            (3, "Moderately Active"),
            (4, "Very Active"),
            (5, "Super Active"),
        ],
        label="Activity Level",
    )
