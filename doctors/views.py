from django.shortcuts import render, redirect
from patients.models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions, EmergencyRecord, EmergencyContact, DocumentSelfIssued
from django.contrib.auth.models import User, auth, Group
from .models import DoctorProfile
from django import forms
from .forms import DoctorCreation, SignUpForm
from django.contrib.auth.forms import UserCreationForm
import time
import datetime

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.template import loader, Context

# Create your views here.
def isDoctor(user):
  return  user.groups.filter(name="Doctor")

def signup(request):
  form = SignUpForm()
  form1 = UserCreationForm()
  form2 = DoctorCreation()
  if request.POST:
    form = SignUpForm(request.POST)
    form1 = UserCreationForm(request.POST)
    form2 = DoctorCreation(request.POST, request.FILES)
    if form.is_valid() and form1.is_valid() and form2.is_valid():
      user = form1.save(commit=False)
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.email = form.cleaned_data['email']
      user.save()

      dr_group = Group.objects.get(name='Doctor')
      dr = form2.save(commit=False)
      dr.user = user
      dr.save()
      dr_group.user_set.add(user)
      loggedIn = authenticate(username=form1.cleaned_data['username'], password=form1.cleaned_data['password1'])
      login(request, loggedIn)
      return redirect('/')

      # request.session["email"] = "test@mail.com"#form.cleaned_data['email']
      # return render(request, 'vid_base_add.html', )

  return render(
    request,
    'account/signup.html',
    {'form': form, 'form1': form1, 'form2': form2}
  )

@user_passes_test(isDoctor)
@login_required
def prescribe(request):
    return render(request,'account/doctor_prescribe.html')

@user_passes_test(isDoctor)
@login_required
def give_prescriptions(request):
    form = ProfileForm(request.FILES)
    if form.is_valid():
        pdfFileObj = form.cleaned_data['doc']
        doctor_id = request.POST.get('did','')
        doctor = DoctorProfile.objects.get(id = doctor_id)
        # doctor = request.user
        patient_id = request.POST.get('pid','')
        patient = PatientProfile.objects.get(id = patient_id)
        post_obj = Document(patient= patient, doctor= doctor, pdf = pdfFileObj)
        post_obj.save()
        return redirect('/')

@user_passes_test(isDoctor)
@login_required
def view_records(request):
    option = request.POST.get('option')
    patient_id = request.POST.get('patient_id')
    patient = PatientProfile.object.get(id = patient_id)
    if option==1:
        treatments_medicines = TreatmentsandMedicines.objects.filter(patient = patient)
        return render(request, "prescriptions/patient_personal_record.html", {patient, treatments_medicines})
    if option==2:
        health_conditions = HealthConditions.objects.filter(patient = patient)
        return render(request, "prescriptions/patient_personal_record.html", {patient, health_conditions})
    if option==3:
        allergies = Allergies.objects.filter(patient = patient)
        return render(request, "prescriptions/patient_personal_record.html", {patient, allergies})
    if option==4:
        lifestyle = Lifestyle.objects.filter(patient = patient)
        return render(request, "prescriptions/patient_personal_record.html", {patient, lifestyle})
    return render(request, "prescriptions/patient_personal_record.html", {patient})

@user_passes_test(isDoctor)
@login_required
def searchPatients(request):
  patients = PatientProfile.objects.all()
  print(patients)

  if request.POST:
    for key in request.POST.keys():
      if key.startswith("patient_"):
        pk = int(key.split('patient_')[1])
        request.session['patient'] = pk
        return redirect(reverse("doctor:view_patient"))
    if 'search' in request.POST:
      search_term = request.POST['search']
      patients = PatientProfile.objects.filter(user__username__contains=search_term)

  records = []
  for patient in patients:
    records.append({
      'username': patient.user.username,
      'name': "%s %s" % (patient.user.first_name, patient.user.last_name),
      'dob': patient.date_of_birth,
      'postcode': patient.zipcode,
      'pk': patient.pk
    })
  return render(request, "doctor/rowsOfPatients.html", {'records': records})

def getPatient(request):
  pk = request.session['patient']
  return PatientProfile.objects.get(pk=pk)

# format records
def TreatmentsandMedicinesToString(patient):
  objs = TreatmentsandMedicines.objects.filter(patient=patient)
  output = []
  for obj in objs:
    output.append("%s: %s" % (obj.medicine, obj.decription))

  if output == []:
    return "None"
  return "\n".join(output)

