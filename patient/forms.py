from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import DateTimeInput

from patient.models import Patient, Doctor, Appointment


class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=256, min_length=3)
    first_name = forms.CharField(max_length=256, min_length=3)
    last_name = forms.CharField(max_length=256, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        exclude = ()
        fields = ['age', 'symptoms',
                  'appointment_request_date'] + ['username', 'first_name', 'last_name', 'email', 'password']

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# PatientFormSet = inlineformset_factory(User, Patient, form=PatientForm,
#                                        fields=['age', 'symptoms',
#                                                'appointment_request_date'])


class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=256, min_length=3)
    first_name = forms.CharField(max_length=256, min_length=3)
    last_name = forms.CharField(max_length=256, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        exclude = ()
        fields = ['specialization', ] + ['username', 'first_name', 'last_name', 'email', 'password']

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'required': True, 'autofocus': True}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': True}))
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ()
        fields = ['doctor', 'patient', 'appointment_date']
        widgets = {'appointment_date': DateTimeInput(attrs={'class': 'datetime-input', 'data-target': '#datet'})}

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'
