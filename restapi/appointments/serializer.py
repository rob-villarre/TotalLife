from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Appointment
from patients.models import Patient
from clinicians.models import Clinician

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'