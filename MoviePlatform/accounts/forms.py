"""Файл с формами для приложения accounts"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=False)

    class Meta:
        """Метаинформация о форме"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']
