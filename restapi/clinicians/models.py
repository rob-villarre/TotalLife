from django.utils import timezone
from django.db import models

class Clinician(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    npi_number = models.CharField(max_length=20, unique=True)
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # db_table = 'clinicians'
        constraints = [
            models.UniqueConstraint(fields=['id', 'npi_number'], name='unique_npi_number')
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.npi_number


# {
#     "id": 3,
#     "first_name": "JOHN",
#     "last_name": "AALTO",
#     "npi_number": "1518196054",
#     "state": "VA",
#     "created_at": "2025-03-15T01:26:56.126383Z"
# }