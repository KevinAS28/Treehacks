from django.db import models
from doctors.models import DoctorProfile
# Create your models here.
class Question(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    text = models.TextField(default = " ")

class Answer(models.Model):
    given_by = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    text = models.TextField(default = " ")