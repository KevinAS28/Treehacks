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
