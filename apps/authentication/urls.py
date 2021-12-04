from django.urls import path

from .views import LoginView, ChangePasswordView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
