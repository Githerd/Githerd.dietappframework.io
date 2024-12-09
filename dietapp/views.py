from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User, Meal, Exercise, Weekly, JournalEntry, TDEE, Message, UserProfile
from .forms import RegisterForm, UserProfileForm, MealForm, JournalEntryForm, TDEEForm, ContactForm
from django.utils.timezone import now
from django.shortcuts import render
from django.core.mail import send_mail


# ========== Views ==========
def contact(request):
    """Render a contact form and handle form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract data from form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email (configure your email settings in settings.py)
            send_mail(
                subject=f"Contact Form Inquiry from {name}",
                message=message,
                from_email=email,
                recipient_list=['your_email@example.com'],  # Replace with your email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return render(request, 'dietapp/contact.html', {'form': ContactForm()})  # Render empty form after success
        else:
            messages.error(request, "There was an error in your form. Please try again.")


def about(request):
    """Render the About page."""
    return render(request, 'dietapp/about.html')


# ========== User Management ==========
def register(request):
    """Register a new user and create associated profiles."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to DietApp.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'dietapp/register.html', {'form': form, 'profile_form': profile_form})


def login_view(request):
    """Log in the user using provided credentials."""
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "dietapp/login.html")


@login_required
def logout_view(request):
    """Log out the user."""
    logout(request)
    return redirect('login')


# ========== Dashboard ==========
@login_required
def dashboard(request):
    """Display the user's dashboard with health data, meals, and activities."""
    # Get the logged-in user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Fetch meals created by the user
    meals = Meal.objects.filter(user=request.user).order_by('-date')[:5]  # Limit to 5 recent meals

    # Fetch TDEE information for the user
    tdee = TDEE.objects.filter(user=request.user).order_by('-date').first()

    # Fetch exercises logged by the user
    exercises = Exercise.objects.filter(user=request.user, date__week=now().isocalendar()[1])

    # Calculate total calories burned from exercises
    total_calories_burned = sum(exercise.calories_burned for exercise in exercises)

    # Calculate BMI
    bmi = user_profile.bmi

    # Pass data to the template
    context = {
        'user_profile': user_profile,
        'meals': meals,
        'tdee': tdee.calories if tdee else None,
        'exercises': exercises,
        'total_calories_burned': total_calories_burned,
        'bmi': bmi,
    }

    return render(request, 'dietapp/dashboard.html', context)


# ========== TDEE Calculator ==========
class TDEEView(TemplateView):
    template_name = "dietapp/tdee.html"

    def calculate_tdee(self, weight, height, age, gender, activity_level):
        """Calculate Total Daily Energy Expenditure (TDEE) using the Harris-Benedict formula."""
        gender_value = 5 if gender == "male" else -161
        activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]
        return ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier

    def get(self, request, *args, **kwargs):
        """Render the TDEE calculation form."""
        form = TDEEForm()
        return render(request, self.template_name, {"form": form, "result": None})

    def post(self, request, *args, **kwargs):
        """Process the TDEE form and save the result for authenticated users."""
        form = TDEEForm(request.POST)
        result = None
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # Calculate TDEE
            result = self.calculate_tdee(weight, height, age, gender, activity_level)

            # Save TDEE for authenticated users
            if request.user.is_authenticated:
                TDEE.objects.create(user=request.user, calories=int(result))

        return render(request, self.template_name, {"form": form, "result": result})



# ========== Journal Entry View ==========
# List view for all journal entries
class JournalListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'dietapp/journal_list.html'  # Custom template
    context_object_name = 'journals'  # Context variable for the journal list
    ordering = ['-date_posted']  # Order by most recent

# Detail view for a single journal entry
class JournalDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = 'dietapp/journal_detail.html'

# Create view for a new journal entry
class JournalCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    fields = ['title', 'content']  # Fields to include in the form
    template_name = 'dietapp/journal_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the current user as the author
        return super().form_valid(form)

# Update view for an existing journal entry
class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JournalEntry
    fields = ['title', 'content']
    template_name = 'dietapp/journal_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        journal = self.get_object()
        return self.request.user == journal.author  # Only allow the author to update

# Delete view for a journal entry
class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JournalEntry
    template_name = 'dietapp/journal_confirm_delete.html'
    success_url = reverse_lazy('dietapp-home')  # Redirect to the homepage after deletion

    def test_func(self):
        journal = self.get_object()
        return self.request.user == journal.author  # Only allow the author to delete


# ====== Meal Views ======
@login_required
def meal_list(request):
    """View to list all meals of the logged-in user."""
    meals = Meal.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dietapp/meal_list.html', {'meals': meals})


@login_required
def meal_create(request):
    """View to create a new meal."""
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, "Meal created successfully!")
            return redirect('meal-list')
    else:
        form = MealForm()
    return render(request, 'dietapp/meal_form.html', {'form': form})


