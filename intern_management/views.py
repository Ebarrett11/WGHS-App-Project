from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InternshipLocationModel
# Create your views here.


@login_required
def details(request):
    if request.method == "GET":
        if request.GET.get("search") is not None:
            pass

    return render(request, 'intern_management/detail_page.html', {
            'locations': request.user.internshiplocationmodel_set.all()
        })


def account(request):
    return render(request, 'intern_management/account.html')

def detail_page(request):
    return render(request, 'intern_management/detail_page.html')

def hours(request):
    return render(request, 'intern_management/hours.html')


def location_details(request, location_id=0):
    return render(request, 'intern_management/location.html', {
        "location": get_object_or_404(InternshipLocationModel, pk=location_id)
    })
