from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    balance = models.IntegerField(default=0)

    def loan_to(self, debtee, amount, reason):
        transaction = Transaction.objects.create(debtor=self, debtee=debtee, amount=amount, reason=reason)
        self.balance += amount
        debtee.balance -= amount
        self.save()
        debtee.save()
        return transaction


class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    repaid_at = models.DateTimeField(null=True)
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debtor_transactions')
    debtee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debtee_transactions')
    reason = models.TextField(max_length=500)

    def as_response(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'is_repaid': bool(self.repaid_at),
            'amount': self.amount,
            'debtor': self.debtor.username,
            'debtee': self.debtee.username,
            'reason': self.reason
        }

    def set_paid(self):
        assert self.repaid_at is None
        self.repaid_at = now()
        self.save()
        self.debtor.balance -= self.amount
        self.debtor.save()
        self.debtee.balance += self.amount
        self.debtee.save()