@login_required
def meal_update(request, pk):
    """View to update an existing meal."""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal updated successfully!")
            return redirect('meal-list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'dietapp/meal_form.html', {'form': form})


@login_required
def meal_delete(request, pk):
    """View to delete a meal."""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, "Meal deleted successfully!")
        return redirect('meal-list')
    return render(request, 'dietapp/meal_confirm_delete.html', {'meal': meal})


# ====== Exercise Views ======
@login_required
def exercise_list(request):
    """View to list all exercises of the logged-in user."""
    exercises = Exercise.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dietapp/exercise_list.html', {'exercises': exercises})


@login_required
def exercise_create(request):
    """View to create a new exercise."""
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, "Exercise created successfully!")
            return redirect('exercise-list')
    else:
        form = ExerciseForm()
    return render(request, 'dietapp/exercise_form.html', {'form': form})


@login_required
def exercise_update(request, pk):
    """View to update an existing exercise."""
    exercise = get_object_or_404(Exercise, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, "Exercise updated successfully!")
            return redirect('exercise-list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'dietapp/exercise_form.html', {'form': form})


@login_required
def exercise_delete(request, pk):
    """View to delete an exercise."""
    exercise = get_object_or_404(Exercise, pk=pk, user=request.user)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, "Exercise deleted successfully!")
        return redirect('exercise-list')
    return render(request, 'dietapp/exercise_confirm_delete.html', {'exercise': exercise})



# ========== Meal Views ==========
@login_required
def single_meal(request):
    """Create or view single meals."""
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, "Meal added successfully!")
            return redirect('singlemeal')
    else:
        form = MealForm()

    meals = Meals.objects.filter(mealcreator=request.user)
    return render(request, 'dietapp/single_meal.html', {'form': form, 'meals': meals})


@login_required
def delete_meal(request, meal_id):
    """Delete a specific meal."""
    meal = get_object_or_404(Meals, id=meal_id, mealcreator=request.user)
    meal.delete()
    messages.success(request, "Meal deleted successfully!")
    return redirect('singlemeal')


# ========== Weekly Plan Views ==========
@login_required
def weekly_plan(request):
    """Manage weekly meal plans."""
    if request.method == "POST":
        day = request.POST.get("day")
        meal_id = request.POST.get("meal_id")
        meal = get_object_or_404(Meals, id=meal_id, mealcreator=request.user)
        Weekly.objects.create(day=day, meal=meal, user=request.user)
        messages.success(request, f"Meal added to your weekly plan for {day}!")
        return redirect('weekly_plan')

    meals = Meals.objects.filter(mealcreator=request.user)
    weekly_meals = Weekly.objects.filter(user=request.user)
    return render(request, 'dietapp/weekly_plan.html', {'meals': meals, 'weekly_meals': weekly_meals})


@login_required
def delete_weekly_plan(request, weekly_id):
    """Remove a meal from the weekly plan."""
    weekly_entry = get_object_or_404(Weekly, id=weekly_id, user=request.user)
    weekly_entry.delete()
    messages.success(request, "Meal removed from weekly plan!")
    return redirect('weekly_plan')


# ========== Messaging Views ==========
@login_required
def send_message(request):
    """Send a message to another user."""
    if request.method == "POST":
        receiver_username = request.POST.get("receiver")
        content = request.POST.get("content")
        if not receiver_username or not content:
            messages.error(request, "Both receiver and message content are required.")
            return redirect('send-message')

        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, 'messaging/send_message.html')


@login_required
def inbox(request):
    """View received messages."""
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/send_message.html', {'messages': messages_received})


@login_required
def sent_messages(request):
    """View sent messages."""
    messages_sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/send_message.html', {'messages': messages_sent}) 


@login_required
def delete_message(request, message_id):
    """Allow a user to delete a message."""
    message = get_object_or_404(Message, id=message_id)

    # Check if the user has permission to delete the message
    if message.receiver == request.user or message.sender == request.user:
        message.delete()
        messages.success(request, "Message deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this message.")

    return redirect('send_message')


# ========== Weekly Calories View ==========
class WeeklyCaloriesView(TemplateView):
    template_name = "dietapp/weekly_calories.html"

    def get_context_data(self, **kwargs):
        """Provide weekly calorie data and meal/exercise information."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            current_week = now().isocalendar()[1]  # Get current ISO week

            # Fetch meals and exercises for the week
            weekly_meals = Meal.objects.filter(user=self.request.user, date__week=current_week)
            weekly_exercises = Exercise.objects.filter(user=self.request.user, date__week=current_week)

            # Calculate total calories
            total_calories_intake = sum(meal.calories for meal in weekly_meals)
            total_calories_burned = sum(exercise.calories_burned for exercise in weekly_exercises)

            # Add data to the context
            context['total_calories_intake'] = total_calories_intake
            context['total_calories_burned'] = total_calories_burned
            context['weekly_meals'] = weekly_meals
            context['weekly_exercises'] = weekly_exercises
        else:
            # Default data for unauthenticated users
            context.update({
                'total_calories_intake': 0,
                'total_calories_burned': 0,
                'weekly_meals': [],
                'weekly_exercises': []
            })
        return context
