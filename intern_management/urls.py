from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "intern_management"
urlpatterns = [
    path('', views.details, name='details'),

    path('account/', views.account, name='account'),
    path('detail_page/', views.detail_page, name='detail_page'),
    path('hours/', views.hours, name='hours'),
    path('location/<int:location_id>/', views.location_details, name='location_details')
]
