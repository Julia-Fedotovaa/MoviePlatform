from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import RegistrationForm


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')  # Перенаправление на страницу входа

    def form_valid(self, form):
        form.save()  # Сохраняет пользователя
        return super().form_valid(form)
