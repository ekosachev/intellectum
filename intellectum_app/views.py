from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request: HttpRequest):
    return render(request, "auth/registration.html")

def auth_registration(request: HttpRequest):
    
