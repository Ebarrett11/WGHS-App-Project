from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

from .forms import UserRegisterForm
from intern_management.models import InternshipLocationModel


class UserRegistrationView(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Account created for {username}!")
        return redirect('users:login')


class UserProfileView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/profile_page.html"
    context_object_name = "locations"

    def get_queryset(self):
        queryset = self.request.user.internshiplocationmodel_set.order_by(
            'title'
        )
        if self.request.GET.get('search'):
            queryset = self.request.user.internshiplocationmodel_set.filter(
                Q(title__contains=self.request.GET['search'])
                | Q(description__contains=self.request.GET['search'])
            ).order_by('title')
        return queryset
