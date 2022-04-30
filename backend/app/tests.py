from django.test import Client, TestCase

# Create your tests here.
class WalletCreationTestCase(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/home')
        self.assertEqual(response.status_code, 200)
