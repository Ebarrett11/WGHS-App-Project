from django.urls import path
from . import views

app_name = "intern_management"
urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='home'
    ),
    path(
        'location/<int:pk>/',
        views.IntershipDetailView.as_view(),
        name='location_details'
    ),
    path(
        'location/signup/',
        views.InternshipSignUpView.as_view(),
        name='location_sign_up'
    ),
    path(
        'location/loghours/<int:pk>',
        views.InternshipLogHoursView.as_view(),
        name='location_log'
    ),
    path(
        'location/confirmhours/<str:request_id>/<str:token>/',
        views.InternshipConfirmHoursView.as_view(),
        name='location_confirm'
    ),

]
