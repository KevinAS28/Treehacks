from django import forms
from .models import DoctorProfile


class DoctorCreation(forms.ModelForm):
  class Meta:
    model = DoctorProfile
    exclude = ['user']

class SignUpForm(forms.Form):
  first_name = forms.CharField(max_length=100)
  last_name = forms.CharField(max_length=100)
  email = forms.EmailField()