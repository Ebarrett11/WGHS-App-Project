from django.urls import path
from . import views
urlpatterns = [
    path('', views.details, name='details'),
    path('account/', views.account, name='account')
]
