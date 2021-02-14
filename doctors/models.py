from django.db import models
from django.contrib.auth .models import User, auth
# Create your models here.
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_license_number = models.CharField(max_length=50, default = " ")
    proof = models.FileField(upload_to='proof_pdfs', null = True)
    country = models.CharField(max_length=200, default = "India")
    city = models.CharField(max_length=200, default = "Delhi")
    date_of_birth = models.DateField(default = "2000-02-03")
    # facial recognition field
    def __str__(self):
        return str(self.label)+" "+str(self.user)

