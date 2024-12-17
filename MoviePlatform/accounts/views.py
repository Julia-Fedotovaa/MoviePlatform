"""Представления приложения accounts"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import RegistrationForm


class AccountView(LoginRequiredMixin, TemplateView):
    """Представление для отображения аккаунта пользователя"""
    template_name = 'account.html'


class RegisterView(FormView):
    """Представление для регистрации пользователя"""
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Метод для обработки валидной формы"""
        form.save()
        return super().form_valid(form)
