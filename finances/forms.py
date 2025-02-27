from django import forms

from .models import Category, Table, Transaction


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'currency']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'currency', 'categories', 'description', 'table']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Фільтруємо таблиці, щоб показати лише ті, що належать поточному користувачу
            self.fields['table'].queryset = Table.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Беремо користувача, щоб прив'язати категорію до нього
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
