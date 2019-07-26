from django.urls import path
from . import views

app_name = "intern_management"
urlpatterns = [
    path('', views.InternshipListView.as_view(), name='details'),
    path('account/', views.account, name='account'),
    path('location/<int:location_id>/', views.location_details, name='location_details')
]
