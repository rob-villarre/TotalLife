from django.db import models
from django.utils import timezone

# TODO: add more descripted fields
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + " " + self.last_name