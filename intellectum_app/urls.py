from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home_view, registration_view, courses_view

urlpatterns = [
    path("", home_view, name="home"),
    path("courses", courses_view, name="courses"),
    path("auth/login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("auth/register/", registration_view),
]
