from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Appointment
from patients.models import Patient
from clinicians.models import Clinician

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    clinician = serializers.PrimaryKeyRelatedField(queryset=Clinician.objects.all(), required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    status = serializers.CharField(max_length=20, default='SCHEDULED')
    created_at = serializers.DateTimeField(read_only=True, default=timezone.now)

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Appointment start_date must be before end_date")
        
        # Validate other fields using model's clean method
        appointment = Appointment(**data)
        appointment.clean()
        
        return data
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['status'] = data['status'].upper()
        return data

    class Meta:
        model = Appointment
        fields = '__all__'