from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.apps import apps
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required

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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('users', 'Profile')  # Dynamically get the Profile model
        fields = ['image', 'age', 'height', 'weight', 'goal']
        widgets = {
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }



@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to a profile page
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})
