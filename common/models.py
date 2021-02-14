from django.db import models
from doctors.models import DoctorProfile
# Create your models here.
class Question(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    text = models.TextField(default = " ")

class Answer(models.Model):
    given_by = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    question_id = models.IntegerField(default="1")
    date=models.DateTimeField(auto_now_add=True)
    text = models.TextField(default = " ")