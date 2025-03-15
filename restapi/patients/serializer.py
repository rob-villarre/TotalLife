from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    dob = serializers.DateField()
    phone_number = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Patient.objects.all())]
    )
    gender = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def validate(self, data):
        return super().validate(data)
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        data['first_name'] = data['first_name'].upper()
        data['last_name'] = data['last_name'].upper()
        data['gender'] = data['gender'].upper()
        data['email'] = data['email'].lower()
        return data