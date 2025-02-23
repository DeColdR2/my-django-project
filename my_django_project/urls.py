from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),            # Адмінка
    path('users/', include('users.urls')),      # URL для авторизації
    path('', include('home.urls')),             # Головна сторінка
    path('finances/', include('finances.urls')),  # Додали маршрути для фінансів
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    

]
