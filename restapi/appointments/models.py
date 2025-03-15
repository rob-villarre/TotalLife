from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    clinician = models.ForeignKey('clinicians.Clinician', on_delete=models.CASCADE, related_name='appointments')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='scheduled')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'clinician', 'start_date'], name='unique_patient_clinician_appointment'),
            models.UniqueConstraint(fields=['clinician', 'start_date'], name='unique_clinician_appointment'),
            models.UniqueConstraint(fields=['patient', 'start_date'], name='unique_patient_appointment')
        ]

    def __str__(self):
        return f"Appointment for {self.patient} with {self.clinician} on {self.start_date} to {self.end_date}"