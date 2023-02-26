from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UserValidationView.as_view()), name='validate-username'),
    path('email-validation', csrf_exempt(EmailValidationView.as_view()), name='email-validation'),
    path('activation/<uidb64>/<token>', VerificationView.as_view(), name='activation'),
]