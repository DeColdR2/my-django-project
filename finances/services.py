import requests
from django.conf import settings

API_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = "5917664317d445f2a93d03dbd3e47ec8"

def get_exchange_rates():
    response = requests.get(f"{API_URL}?app_id={API_KEY}")
    if response.status_code == 200:
        return response.json().get('rates', {})
    return {}

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates()
    if from_currency == "USD":
        return amount * rates.get(to_currency, 1)
    elif from_currency in rates:
        return (amount / rates[from_currency]) * rates.get(to_currency, 1)
    return amount
