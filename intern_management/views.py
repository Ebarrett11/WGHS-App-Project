from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import InternshipLocationModel
# Create your views here.


class InternshipListView(LoginRequiredMixin, ListView):
    model = InternshipLocationModel
    context_object_name = "locations"
    template_name = "intern_management/detail_page.html"

def account(request):
    return render(request, 'intern_management/account.html')


def location_details(request, location_id=0):
    return render(request, 'intern_management/location.html', {
        "location": get_object_or_404(InternshipLocationModel, pk=location_id)
    })
