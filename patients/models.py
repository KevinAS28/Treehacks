from django.db import models
from django.contrib.auth.models import User, auth

class PatientProfile(models.Model):  
    # Patient profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)  # patient, doctor or hospital
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    profilePicture = models.ImageField(upload_to="profilePics")
    # facial recognition field
    def __str__(self):
        return str(self.label)+" "+str(self.user)