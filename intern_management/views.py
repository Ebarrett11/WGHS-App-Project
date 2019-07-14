from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def details(request):
    return render(request, 'intern_management/detail_page.html')
