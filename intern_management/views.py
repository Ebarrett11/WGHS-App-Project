from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .forms import InternshipSignUpForm, InternshipLogForm
from .models import InternshipLocationModel
from .tokens import default_token_generator as token_gen
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/detail_page.html"
    context_object_name = "locations"
    paginate_by = 10

    def get_queryset(self):
        queryset = self.request.user.internshiplocationmodel_set.order_by('title')
        if self.request.GET.get('search'):
            queryset = self.request.user.internshiplocationmodel_set.filter(
                Q(title__contains=self.request.GET['search'])
                | Q(description__contains=self.request.GET['search'])
            ).order_by('title')
        return queryset


class IntershipLocationDetail(DetailView):
    model = InternshipLocationModel
    template_name = "intern_management/location.html"
    context_object_name = "location"


class InternshipSignUpView(FormView):
    template_name = 'intern_management/location_sign_up.html'
    form_class = InternshipSignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        context = {
            'name': form.cleaned_data['location_name'],
            'address': form.cleaned_data['location_address'].title,
            'website': form.cleaned_data['location_website'],
            'email': form.cleaned_data['location_email'],
        }

        form.send_mail(context, settings.ADMIN_EMAIL)
        messages.success(self.request, 'Request Submitted Successfully')
        return super().form_valid(form)


class InternshipLogHoursView(LoginRequiredMixin, FormView):
    template_name = 'intern_management/location_hours_log.html'
    form_class = InternshipLogForm
    success_url = reverse_lazy('intern_management:details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial.update({
            'locations': self.request.user.internshiplocationmodel_set.order_by('title'),
            'pk': self.kwargs.get("pk"),
        })
        kwargs.update({
            'initial': initial,
        })

        return kwargs

    def form_valid(self, form):

        context = {
            'name': form.cleaned_data['name'],
            'location': form.cleaned_data['location'].title,
            'hours': form.cleaned_data['hours'],
            'domain': get_current_site(self.request),
            'lid': urlsafe_base64_encode(force_bytes(form.cleaned_data['location'].pk)).decode(),
            'token': token_gen.make_token(self.request.user, form.cleaned_data['location']),
        }

        form.send_mail(context, form.cleaned_data['location'].contact_email)
        messages.success(self.request, 'Request Submitted Successfully')
        return super().form_valid(form)


class InternshipConfirmHoursView(LoginRequiredMixin, UserPassesTestMixin,
                                 TemplateView):
    template_name = "intern_management/location_hours_confirm.html"

    def test_func(self):
        return True
