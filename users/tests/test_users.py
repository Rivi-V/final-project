from django.test import TestCase
from django.urls import reverse

from users.forms import ProfileForm
from users.models import User


class AuthFlowTests(TestCase):
    def test_register_login_and_logout(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'name': 'Иван',
                'surname': 'Иванов',
                'email': 'ivan@example.com',
                'password': 'secret12345',
            },
        )
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(email='ivan@example.com').exists())

        response = self.client.post(
            reverse('users:login'),
            {'email': 'ivan@example.com', 'password': 'secret12345'},
        )
        self.assertRedirects(response, reverse('projects:list'))

        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('projects:list'))

    def test_profile_form_normalizes_phone_and_validates_github(self):
        user = User.objects.create_user(
            email='user@example.com', password='password', name='User', surname='One'
        )
        form = ProfileForm(
            data={
                'name': 'User',
                'surname': 'One',
                'about': 'Hello',
                'phone': '89991234567',
                'github_url': 'https://github.com/user',
            },
            instance=user,
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '+79991234567')

        invalid_form = ProfileForm(
            data={
                'name': 'User',
                'surname': 'One',
                'about': 'Hello',
                'phone': '89991234567',
                'github_url': 'https://gitlab.com/user',
            },
            instance=user,
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertIn('github_url', invalid_form.errors)
