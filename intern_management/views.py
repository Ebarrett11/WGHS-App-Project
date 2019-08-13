import hashlib
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .forms import InternshipSignUpForm, InternshipLogForm
from .models import InternshipLocationModel
from .tokens import default_token_generator as token_gen
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
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


class HomePageView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/home.html"
    context_object_name = "locations"
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search'):
            queryset = self.request.user.internshiplocationmodel_set.filter(
                Q(title__contains=self.request.GET['search'])
                | Q(description__contains=self.request.GET['search'])
            ).order_by('title')
            return queryset
        return super().get_queryset()


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
    success_url = reverse_lazy('intern_management:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial.update({
            'locations':
                self.request.user.internshiplocationmodel_set.order_by(
                    'title'
                ),
            'pk': self.kwargs.get("pk"),
        })
        kwargs.update({
            'initial': initial,
        })

        return kwargs

    def form_valid(self, form):
        import string
        import random
        salt = ''.join(
            random.SystemRandom().choice(
                string.ascii_letters + string.digits
            ) for _ in range(10)
        )
        location = form.cleaned_data['location']
        token = token_gen.make_token(
            location,
            salt
        )

        # context for email to be sent
        context = {
            'name': form.cleaned_data['name'],
            'location': location,
            'hours': form.cleaned_data['hours'],
            'domain': get_current_site(self.request),
            'uid': urlsafe_base64_encode(
                force_bytes(self.request.user.pk)
                + b':'
                + force_bytes(salt)
            ).decode(),
            'token': token,
        }

        # save token to location
        location.outstanding_tokens += str(
            hashlib.sha256(
                force_bytes(token)
            ).hexdigest()) + ':'
        location.save()

        # send email to location manager
        form.send_mail(context, location.contact_email)
        messages.success(self.request, 'Request Submitted Successfully')
        return super().form_valid(form)


class InternshipConfirmHoursView(LoginRequiredMixin, UserPassesTestMixin,
                                 TemplateView):
    template_name = "intern_management/location_hours_confirm.html"

    def get_context_data(self, **kwargs):
        location = get_object_or_404(InternshipLocationModel, pk=kwargs['pk'])
        decoded_url = urlsafe_base64_decode(self.kwargs['UID']).split(b':')
        context = super().get_context_data(**kwargs)
        context.setdefault('location', location.title)
        context.setdefault('name', get_object_or_404(User, pk=int(decoded_url[0])))
        return context

    def test_func(self):
        # """
        #     Must return True for user to access view
        #
        #     Requirements:
        #         User must have valid Url token
        #             token must be used within allocated time
        #             token must be part of token list on database location
        #         User must be logged in as Manager for that location
        # """
        # # Get req info from request and Url
        # user = self.request.user
        # decoded_url = urlsafe_base64_decode(self.kwargs['UID'])
        # params = tuple(decoded_url.split(b':'))
        # location = InternshipLocationModel.objects.get(
        #     pk=kwargs['pk']
        # )
        # salt = params[1].decode()
        # token = self.kwargs['token']
        # # Validate Token
        # if token_gen.check_token(location,
        #                          salt, token):
        #     if user == location.manager:
        #         return True
        #
        # # If token fails return False
        # else:
        #     print("Token Validation fail")
        #     return False
        return True
