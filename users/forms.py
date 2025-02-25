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

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={'invalid': 'Введіть коректний email.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        error_messages={'required': 'Пароль не може бути порожнім.'}
    )