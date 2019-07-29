from django.urls import path
from . import views

app_name = "intern_management"
urlpatterns = [
    path('', views.InternshipListView.as_view(), name='details'),
    path('location/<int:pk>/', views.IntershipLocationDetail.as_view(), name='location_details'),
    path('location/sign-up/', views.InternshipSignUpView.as_view(), name='location_sign_up'),
    path('location/log-hours/<int:pk>', views.InternshipLogHoursView.as_view(), name='location_log'),

]
