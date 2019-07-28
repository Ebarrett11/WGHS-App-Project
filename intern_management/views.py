from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InternshipSignUpForm, InternshipLogForm
from .models import InternshipLocationModel
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/detail_page.html"
    context_object_name = "locations"
    ordering = "title"
    paginate_by = 10

    def get_queryset(self):
        return InternshipLocationModel.objects.all().filter(user=self.request.user)


class IntershipLocationDetail(DetailView):
    model = InternshipLocationModel
    template_name = "intern_management/location.html"
    context_object_name = "location"


class InternshipSignUpView(FormView):
    template_name = 'intern_management/location_sign_up.html'
    form_class = InternshipSignUpForm
    success_url = 'users:login'


class InternshipLogHoursView(LoginRequiredMixin, FormView):
    template_name = 'intern_management/location_log.html'
    form_class = InternshipLogForm
    success_url = 'intern_management:details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("location", get_object_or_404(InternshipLocationModel, pk=self.kwargs.get("pk")))
        return context

    def form_valid(self, form):
        print("form was valid")
        return super().form_valid(form)
