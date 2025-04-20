from django.urls import path
from django.contrib.auth import views as auth_views

from .views import assignments_view, home_view, registration_view, courses_view
from .widgets import my_courses, profile_widget, top_ups, upcoming_lessons

urlpatterns = [
    path("", home_view, name="home"),
    path("courses", courses_view, name="courses"),
    path("assignments", assignments_view, name="assignments"),
    path("auth/login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("auth/register/", registration_view),
    path("widget/profile", profile_widget),
    path("widget/upcoming_lessons", upcoming_lessons),
    path("widget/my_courses", my_courses),
    path("widget/top_ups", top_ups),
]
