from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    # id = models.AutoField(primary_key=True)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # dob = models.DateField()
    # phone_number = models.CharField(max_length=20)
    # email = models.EmailField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
