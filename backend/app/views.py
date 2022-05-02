import json

from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import JsonResponse
from app.forms import TransactionForm
from app.models import Transaction, User


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    # TODO Will need to use real sessions for a production quality app
    return JsonResponse({
        'status': 'success',
        'data': {'has_valid_credentials': bool(user)}
    })


def add_transaction(request):
    form = TransactionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'status': 'fail',
            'data': json.loads(form.errors.as_json())
        })
    if form.cleaned_data['is_debit']:
        debtor, debtee = form.cleaned_data['other'], form.cleaned_data['self']
    else:
        debtor, debtee = form.cleaned_data['self'], form.cleaned_data['other']
    transaction = debtor.loan_to(debtee, form.cleaned_data['amount'], form.cleaned_data['reason'])
    return JsonResponse({
        'status': 'success',
        'data': {'transaction': transaction.as_response()}
    })


def show_transactions(request):
    user = User.objects.filter(username=request.GET['username']).first()
    if not user:
        return JsonResponse({
            'status': 'fail',
            'data': {'user': 'not found'}
        })
    transactions = Transaction.objects.filter(Q(debtor=user) | Q(debtee=user)).order_by('-id').all()
    return JsonResponse({
        'status': 'success',
        'data': {'transactions': [transaction.as_response() for transaction in transactions]}
    })


def mark_paid(request):
    transaction = Transaction.objects.filter(id=request.POST['transaction_id'], repaid_at=None).first()
    if not transaction:
        return JsonResponse({
            'status': 'fail',
            'data': {'transaction': 'not found'}
        })
    transaction.set_paid()
    return JsonResponse({
        'status': 'success',
        'data': {}
    })
