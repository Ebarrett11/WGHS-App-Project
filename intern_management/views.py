from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import InternshipSignUpForm, InternshipLogForm
from .models import InternshipLocationModel
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    template_name = "intern_management/detail_page.html"
    context_object_name = "locations"
    paginate_by = 10

    def get_queryset(self):
        queryset = InternshipLocationModel.objects.filter(
            user=self.request.user
        ).order_by('title')

        if self.request.GET.get('search'):
            queryset = InternshipLocationModel.objects.filter(
                Q(user=self.request.user)
                & Q(title__contains=self.request.GET.get('search'))
                | Q(description__contains=self.request.GET.get('search'))
            ).order_by('title')
        return queryset


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
    success_url = reverse_lazy('intern_management:details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial.update({
            'locations': InternshipLocationModel.objects.all().filter(
                user=self.request.user
            ),
            'pk': self.kwargs.get("pk"),
        })
        kwargs.update({
            'initial': initial
        })

        return kwargs

    def form_valid(self, form):
        context = {
            'name': form.cleaned_data['name'],
            'location': form.cleaned_data['location'].title,
            'hours': form.cleaned_data['hours'],
        }

        form.send_mail(context, "Cu-Sith@gmx.com")
        return super().form_valid(form)
