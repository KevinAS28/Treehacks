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


from .models import PatientProfile
from .models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions, EmergencyContact, EmergencyRecord, DocumentSelfIssued
from .forms import PatientCreation, SignUpForm,  AllergiesForm, HealthConditionsForm, TreatmentsandMedicinesForm, LifestyleForm, EmergencyContactForm, EmergencyRecordForm, DocumentSelfIssuedForm

#face recogntion
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import camera_auth, camera_add


#### Facial Recognition Functions
# ----------------------------------------------------------------------------------------------------#


# #Face recognition module. It will take around 30 seconds to run. 
# print("\n\nLoading face recognition modules...")
# FRGraph = FaceRecGraph()
# aligner = AlignCustom()
# extract_feature = FaceFeature(FRGraph)
# face_detect = MTCNNDetect(FRGraph, scale_factor=2)
# print("Done\n\n")

def gen(request, camera):
    while not camera.done:
        frame = camera.get_frame()
        if frame==None:
            break
        
        vid =  (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield vid


    # request.session['test'] = 'YAY'
    # return redirect()

def tester(request):
    # return render(request, 'vid_base_add.html', {'test': request.session['email']})
    def gen1():
          t = loader.get_template('test.html')
          for i in range(100):
            time.sleep(1)
            yield t.render({'test': '<h1>{}</h1>'.format(str(i))})
            
    return StreamingHttpResponse(gen1())
    

def add_face_src(request):
    print("add_face_src: ", request.session["email"])
    frames = gen(request, camera_add.VideoCamera(FRGraph, aligner, extract_feature, face_detect, name=request.session["email"]))
    return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')

def add_face(request):
    return render(request, 'vid_base_add.html')


#### all the account processes
# ----------------------------------------------------------------------------------------------------#
# Patients Account access

# Todo
@login_required
def alertContacts(request):
  return render(request, 'patient/alert_contacts.html')

def signup(request):
  form = SignUpForm()
  form1 = UserCreationForm()
  form2 = PatientCreation()
  if request.POST:
    form = SignUpForm(request.POST)
    form1 = UserCreationForm(request.POST)
    form2 = PatientCreation(request.POST, request.FILES)
    if form.is_valid() and form1.is_valid() and form2.is_valid():
      user = form1.save(commit=False)
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.email = form.cleaned_data['email']
      user.save()

      patient_group = Group.objects.get(name='Patient')
      patient = form2.save(commit=False)
      patient.user = user
      patient.save()
      patient_group.user_set.add(user)
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
      "authorisedBy": "You",
      "date": doc.date_uploaded
    }
    )
  return render(request,'patient/files.html', {"title": "Files you have shared with your doctor", 'add_link': 'patient:upload_doc', "records": records})

