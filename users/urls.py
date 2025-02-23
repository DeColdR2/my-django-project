from django.urls import path
from .views import UserRegisterView, UserLoginView, user_logout
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
]
