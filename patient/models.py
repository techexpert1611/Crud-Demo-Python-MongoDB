from django.contrib.auth.models import User
from djongo import models
import datetime


class Patient(models.Model):
    age = models.IntegerField()
    symptoms = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_request_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}"


class Doctor(models.Model):
    specialization = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
