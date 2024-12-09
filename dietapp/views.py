from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, MealForm, JournalEntryForm
from .models import Meal, UserProfile, Message, Exercise, TDEE, JournalEntry
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.utils.timezone import now
from .forms import TDEEForm


# Basic Views
def home(request):
    return render(request, 'dietapp/home.html')


def about(request):
    return render(request, 'dietapp/about.html')


def contact(request):
    return render(request, 'dietapp/contact.html')


# User Management
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to DietApp.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'dietapp/register.html', {'form': form, 'profile_form': profile_form})


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'dietapp/dashboard.html', {'user': user_profile})


def tdee_calculate(request):
    result = None
    if request.method == "POST":
        form = TDEEForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']

            # Gender constant: 5 for male, -161 for female
            gender_value = 5 if gender == "male" else -161
            activity_multiplier = [1.2, 1.375, 1.55, 1.725, 1.9][int(activity_level) - 1]

            result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activity_multiplier
    else:
        form = TDEEForm()

    return render(request, "dietapp/tdee_calculate.html", {"form": form, "result": result})


# Journal Management
class JournalListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'dietapp/journal_list.html'
    context_object_name = 'journals'


class JournalDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = 'dietapp/journal_detail.html'


class JournalCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'dietapp/journal_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author


class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JournalEntry
    template_name = 'dietapp/journal_confirm_delete.html'
    success_url = reverse_lazy('journal-list')

    def test_func(self):
        return self.request.user == self.get_object().author


# Messages
@login_required
def send_message(request):
    if request.method == "POST":
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
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
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'messages': messages})


# TDEE & Weekly Calories
class TDEEView(TemplateView):
    template_name = 'dietapp/tdee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tdee = TDEE.objects.filter(user=self.request.user).first()
        context['tdee'] = tdee.calories if tdee else 0
        return context


class WeeklyCaloriesView(TemplateView):
    template_name = 'dietapp/weekly_calories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weekly_meals = Meal.objects.filter(user=self.request.user, date__week=timezone.now().isocalendar()[1])
        weekly_exercises = Exercise.objects.filter(user=self.request.user, date__week=timezone.now().isocalendar()[1])
        context['total_calories_intake'] = sum(meal.calories for meal in weekly_meals)
        context['total_calories_burned'] = sum(exercise.calories_burned for exercise in weekly_exercises)
        return context
