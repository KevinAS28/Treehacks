from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions
from django.contrib.auth.decorators import login_required, user_passes_test
# ----------------------------------------------------------------------------------------------------#
# Patients Account access
def startup(request):
    # startup page of the application
    return render(request,'account/patient_signup.html')

def signup(request):
  # signup process
  if request.method=='POST':
    # checks if request method is POST
    username = request.POST.get('username','')
    mail = request.POST.get('email','')
    fname = request.POST.get('fname','')
    lname = request.POST.get('lname','')
    password = request.POST.get('password','')
    conf_pass = request.POST.get('confpassword','')
    addressline1 = request.POST.get('addressline1','')
    addressline2 = request.POST.get('addressline2','')
    country = request.POST.get('country','')
    city = request.POST.get('city','')
    date_of_birth = request.POST.get('dob','')
    # to check if person already exists
    # sameUser=User.objects.filter(fname = fname, lname = lname)
    # for user in sameUser:
    #     if PatientProfile.objects.filter(user = user, country = country, city = city):
    #         messages.error(request,"Person already exists")
    #         return redirect('/')

    # to check if password and conf password match
    if password==conf_pass:
      user_obj = User.objects.create_user(username = username, first_name = fname, last_name = lname, password = password, email = mail)
      user_obj.save()
      patient_obj = PatientProfile(user = user_obj,  city = city, date_of_birth=date_of_birth, country = country, addressline1 = addressline1, addressline2 = addressline2)
      patient_obj.save()
    return redirect('/')
  else:
    return render(request,'account/patient_signup.html')

def documents(request):
    patient_id = request.POST.get('patient_id')
    patient = PatientProfile.objects.get(id = patient_id)
    all_docs = Document.objects.filter(patient = patient)
    return render(request, "prescriptions/documents.html", all_docs)

# our services
def services(request):
    # about us page of the application
    return render(request,'patient/our_services.html')

# ----------------------------------------------------------------------------------------------------#
# Patients Health Records

# format records
def TreatmentsandMedicinesToString(patient_id):
  objs = Lifestyle.objects.filter(id=patient_id)
  output = []
  for obj in objs:
    output.append("%s: %s" % (obj.medicine, obj.description))

  if output == []:
    return "None"
  return "<br/>".join(output)

def HealthConditionsToString(patient_id):
  objs = HealthConditions.objects.filter(id=patient_id)
  output = []
  for obj in objs:
    output.append(obj.name)

  if output == []:
    return "None"
  return "<br/>".join(output)

def AllergiesToString(patient_id):
  objs = Allergies.objects.filter(id=patient_id)
  output = []
  for obj in objs:
    output.append(obj.name)

  if output == []:
    return "None"
  return "<br/>".join(output)

def LifestyleToString(patient_id):
  objs = Lifestyle.objects.filter(id=patient_id)
  output = []
  for obj in objs:
    output.append("%s: %s" % (obj.activity, obj.amount))

  if output == []:
    return "Unknown"
  return "<br/>".join(output)

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
  patient_photo = "/static/img/avatar.png"
  main_display = [
    {'title': 'Date of birth', 'value': patient.date_of_birth},
    {'title': 'Sex', 'value': patient.sex},
    {'title': 'Pronouns', 'value': patient.pronouns},
    {'title': 'Race', 'value': patient.race},
    {'title': 'Phone number', 'value': patient.number},
    {'title': 'Email', 'value': user.email},
    {'title': 'Address', 'value': "%s, %s, %s, %s, %s" % (patient.addressline1, patient.addressline2, patient.city, patient.country, patient.zipcode)},
  ]


  subtitles = [
    {'title': 'Treatments and medicines', 'content': HealthConditionsToString(patient_id), 'active': page_section==0, 'page_section':0},
    {'title': 'Health conditions', 'content': HealthConditionsToString(patient_id), 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': AllergiesToString(patient_id), 'active': page_section==2, 'page_section':2},
    {'title': 'Lifestyle', 'content': LifestyleToString(patient_id), 'active': page_section==3, 'page_section':3}
  ]

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
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path
    }
  )

@login_required
def emergency(request, page_section=0):
  patient_id = "unique-identifier"
  patient_name = "Jane S. Doe"
  patient_photo = "/static/img/avatar.png"
  content = "Don't let me die. Very broken bones. Handle with care. Do not ship internationally."

  return render(
    request, 
    'patient/profile_string.html',
    {
      'title': "Your health record",
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "content": content
    }
  )

#patient files example
@login_required
def files(request):
  records = [
    {
      "name": "Test.jpg",
      "description": "A test image file.",
      "qr": "qr.jpg",
      "authorisedBy": "Dr Clever",
      "date": "13/02/2021"
    }
  ]
  return render(request,'patient/files.html', {"title": "Example", "records": records})

@login_required
def prescriptions(request):
    return render(request,'patient/files.html')

@login_required
def tests(request):
    return render(request,'patient/files.html')

@login_required
def otherFiles(request):
    return render(request,'patient/files.html')
