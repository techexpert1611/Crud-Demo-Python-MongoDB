# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView, TemplateView

from mongo import insert_appointment
from patient.forms import PatientForm, DoctorForm, LoginForm, AppointmentForm
from patient.models import Patient, Doctor


class PatientCreateView(CreateView):
    model = Patient
    template_name = 'patient/add_patient.html'
    form_class = PatientForm
    success_url = '/login'

    def get_context_data(self, **kwargs):
        data = super(PatientCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['patients'] = PatientForm(self.request.POST)
        else:
            data['patients'] = PatientForm()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        patients = context['patients']
        user = User.objects.create_user(username=form.data.get('username'), first_name=form.data.get('first_name'),
                                        last_name=form.data.get('last_name'), email=form.data.get('email'))
        user.set_password(form.data.get('password'))
        with transaction.atomic():
            self.object = form.save()
            if patients.is_valid():
                patients.instance = self.object
                patients.instance.user = user
                patients.save()

        return super(PatientCreateView, self).form_valid(form)


class DoctorCreateView(CreateView):
    model = Doctor
    template_name = 'doctor/add_doctor.html'
    form_class = DoctorForm
    success_url = '/login'

    def get_context_data(self, **kwargs):
        data = super(DoctorCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['doctors'] = DoctorForm(self.request.POST)
        else:
            data['doctors'] = DoctorForm()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        doctors = context['doctors']
        user = User.objects.create_user(username=form.data.get('username'), first_name=form.data.get('first_name'),
                                        last_name=form.data.get('last_name'), email=form.data.get('email'))
        user.set_password(form.data.get('password'))
        with transaction.atomic():
            self.object = form.save()
            if doctors.is_valid():
                doctors.instance = self.object
                doctors.instance.user = user
                doctors.save()

        return super(DoctorCreateView, self).form_valid(form)


class LoginUserView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(LoginUserView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['users'] = LoginForm(self.request.POST)
        else:
            data['users'] = LoginForm()

        return data

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        if username == "user" and password == "User@1234":
            user = User.objects.filter(username=username).first()
            login(self.request, user)
            return redirect('/')
        else:
            messages.error(self.request, 'username or password not correct')
            return redirect('login')


class Home(TemplateView):
    template_name = 'home.html'


class Appointment(FormView):
    template_name = 'appointment.html'
    form_class = AppointmentForm
    success_url = '/'

    def form_valid(self, form):
        doctor_name, patient_name, date_time = form.cleaned_data.get('doctor'), form.cleaned_data.get(
            'patient'), form.cleaned_data.get('appointment_date')
        doctor = Doctor.objects.filter(user__username=doctor_name).first()
        patient = Patient.objects.filter(user__username=patient_name).first()
        appointment_dict = {'doctor': doctor.id, 'patient': patient.id, 'appointment_date': date_time}
        insert_appointment(appointment_dict)
        return redirect('/')
