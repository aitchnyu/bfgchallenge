from django.test import Client, TestCase

from app.models import User


class LoginTestCase(TestCase):
    def test_user_can_login_with_correct_credentials_(self):
        client = Client()
        user = User.objects.create_user(username='foo', password='bar', balance=0)
        response = client.post('/login', {'username': 'foo', 'password': 'bar'})
        self.assertTrue(response.json()['has_logged_in'])

    def test_login_with_incorrect_credentials_fail(self):
        client = Client()
        response = client.post('/login', {'username': 'foo', 'password': 'bar'})
        self.assertFalse(response.json()['has_logged_in'])
