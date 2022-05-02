from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Transaction, User


class Command(BaseCommand):
    @transaction.atomic()
    def handle(self, *args, **options):
        user_1 = User.objects.create_user(username='user1', password='user1')
        user_2 = User.objects.create_user(username='user2', password='user2')
        user_3 = User.objects.create_user(username='user3', password='user3')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_2.loan_to(user_3, 100, 'foo')
        user_3.loan_to(user_2, 100, 'bar')
