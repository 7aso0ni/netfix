from django.urls import path
from . import views

urlpatterns = [
    path("auth/register", views.registerUser, name="register"),
    path("auth/login", views.loginUser, name="login"),
]
