from django.test import TestCase
from django.urls import reverse
from .models import User

class UserTests(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect after login