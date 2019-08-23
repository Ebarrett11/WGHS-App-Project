from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import UserRegisterForm


class UserRegistrationView(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Account created for {username}!")
        return redirect('users:login')
