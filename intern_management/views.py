from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView

from .forms import InternshipSignUpForm
from .models import InternshipLocationModel
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/detail_page.html"
    context_object_name = "locations"
    ordering = "title"
    paginate_by = 10


class IntershipLocationDetail(DetailView):
    model = InternshipLocationModel
    template_name = "intern_management/location.html"
    context_object_name = "location"


class InternshipSignUpView(FormView):
    template_name = 'intern_management/location_sign_up.html'
    form_class = InternshipSignUpForm
    success_url = 'users:login'
