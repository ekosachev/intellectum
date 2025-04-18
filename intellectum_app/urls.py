from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home_view

urlpatterns = [
    path("", home_view, name="home_view"),
    path("auth/login/", auth_views.LoginView.as_view(template_name="auth/login.html")),
    path("auth/register/"),
]
