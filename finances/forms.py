from django import forms
from .models import Table, Transaction

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'currency']  

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['table', 'amount', 'currency', 'description']

