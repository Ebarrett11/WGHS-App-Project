from django.shortcuts import render
# Create your views here.


def details(request):
    return render(request, 'intern_management/detail_page.html')


def account(request):
    return render(request, 'intern_management/account.html')
