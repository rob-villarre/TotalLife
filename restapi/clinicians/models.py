from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
import requests

class Clinician(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    npi_number = models.CharField(max_length=10, unique=True)
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'npi_number'], name='unique_npi_number')
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.npi_number
