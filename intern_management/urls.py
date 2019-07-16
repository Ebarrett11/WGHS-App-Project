from django.urls import path
from . import views

app_name = "intern_management"
urlpatterns = [
    path('', views.details, name='details'),
    path('account/', views.account, name='account')
]
