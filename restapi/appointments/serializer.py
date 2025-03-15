from django.utils import timezone
from rest_framework import serializers
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

        appointment = self.instance if self.instance else Appointment(**data)
    
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Appointment start_date must be before end_date")
        
        # Ensure no overlapping appointments for the same clinician
        overlapping_clinician_appointments = Appointment.objects.filter(
            clinician=data['clinician'],
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        ).exclude(id=appointment.id)

        if overlapping_clinician_appointments.exists():
            raise serializers.ValidationError('This appointment overlaps with an existing appointment for the clinician.')
        
        # Ensure no overlapping appointments for the same patient
        overlapping_patient_appointments = Appointment.objects.filter(
            patient=data['patient'],
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        ).exclude(id=appointment.id)

        if overlapping_patient_appointments.exists():
            raise serializers.ValidationError('This appointment overlaps with an existing appointment for the patient.')
        
        return data
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['status'] = data['status'].upper()
        return data

    class Meta:
        model = Appointment
        fields = '__all__'