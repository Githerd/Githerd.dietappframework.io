from django.test import TestCase
from django.urls import reverse
from .models import User
from .forms import UserRegisterForm

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )


    def test_user_profile_update(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password123'))

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect after login

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")  # Adjust for your template message


    def test_password_reset(self):
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)  # Should redirect after initiating password reset
        self.assertContains(response, "We've emailed you instructions for resetting your password.")
    

    def test_registration_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
