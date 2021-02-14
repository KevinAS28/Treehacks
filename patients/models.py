from django.db import models
from django.contrib.auth.models import User, auth
from doctors.models import DoctorProfile

class PatientProfile(models.Model):  
    # Patient profile

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    profilePicture = models.ImageField(upload_to="profilePics")
    addressline1 =  models.CharField(max_length=200, default = " ")
    addressline2 =  models.CharField(max_length=200, default = " ")
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=12)

    sex = models.CharField(max_length=20)
    pronouns = models.CharField(max_length=100)
    race = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)


    # facial recognition field    
    def __str__(self):
        return str(self.user)

class Document(models.Model): #stores individual documents
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    issued_by = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=(('Prescription', 'Prescription'), ('Results', 'Results'), ('Other', 'Other')))
    pdf = models.FileField(upload_to='prescription_pdfs')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    qr = models.CharField(max_length=200)
    date_uploaded = models.DateField()

class DocumentSelfIssued(models.Model): #stores individual documents
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='self_uploaded_pdfs')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    qr = models.CharField(max_length=200)
    date_uploaded = models.DateField()

# class Records(models.Model): #stores the records + documents of a patient
#     patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
#     # other details
#     if Document.objects.all():
#         documents = Document.objects.filter(patient = patient).order_by('-pk')

class Allergies(models.Model):
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class HealthConditions(models.Model):
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class TreatmentsandMedicines(models.Model):
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    medicine = models.CharField(max_length=200)
    decription = models.CharField(max_length=200)

class Lifestyle(models.Model):
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    activity = models.CharField(max_length=200) 
    amount = models.CharField(max_length=200) 

class EmergencyContact(models.Model):
  patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
  first_name =  models.CharField(max_length=200)
  last_name =  models.CharField(max_length=200)
  relation =  models.CharField(max_length=200)
  phone_number = models.CharField(max_length=20)

class EmergencyRecord(models.Model):
  patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
  message=models.CharField(max_length=255)
