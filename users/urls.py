from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailVerify, VerificationView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verification/<str:token>/', EmailVerify.as_view(), name='verification'),
    path('verification/', VerificationView.as_view(), name='verify'),
    path('password_reset/', PasswordChangeView.as_view(), name='password_reset')
]

