from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Clinician

class ClinicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinician
        fields = '__all__'