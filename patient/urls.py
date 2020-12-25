from django.urls import path
from patient.views import PatientCreateView, DoctorCreateView, LoginUserView, Appointment

urlpatterns = [
    path('patient/create/', PatientCreateView.as_view()),
    path('doctor/create/', DoctorCreateView.as_view()),
    path('login/', LoginUserView.as_view(), name='login'),
    path('appointment/', Appointment.as_view(), name='appointment')
]
