import requests
from django.conf import settings

API_URL = "https://openexchangerates.org/api/latest.json"

def get_exchange_rates():
    """Отримує актуальні курси валют від Open Exchange Rates."""
    try:
        response = requests.get(API_URL, params={"app_id": settings.OPEN_EXCHANGE_RATES_API_KEY})
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})
    except requests.RequestException:
        return {}  #
