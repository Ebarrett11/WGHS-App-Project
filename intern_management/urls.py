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
        'profile/',
        views.InternshipListView.as_view(),
        name='profile'
    ),
    path(
        'location/<int:pk>/',
        views.IntershipLocationDetail.as_view(),
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
        'location/confirmhours/<int:pk>/<str:UID>/<str:token>/',
        views.InternshipConfirmHoursView.as_view(),
        name='location_confirm'
    ),

]
