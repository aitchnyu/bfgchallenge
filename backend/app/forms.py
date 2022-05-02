from django import forms

from app.models import User

class TransactionForm(forms.Form):
    amount = forms.IntegerField(min_value=0)
    self = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='username')
    other = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='username')
    is_debit = forms.BooleanField()
    reason = forms.CharField(max_length=500)

    # TODO check self and other are different