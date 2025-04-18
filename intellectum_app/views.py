from django.shortcuts import render, redirect
from django.contrib.auth import login

from intellectum_app.forms import RegistrationForm
# Create your views here.


def home_view(request):
    return render(request, "auth/registration.html")


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            login(request, user, backend="axes.backends.AxesBackend")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "auth/registration.html", {"form": form})
