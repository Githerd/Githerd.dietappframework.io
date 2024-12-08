from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Meal, Exercise, UserProfile

User = get_user_model()

class DietAppTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test user and related profile
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            age=25,
            weight=70,
            height=175,
            dietary_preferences="Vegetarian"
        )

        # Create a sample meal and exercise
        cls.meal = Meal.objects.create(
            user=cls.user,
            name="Test Meal",
            calories=500,
            protein=20,
            carbs=50,
            fat=15,
            description="A test meal"
        )

        cls.exercise = Exercise.objects.create(
            user=cls.user,
            name="Test Exercise",
            type="cardio",
            duration=30,
            calories_burned=300
        )

    def test_meal_list_view(self):
        url = reverse('meal-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Meal')
        self.assertTemplateUsed(response, 'dietapp/meal_list.html')

    def test_meal_detail_view(self):
        url = reverse('meal-detail', args=[self.meal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.meal.name)

    def test_create_meal_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/meal_form.html')

        response = self.client.post(reverse('meal-create'), {
            'name': 'New Meal',
            'calories': 400,
            'protein': 25,
            'carbs': 40,
            'fat': 10,
            'description': 'Another test meal',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Meal.objects.filter(name='New Meal').exists())

    def test_update_meal_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('meal-update', kwargs={'pk': self.meal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/meal_form.html')

        response = self.client.post(url, {
            'name': 'Updated Meal',
            'calories': 450,
            'protein': 30,
            'carbs': 45,
            'fat': 12,
            'description': 'Updated test meal',
        })
        self.meal.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.meal.name, 'Updated Meal')

    def test_delete_meal_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('meal-delete', kwargs={'pk': self.meal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/meal_confirm_delete.html')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Meal.objects.filter(pk=self.meal.pk).exists())

    def test_exercise_list_view(self):
        url = reverse('exercise-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Exercise')
        self.assertTemplateUsed(response, 'dietapp/exercise_list.html')

    def test_create_exercise_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('exercise-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/exercise_form.html')

        response = self.client.post(reverse('exercise-create'), {
            'name': 'New Exercise',
            'type': 'strength',
            'duration': 40,
            'calories_burned': 350,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Exercise.objects.filter(name='New Exercise').exists())

    def test_update_exercise_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('exercise-update', kwargs={'pk': self.exercise.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/exercise_form.html')

        response = self.client.post(url, {
            'name': 'Updated Exercise',
            'type': 'cardio',
            'duration': 35,
            'calories_burned': 320,
        })
        self.exercise.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.exercise.name, 'Updated Exercise')

    def test_delete_exercise_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('exercise-delete', kwargs={'pk': self.exercise.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dietapp/exercise_confirm_delete.html')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Exercise.objects.filter(pk=self.exercise.pk).exists())
