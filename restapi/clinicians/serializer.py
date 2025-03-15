from django.urls import path, include
from django.contrib.auth.models import User
import requests
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator
from .models import Clinician

class ClinicianSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    npi_number = serializers.CharField(
        max_length=10,
        required=True,
        validators=[UniqueValidator(queryset=Clinician.objects.all())]
    )
    state = serializers.CharField(max_length=2, required=True)

    def validate(self, data):
        npi_number = data.get('npi_number')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        state = data.get('state')

        # API endpoint for NPI validation
        url = f'https://npiregistry.cms.hhs.gov/api/?number={npi_number}&version=2.1'

        response = requests.get(url)

        if response.status_code != 200:
            raise serializers.ValidationError("Error validating NPI number.")
        
        data = response.json()

        if 'results' not in data or len(data['results']) == 0:
            raise serializers.ValidationError('Invalid NPI number.')
        
        clinician_data = data['results'][0]
        # TODO: check all addresses?
        if clinician_data['basic']['first_name'] != first_name \
            or clinician_data['basic']['last_name'] != last_name \
            or clinician_data['addresses'][0]['state'] != state:
            raise serializers.ValidationError("NPI number does not match provided first name, last name, or state.")
        
        return data
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['first_name'] = data['first_name'].upper()
        data['last_name'] = data['last_name'].upper()
        data['state'] = data['state'].upper()
        return data
    
    class Meta:
        model = Clinician
        fields = '__all__'