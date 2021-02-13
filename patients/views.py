from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import PatientProfile

#### all the account processes
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
        country = request.POST.get('country','')
        city = request.POST.get('city','')
        date_of_birth = request.POST.get('dob','')
        # to check if person already exists
        sameUser = PatientProfile.objects.filter(mail=mail)
        if sameUser:
            messages.error(request,"Email id already exists")
            return redirect('/')
        sameUser=PatientProfile.objects.filter(fname = fname).filter(lname = lname).filter(country=country).filter(date_of_birth = date_of_birth)
        if sameUser:
            messages.error(request,"Person already exists")
            return redirect('/')

        # to check if password and conf password match
        if password==conf_pass:
            user_obj = PatientProfile.objects.create_user(username = username, first_name = fname, last_name = lname, password = password, email = mail, city = city, date_of_birth=date_of_birth, country = country)
            user_obj.save()

    return redirect('/')

def user_login(request):
    # loginprocess
    if request.method=="POST":
        username = request.POST.get('username','')
        user_password = request.POST.get('password','')

        #authentication
        user = auth.authenticate(username= username, password = user_password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Logged In")
            return redirect('/feed')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('/')

def user_logout(request):
    # logout process
    auth.logout(request)
    messages.success(request,"logged out")
    return redirect('/')

# our services
def services(request):
    # startup page of the application
    return render(request,'patient/our_services.html')

def healthRecord(request, page_section=0):
  patient_id = "unique-identifier"
  patient_name = "Jane S. Doe"
  patient_photo = "/static/img/avatar.png"
  main_display = [
    {'title': 'Date of birth', 'value': "12/02/2021"},
    {'title': 'Sex', 'value': "Female"},
    {'title': 'Pronouns', 'value': "She/Her"},
    {'title': 'Race', 'value': "White"},
    {'title': 'Phone number', 'value': "012345 67890"},
    {'title': 'Email', 'value': "janeDoe2@gmail.com"},
    {'title': 'Address', 'value': "123 Fancy st., City, L12 6UH"},
  ]
  subtitles = [
    {'title': 'Treatments and medicines', 'content': 'None.', 'active': page_section==0, 'page_section':0},
    {'title': 'Health conditions', 'content': 'None.', 'active': page_section==1, 'page_section':1},
    {'title': 'Allergies', 'content': 'Eggs.', 'active': page_section==2, 'page_section':2},
    {'title': 'Lifestyle', 'content': 'Heavy smoker.', 'active': page_section==3, 'page_section':3}
  ]
  url_path = "/".join(request.path.split('/')[:-1])

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
      "url_name": url_path
    }
  )

def emergency(request):
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

#patient records example
def records(request):
  name = "Jane S. Doe"
  their_pic = "/static/img/avatar.png"
  dob = "25/12/1923"
  number = "01234 673412"
  email = "janeDoe2@gmail.com"
  address = "123 Fancy st., City, L12 6UH"

  return render(request,'patient/patient_record.html', {"title": "Example", "their_name": name, "their_photo": their_pic, "dob": dob, "phone": number, "email": email, "address": address})

#patient files example
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