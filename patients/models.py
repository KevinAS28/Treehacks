from django.db import models
from django.contrib.auth.models import User, auth
from doctors.models import DoctorProfile


class PatientProfile(models.Model):  
    # Patient profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200, default = "Patient")  # patient, doctor or hospital
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    profilePicture = models.ImageField(upload_to="profilePics")
    # facial recognition field
    def __str__(self):
        return str(self.label)+" "+str(self.user)


class Document(models.Model):
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    issued_by = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='prescription_pdfs')

class Records(models.Model):
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    # other details
    documents = []
    if Document.objects.all():
        documents = Document.objects.filter(patient = patient).order_by('-pk')