from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Register')

    def test_register_view_POST_valid_form(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword',
                'password2': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Dear testuser, you have been successfully signed up!")
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_POST_invalid_form(self):
        data = {'username': 'testuser', 'email': 'invalidemail', 'password1': 'testpassword',
                'password2': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Enter a valid email address.')
        self.assertFalse(User.objects.filter(username='testuser').exists())
