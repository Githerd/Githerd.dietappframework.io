from django.shortcuts import render, redirect
from django.contrib import messages  # For flash messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# User Registration View
def register(request):
    """
    Handles user registration. Displays the registration form and processes user input.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user and display a success message
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'The account {username} was created successfully. You can now login.')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# User Profile View
@login_required
def profile(request):
    """
    Handles user profile updates, including user account information and profile details.
    """
    if request.method == 'POST':
        # Instantiate forms with POST data and files for the logged-in user
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            # Save the updated user and profile data
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated successfully.')
            return redirect('profile')  # Avoid re-submission of form data on page refresh
    else:
        # Pre-fill the forms with the current user's data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Context data for rendering the profile template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)from django.shortcuts import render, redirect
from django.contrib import messages #import for messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'The account {username} was created successfully, now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
