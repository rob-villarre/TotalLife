from django.db import models

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    clinician = models.ForeignKey('clinicians.Clinician', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.clinician} on {self.appointment_date}"