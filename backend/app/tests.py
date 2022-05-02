import json
from django.core.serializers.json import DjangoJSONEncoder
from django.test import Client, TestCase

from app.models import Transaction, User


class AppTestCase(TestCase):
    maxDiff = None  # Show all the text in case a diff fails

    def assertResponseDataEqualsTo(self, response, dictt):
        '''
        An example of a matching pair would be
        {'id': 'ea0212d3-abd6-406f-8c67-868e814a2436',
        'at': '2022-04-29T15:20:50.590Z'}
        which has been deserialized from an actual response

        and

        {'id': UUID('ea0212d3-abd6-406f-8c67-868e814a2436',
        'at': datetime.datetime(2022, 4, 29, 15, 20, 50, 590566, tzinfo=datetime.timezone.utc))}
        which was returned by some function
        '''
        self.assertEqual(
            response.json()['data'],
            # Transform date, uuids etc into their json counterparts
            json.loads(json.dumps(dictt, cls=DjangoJSONEncoder)))

    def assertResponseSuccess(self, response):
        self.assertEqual(response.json()['status'], 'success')

    def assertResponseFail(self, response):
        self.assertEqual(response.json()['status'], 'fail')


class LoginTestCase(AppTestCase):
    def test_user_can_login_with_correct_credentials(self):
        client = Client()
        user = User.objects.create_user(username='foo', password='bar')
        response = client.post('/login', {'username': 'foo', 'password': 'bar'})
        self.assertTrue(response.json()['data']['has_valid_credentials'])

    def test_login_with_incorrect_credentials_fail(self):
        client = Client()
        response = client.post('/login', {'username': 'foo', 'password': 'bar'})
        self.assertFalse(response.json()['data']['has_valid_credentials'])


class CreateTransactionTestCase(AppTestCase):
    def test_user_can_create_transaction(self):
        client = Client()
        user_1 = User.objects.create_user(username='u1', password='u1')
        user_2 = User.objects.create_user(username='u2', password='u2')
        response = client.post(
            '/add_transaction',
            {'self': 'u1',
             'other': 'u2',
             'amount': '100',
             'is_debit': 'true',
             'reason': 'restaurant'}
        )
        self.assertResponseSuccess(response)
        transaction_1 = Transaction.objects.filter(debtor=user_2).get()
        self.assertEqual(transaction_1.debtee, user_1)
        self.assertEqual(transaction_1.amount, 100)
        self.assertEqual(transaction_1.reason, 'restaurant')
        self.assertResponseDataEqualsTo(response, {'transaction': transaction_1.as_response()})
        user_1 = User.objects.get(username='u1')
        user_2 = User.objects.get(username='u2')
        self.assertEqual(user_1.balance, -100)
        self.assertEqual(user_2.balance, 100)

    def test_sending_malformed_data_returns_form_errors(self):
        client = Client()
        user_1 = User.objects.create_user(username='u1', password='u1')
        user_2 = User.objects.create_user(username='u2', password='u2')
        response = client.post(
            '/add_transaction',
            {'self': 'fake',
             'other': 'fake',
             'amount': '100',
             'is_debit': 'true',
             'reason': 'restaurant'}
        )
        self.assertResponseFail(response)
        self.assertEqual(set(response.json()['data'].keys()), {'self', 'other'})


class GetTransactionsTestCase(AppTestCase):
    def test_user_can_get_transactions_related_to_them(self):
        client = Client()
        user_1 = User.objects.create_user(username='u1', password='u1')
        user_2 = User.objects.create_user(username='u2', password='u2')
        user_3 = User.objects.create_user(username='u3', password='u3')
        transaction_1 = user_1.loan_to(user_2, 100, 'foo')
        transaction_2 = user_2.loan_to(user_1, 100, 'foo')
        transaction_3 = user_2.loan_to(user_3, 100, 'foo')
        transaction_4 = user_3.loan_to(user_2, 100, 'foo')
        transaction_5 = user_3.loan_to(user_1, 100, 'foo')
        response = client.get('/get_transactions', {'username': 'u1'})
        response_transactions = response.json()['data']['transactions']
        self.assertEqual(response_transactions[0]['id'], transaction_5.id)
        self.assertEqual(response_transactions[1]['id'], transaction_2.id)
        self.assertEqual(response_transactions[2]['id'], transaction_1.id)


class MarkPaidTestCase(AppTestCase):
    def test_user_can_mark_transaction_as_paid(self):
        client = Client()
        user_1 = User.objects.create_user(username='u1', password='u1')
        user_2 = User.objects.create_user(username='u2', password='u2')
        transaction_1 = user_1.loan_to(user_2, 100, 'foo')
        response = client.post('/mark_paid', {'transaction_id': transaction_1.id})
        transaction_1 = Transaction.objects.get(id=transaction_1.id)
        self.assertIsNotNone(transaction_1.repaid_at)
        user_1 = User.objects.get(id=user_1.id)
        self.assertEqual(user_1.balance, 0)
        user_2 = User.objects.get(id=user_2.id)
        self.assertEqual(user_2.balance, 0)

    def test_paying_already_paid(self):
        client = Client()
        user_1 = User.objects.create_user(username='u1', password='u1')
        user_2 = User.objects.create_user(username='u2', password='u2')
        transaction_1 = user_1.loan_to(user_2, 100, 'foo')
        transaction_1.set_paid()
        response = client.post('/mark_paid', {'transaction_id': transaction_1.id})
        self.assertResponseFail(response)


