from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages

from .models import PatientProfile
from django.views.decorators.csrf import csrf_exempt

from .models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientCreation, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


#### all the account processes

def scan_face(request):
    pass



# ----------------------------------------------------------------------------------------------------#
# Patients Account access

def startup(request):
    # startup page of the application
    return render(request,'account/patient_signup.html')

@csrf_exempt
def signup(request):
    # signup process
#     if request.method=='POST':
#         # checks if request method is POST
#         username = request.POST.get('username','')
#         mail = request.POST.get('email','')
#         fname = request.POST.get('fname','')
#         lname = request.POST.get('lname','')
#         password = request.POST.get('password','')
#         conf_pass = request.POST.get('confpassword','')
#         country = request.POST.get('country','')
#         city = request.POST.get('city','')
#         date_of_birth = request.POST.get('dob','')
        
#         # to check if person already exists
#         # sameUser = PatientProfile.objects.filter(mail=mail)
#         # if sameUser:
#         #     messages.error(request,"Email id already exists")
#         #     return redirect('/')
#         # sameUser=PatientProfile.objects.filter(fname = fname).filter(lname = lname).filter(country=country).filter(date_of_birth = date_of_birth)
#         # if sameUser:
#         #     messages.error(request,"Person already exists")
#         #     return redirect('/')

#         # to check if password and conf password match
#         if password==conf_pass:
#             user_obj = PatientProfile(username = username, label = "patients", city = city, date_of_birth=date_of_birth, country = country)
#             user_obj.save()
#         else:
#             messages.error(request,"Password not match")
#             print("password not match")
        
#         return redirect('/')

#     if request.method=="GET":
#         return render(request, "account/patient_signup.html")
#     else:
#         messages.error(request, "Invalid method")
    

# def user_login(request):
#     # loginprocess
#     if request.method=="POST":
#         username = request.POST.get('username','')
#         user_password = request.POST.get('password','')

#         #authentication
#         user = auth.authenticate(username= username, password = user_password)
#         if user is not None:
#             auth.login(request,user)
#             messages.success(request,"Logged In")
#             return redirect('/feed')
#         else:
#             messages.error(request,"Invalid credentials")
#             return redirect('/')
#     elif request.method=="GET":
#         return render(request, "account/patient_login.html")


# def user_logout(request):
#     # logout process
#     auth.logout(request)
#     messages.success(request,"logged out")
#     return redirect('/')

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
  return render(
    request,
    'account/signup.html',
    {'form': form, 'form1': form1, 'form2': form2}
  )

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
def TreatmentsandMedicinesToString(patient):
  objs = Lifestyle.objects.filter(patient=patient)
  output = []
  for obj in objs:
    output.append("%s: %s" % (obj.medicine, obj.description))

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
    {'title': 'Treatments and medicines', 'content': HealthConditionsToString(patient), 'active': page_section==0, 'page_section':0},
    {'title': 'Health conditions', 'content': HealthConditionsToString(patient), 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': AllergiesToString(patient), 'active': page_section==2, 'page_section':2},
    {'title': 'Lifestyle', 'content': LifestyleToString(patient), 'active': page_section==3, 'page_section':3}
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
      "url_path": url_path,
    }
  )

@login_required
def emergency(request, page_section=0):
  patient = getPatient(request)
  patient_id = patient.id
  user = patient.user

  patient_name = "%s %s" % (user.first_name, user.last_name)
  patient_photo = "/static/img/avatar.png"
  main_display = "Don't let me die. Very broken bones. Handle with care. Do not ship internationally."

  subtitles = [
    {'title': 'Emergency Contact', 'content': "list of contact", 'active': page_section==0, 'page_section':0},
    {'title': 'Health condition details', 'content': HealthConditionsToString(patient), 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': AllergiesToString(patient), 'active': page_section==2, 'page_section':2},
  ]

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
      "id": patient_id,
      "patient_name": patient_name,
      'profile_photo': patient_photo,
      "main_display": main_display,
      'subtitles': subtitles,
      "url_path": url_path,
      "flags": flags
    }
  )

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

