from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm
from .models import User

class UserRegisterView(CreateView):
    """Реєстрація користувача"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class UserLoginView(LoginView):
    """Вхід в акаунт"""
    form_class = UserLoginForm
    template_name = 'users/login.html'

def user_logout(request):
    """Вихід з акаунту"""
    logout(request)
    return redirect('home')
