from django.db import models
from django.conf import settings
from .utils import get_exchange_rates
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=[('USD', 'US Dollar'), ('UAH', 'Ukrainian Hryvnia'),("EUR", "EUR")], default='UAH')
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("table_list")
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    categories = models.ManyToManyField(Category, related_name='transactions')
    table = models.ForeignKey (Table, on_delete=models.CASCADE, related_name="transactions")
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[("USD", "USD"), ("EUR", "EUR"), ("UAH", "UAH")], default="UAH")
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def convert_to_base_currency(self):
        """Конвертує суму в базову валюту UAH"""
        rates = get_exchange_rates()
        if self.currency == settings.BASE_CURRENCY or self.currency not in rates:
            return self.amount
        return self.amount * rates.get(settings.BASE_CURRENCY, 1)

    def __str__(self):
       return f"{self.amount} {self.currency} - {self.date}"
