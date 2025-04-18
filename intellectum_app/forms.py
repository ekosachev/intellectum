from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Минимум 8 символов. Минимум 1 буква или специальный символ",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Совпадает с паролем",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Логин (используется для входа на сайт)",
            "email": "E-mail",
        }
        help_texts = {
            "first_name": "",
            "last_name": "",
            "email": "Должен быть действительным адресом электронной почты",
        }


class SigninForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
