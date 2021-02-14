from django import forms
from .models import PatientProfile, Allergies, HealthConditions, TreatmentsandMedicines, Lifestyle, EmergencyContact, EmergencyRecord, DocumentSelfIssued

class PatientCreation(forms.ModelForm):
  class Meta:
    model = PatientProfile
    exclude = ['user']
    widgets = {
      'date_of_birth': forms.TextInput(
        attrs={'type': 'date'}
      ),
    }

class SignUpForm(forms.Form):
  first_name = forms.CharField(max_length=100)
  last_name = forms.CharField(max_length=100)
  email = forms.EmailField()

class AllergiesForm(forms.ModelForm):
  class Meta:
    model = Allergies
    exclude = ['patient']

class HealthConditionsForm(forms.ModelForm):
  class Meta:
    model = HealthConditions
    exclude = ['patient']

class TreatmentsandMedicinesForm(forms.ModelForm):
  class Meta:
    model = TreatmentsandMedicines
    exclude = ['patient']

class LifestyleForm(forms.ModelForm):
  class Meta:
    model = Lifestyle
    exclude = ['patient']

class EmergencyContactForm(forms.ModelForm):
  class Meta:
    model = EmergencyContact
    exclude = ['patient']

class EmergencyRecordForm(forms.ModelForm):
  class Meta:
    model = EmergencyRecord
    exclude = ['patient']

class DocumentSelfIssuedForm(forms.ModelForm):
  class Meta:
    model = DocumentSelfIssued
    exclude = ['patient', 'date_uploaded']