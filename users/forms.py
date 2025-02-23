from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    """Форма реєстрації"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserLoginForm(AuthenticationForm):
    """Форма логіну"""
    username = forms.EmailField(label="Email", required=True)
