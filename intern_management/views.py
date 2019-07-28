from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InternshipSignUpForm, InternshipLogForm
from .models import InternshipLocationModel
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/detail_page.html"
    context_object_name = "locations"
    paginate_by = 10

    def get_queryset(self):
        return InternshipLocationModel.objects.all().filter(
            user=self.request.user
        ).order_by('title')


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial.update({
            'locations': InternshipLocationModel.objects.all().filter(
                user=self.request.user
            )
        })
        kwargs.update({
            'initial': initial
        })

        return kwargs

    def form_valid(self, form):
        print("form was valid")
        return super().form_valid(form)