def HealthConditionsToString(patient):
  objs = HealthConditions.objects.filter(patient=patient)
  output = []
  for obj in objs:
    output.append(obj.name)

  if output == []:
    return "None"
  return "\n".join(output)

def AllergiesToString(patient):
  objs = Allergies.objects.filter(patient=patient)
  output = []
  for obj in objs:
    output.append(obj.name)

  if output == []:
    return "None"
  return "\n".join(output)

def LifestyleToString(patient):
  objs = Lifestyle.objects.filter(patient=patient)
  output = []
  for obj in objs:
    output.append("%s: %s" % (obj.activity, obj.amount))

  if output == []:
    return "Unknown"
  return "\n".join(output)


@user_passes_test(isDoctor)
@login_required
def viewPatient(request, page_section=0):
  patient = getPatient(request)

  patient_id = patient.id
  user = patient.user

  patient_name = "%s %s" % (user.first_name, user.last_name)
  patient_photo = patient.profilePicture.url
  main_display = [
    {'title': 'Date of birth', 'value': patient.date_of_birth},
    {'title': 'Sex', 'value': patient.sex},
    {'title': 'Pronouns', 'value': patient.pronouns},
    {'title': 'Race', 'value': patient.race},
    {'title': 'Phone number', 'value': patient.phone_number},
    {'title': 'Email', 'value': user.email},
    {'title': 'Address', 'value': "%s, %s, %s, %s, %s" % (patient.addressline1, patient.addressline2, patient.city, patient.country, patient.zipcode)},
  ]


  subtitles = [
    {'title': 'Treatments and medicines', 'content': TreatmentsandMedicinesToString(patient), 'active': page_section==0, 'page_section':0},
    {'title': 'Health conditions', 'content': HealthConditionsToString(patient), 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': AllergiesToString(patient), 'active': page_section==2, 'page_section':2},
    {'title': 'Lifestyle', 'content': LifestyleToString(patient), 'active': page_section==3, 'page_section':3}
  ]

  url_path = "doctor:view_patient"

  return render(
    request, 
    'patient/profile_list.html',
    {
      'title': "Patient health record",
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path,
      'doctor': True
    }
  )


@user_passes_test(isDoctor)
@login_required
def view_emergency(request, page_section=0):
  patient = getPatient(request)

  patient_id = patient.id
  user = patient.user

  patient_name = "%s %s" % (user.first_name, user.last_name)
  patient_photo = patient.profilePicture.url
  main_display = "Don't let me die. Very broken bones. Handle with care. Do not ship internationally."

  emergencySummaryForms = []
  objs = EmergencyRecord.objects.filter(patient=patient)
  if not objs:
    main_display = "Please fill this field with a summary of your conditions."
  else:
    main_display = objs[0].message

  contacts = []
  objs = EmergencyContact.objects.filter(patient=patient)
  for obj in objs:
    contacts.append("%s %s - %s - %s" % (obj.first_name, obj.last_name, obj.relation, obj.phone_number))

  if not contacts:
    contacts = ["Please add at least one emergency contact."]

  subtitles = [
    {'title': 'Emergency Contact', 'content': "\n".join(contacts), 'active': page_section==0, 'page_section':0},
    {'title': 'Health condition details', 'content': HealthConditionsToString(patient), 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': AllergiesToString(patient), 'active': page_section==2, 'page_section':2},
  ]

  if page_section == 0:
    add_link = "emergency_contacts"
  elif page_section == 1:
    add_link = "add_health_condition"
  else:
    add_link = "add_allergies"

  flags = []
  for obj in Allergies.objects.filter(patient=patient):
    flags.append(obj.name)
  for obj in HealthConditions.objects.filter(patient=patient):
    flags.append(obj.name)

  url_path = "doctor:view_emergency"

  return render(
    request, 
    'patient/profile_string.html',
    {
      'title': "Emergency details",
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path,
      "flags": flags,
      'doctor': True
    }
  )

def documents(request):
  patient = getPatient(request)
  docs = DocumentSelfIssued.objects.filter(patient=patient)
  
  records = []
  for doc in docs:
    records.append(
    {
      "pdf": doc.pdf,
      "name": doc.name,
      "description": doc.description,
      "qr": doc.qr,
      "authorisedBy": "%s %s" % (patient.user.first_name, patient.user.last_name),
      "date": doc.date_uploaded
    }
    )
  return render(request,'patient/files.html', {"title": "Files shared by patient", "records": records, 'doctor': True})