def upload_doc(request):
  patient = getPatient(request)
  forms = [DocumentSelfIssuedForm(request.POST or None, request.FILES or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.date_uploaded = datetime.date.today()
        obj.save()
      return redirect(reverse('patient:patient_files'))
  
  contact = {'name': 'Upload a file to share with your doctor', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})

# our services
def services(request):
    # about us page of the application
    return render(request,'patient/our_services.html')


# ----------------------------------------------------------------------------------------------------#
# Patients Health Records

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

@login_required
def getPatient(request):
  user = request.user
  patient = PatientProfile.objects.get(user=user)
  return patient

@login_required
def healthRecord(request, page_section=0):
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

  if page_section == 0:
    add_link = "add_treatments"
  elif page_section == 1:
    add_link = "add_health_condition"
  elif page_section == 2:
    add_link = "add_allergies"
  else:
    add_link = "add_lifestyle"

  try:
    int(request.path.split('/')[-1])
    url_path = "/".join(request.path.split('/')[:-1])
  except ValueError:
    url_path = request.path

  return render(
    request, 
    'patient/profile_list.html',
    {
      'title': "Your health record",
      'edit_link': 'patient:edit_health',
      'add_link': 'patient:%s' % add_link,
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path,
    }
  )

def editHealthRecord(request):
  patient = getPatient(request)

  personalForm = [PatientCreation(request.POST or None, instance=patient)]

  allergiesForms = []
  objs = Allergies.objects.filter(patient=patient)
  for obj in objs:
    allergiesForms.append(AllergiesForm(request.POST or None, instance=obj))

  healthForms = []
  objs = HealthConditions.objects.filter(patient=patient)
  for obj in objs:
    healthForms.append(HealthConditionsForm(request.POST or None, instance=obj))

  treatForms = []
  objs = TreatmentsandMedicines.objects.filter(patient=patient)
  for obj in objs:
    treatForms.append(TreatmentsandMedicinesForm(request.POST or None, instance=obj))

  lifestyleForms = []
  objs = Lifestyle.objects.filter(patient=patient)
  for obj in objs:
    lifestyleForms.append(LifestyleForm(request.POST or None, instance=obj))

  if request.POST:
    valid = True
    for form in allergiesForms + healthForms + treatForms + lifestyleForms:
      valid = form.is_valid() and valid
    if valid:
      for form in allergiesForms + healthForms + treatForms + lifestyleForms:
        form.save()
      return redirect(reverse('patient:patient_health'))
  
  patientData = {'name': 'Personal Details', 'forms': personalForm}
  allergies = {'name': 'Allergies', 'forms': allergiesForms}
  health = {'name': 'Health Conditions', 'forms': healthForms} 
  treat = {'name': 'Treatments and Medicines', 'forms': treatForms}
  lifestyle = {'name': 'Lifestyle', 'forms': lifestyleForms}
  return render(request, 'patient/edit_page.html', {'sections': [patientData, allergies, health, treat, lifestyle]})

def add_treatments(request):
  patient = getPatient(request)
  forms = [TreatmentsandMedicinesForm(request.POST or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.save()
      return redirect(reverse('patient:patient_health'))
  
  contact = {'name': 'Add a treatment or medicine', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})

def add_health_condition(request):
  patient = getPatient(request)
  forms = [HealthConditionsForm(request.POST or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.save()
      return redirect(reverse('patient:patient_health'))
  
  contact = {'name': 'Add a health condition', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})

def add_allergies(request):
  patient = getPatient(request)
  forms = [AllergiesForm(request.POST or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.save()
      return redirect(reverse('patient:patient_health'))
  
  contact = {'name': 'Add an allergy', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})


def add_lifestyle(request):
  patient = getPatient(request)
  forms = [LifestyleForm(request.POST or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.save()
      return redirect(reverse('patient:patient_health'))
  
  contact = {'name': 'Add a part of your lifestyle e.g. smoker: heavy', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})

@login_required
def emergency(request, page_section=0):
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

  try:
    int(request.path.split('/')[-1])
    url_path = "/".join(request.path.split('/')[:-1])
  except ValueError:
    url_path = request.path

  return render(
    request, 
    'patient/profile_string.html',
    {
      'title': "Emergency details",
      'edit_link': 'patient:edit_emergency',
      'add_link': 'patient:%s' % add_link,
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path,
      "flags": flags
    }
  )

def addEmergencyContact(request):
  patient = getPatient(request)
  forms = [EmergencyContactForm(request.POST or None)]

  if request.POST:
    valid = True
    for form in forms:
      valid = form.is_valid() and valid
    if valid:
      for form in forms:
        obj = form.save(commit=False)
        obj.patient = patient 
        obj.save()
      return redirect(reverse('patient:patient_emergency'))
  
  contact = {'name': 'Your emergency contacts', 'forms': forms}
  return render(request, 'patient/edit_page.html', {'sections': [contact]})

def editEmergency(request):
  patient = getPatient(request)

  emergencySummaryForms = []
  objs = EmergencyRecord.objects.filter(patient=patient)
  for obj in objs:
    emergencySummaryForms.append(EmergencyRecordForm(request.POST or None, instance=obj))
  if not obj:
    emergencySummaryForms.append(EmergencyRecordForm(request.POST or None))

  contactForms = []
  objs = EmergencyContact.objects.filter(patient=patient)
  for obj in objs:
    contactForms.append(EmergencyContactForm(request.POST or None, instance=obj))

  allergiesForms = []
  objs = Allergies.objects.filter(patient=patient)
  for obj in objs:
    allergiesForms.append(AllergiesForm(request.POST or None, instance=obj))

  healthForms = []
  objs = HealthConditions.objects.filter(patient=patient)
  for obj in objs:
    healthForms.append(HealthConditionsForm(request.POST or None, instance=obj))

  if request.POST:
    valid = True
    for form in emergencySummaryForms + contactForms + allergiesForms + healthForms:
      valid = form.is_valid() and valid
    if valid:
      for form in emergencySummaryForms + contactForms + allergiesForms + healthForms:
        obj = form.save(commit=False)
        obj.patient = patient
        obj.save()
      return redirect(reverse('patient:patient_emergency'))
  
  emergency = {'name': 'Message to person treating you', 'forms': emergencySummaryForms}
  contact = {'name': 'Your emergency contacts', 'forms': contactForms}
  allergies = {'name': 'Allergies', 'forms': allergiesForms}
  health = {'name': 'Health Conditions', 'forms': healthForms} 
  return render(request, 'patient/edit_page.html', {'sections': [emergency, contact, allergies, health]})




@login_required
def prescriptions(request):
  patient = getPatient(request)

  return render(request,'patient/files.html', {"title": "Your prescriptions", "records": []})

@login_required
def tests(request):
  patient = getPatient(request)

  return render(request,'patient/files.html', {"title": "Your test, scans and z-ray results", "records": []})

@login_required
def otherFiles(request):
  patient = getPatient(request)

  return render(request,'patient/files.html', {"title": "Other files", "records": []})
