import hashlib
import string
import random
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .forms import InternshipLogForm
from .models import (
    InternshipLocationModel, LoggedHoursModel, CommentModel,
)
from .tokens import default_token_generator as token_gen
# Create your views here.


class HomePageView(ListView):
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
        return super().get_queryset().order_by('title')


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


class IntershipLocationDetail(DetailView):
    model = InternshipLocationModel
    template_name = "intern_management/location.html"
    context_object_name = "location"

    def get_context_data(self, **kwargs):
        location = kwargs['object']
        context = super().get_context_data(**kwargs)
        context.setdefault("comments", location.commentmodel_set.all())

        if location in self.request.user.internshiplocationmodel_set.all():
            context.setdefault("is_enrolled", True)

        context.setdefault(
            "total_hours", location.get_total_hours(self.request.user)
        )
        context.setdefault(
            "available_work",
            location.availableworkmodel_set.all()
        )

        return context

    def post(self, *args, **kwargs):
        CommentModel.objects.create(
            user=self.request.user,
            location=get_object_or_404(
                InternshipLocationModel, pk=kwargs['pk']
            ),
            text=self.request.POST['text'],
            date_posted=timezone.now()
        )
        return redirect("intern_management:location_details", pk=kwargs['pk'])


class InternshipSignUpView(TemplateView):
    template_name = 'intern_management/location_sign_up.html'


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
        location = form.cleaned_data['location']

        request_id = ''.join(
            random.SystemRandom().choice(
                string.ascii_letters + string.digits
            ) for _ in range(10)
        )
        request = location.loggedhoursmodel_set.create(
            id=request_id, total_hours=form.cleaned_data['hours'],
            is_valid=False, user=self.request.user
        )
        token = token_gen.make_token(
            location,
            request
        )
        token_gen.assign_token(token, location)
        # context for email to be sent
        context = {
            'name': form.cleaned_data['name'],
            'location': location,
            'hours': form.cleaned_data['hours'],
            'domain': get_current_site(self.request),
            'request_id': urlsafe_base64_encode(
                force_bytes(request.id)
            ),
            'token': token,
        }

        # send email to location manager
        form.send_mail(context, location.contact_email)
        messages.success(self.request, 'Request Submitted Successfully')
        return super().form_valid(form)


class InternshipConfirmHoursView(LoginRequiredMixin, UserPassesTestMixin,
                                 TemplateView):
    template_name = "intern_management/location_hours_confirm.html"

    def get_context_data(self, **kwargs):
        request = get_object_or_404(
            LoggedHoursModel,
            pk=urlsafe_base64_decode(kwargs['request_id']).decode()
        )
        context = super().get_context_data(**kwargs)
        context.setdefault('location', request.location.title)
        context.setdefault('name', request.user.username)
        return context

    def post(self, *args, **kwargs):
        # need to put logging hours logic here
        request = get_object_or_404(
            LoggedHoursModel,
            pk=urlsafe_base64_decode(kwargs['request_id']).decode()
        )
        request.is_valid = True

        # invalidate Token
        location = request.location
        location_tokens = request.location.outstanding_tokens
        tokens = location_tokens.split(':')
        token_hash = str(hashlib.sha256(force_bytes(kwargs['token'])).hexdigest())
        tokens.remove(token_hash)
        tokens_serialized = ":".join(tokens)
        location.outstanding_tokens = tokens_serialized
        location.save()
        request.save()

        # Give success message
        messages.success(self.request, "Logged Hours Confirmed Successfully")
        return redirect('intern_management:home')

    def test_func(self):
        """
            Must return True for user to access view

            Requirements:
                User must have valid Url token
                    token must be used within allocated time
                    token must be part of token list on database location
                User must be logged in as Manager for that location
        """
        # Get req info from request and Url
        request = get_object_or_404(
            LoggedHoursModel,
            pk=urlsafe_base64_decode(self.kwargs['request_id']).decode()
        )
        token = self.kwargs["token"]
        location = request.location
        # Validate Token
        if token_gen.is_valid_token(
            location, request, token
        ):
            # if self.request.user in request.location.managers:
            return True

        # If token fails return False
        else:
            return False
