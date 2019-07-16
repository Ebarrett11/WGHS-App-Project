from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InternshipLocationModel
# Create your views here.


@login_required
def details(request):
    if request.method == "GET":
        if request.GET.get("search") != None:
            pass


    return render(request, 'intern_management/detail_page.html', { 'locations': InternshipLocationModel.objects.all()})


def account(request):
    return render(request, 'intern_management/account.html')
