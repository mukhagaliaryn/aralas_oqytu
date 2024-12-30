from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.forms import UserForm, UserUpdateForm
from accounts.models import User


# Signup
class SignUpView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


# Profile
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user


# Edit profile
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Сіздің профиліңіз сәтті жаңартылды!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Төмендегі қателерді түзетіңіз.')
        return super().form_invalid(form)


# Delete profile
class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


# Password change
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Сіздің пароліңіз сәтті жаңартылды!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Төмендегі қатені түзетіңіз.')
        return super().form_invalid(form)
