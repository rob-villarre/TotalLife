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

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")
        
        # Ensure no overlapping appointments for the same clinician
        overlapping_clinician_appointments = Appointment.objects.filter(
            clinician=self.clinician,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(id=self.id)

        if overlapping_clinician_appointments.exists():
            raise ValidationError('This appointment overlaps with an existing appointment for the clinician.')
        
        # Ensure no overlapping appointments for the same patient
        overlapping_patient_appointments = Appointment.objects.filter(
            patient=self.patient,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(id=self.id)

        if overlapping_patient_appointments.exists():
            raise ValidationError('This appointment overlaps with an existing appointment for the patient.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"Appointment for {self.patient} with {self.clinician} on {self.start_date} to {self.end_date}"