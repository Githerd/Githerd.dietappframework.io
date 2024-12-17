from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.urls import reverse

class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_profile_created(self):
        # Test if the profile is automatically created for a new user
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.user.username, 'testuser')

    def test_profile_str_method(self):
        # Test the __str__ method of the Profile model
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser Profile')


class UserFormsTest(TestCase):
    def test_valid_user_register_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_register_form(self):
        form_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'pass',
            'password2': 'mismatch',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_page_loads(self):
        # Test if the registration page loads correctly
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_successful_user_registration(self):
        # Test registering a new user
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_profile_page_loads(self):
        # Test if the profile page loads correctly
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_update(self):
        # Test updating the user profile
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'This is a test bio',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
