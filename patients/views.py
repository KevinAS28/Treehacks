from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import PatientProfile
from django.views.decorators.csrf import csrf_exempt

#### all the account processes

def scan_face(request):
    pass

def startup(request):
    # startup page of the application
    return render(request,'account/patient_signup.html')

@csrf_exempt
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
        # sameUser = PatientProfile.objects.filter(mail=mail)
        # if sameUser:
        #     messages.error(request,"Email id already exists")
        #     return redirect('/')
        # sameUser=PatientProfile.objects.filter(fname = fname).filter(lname = lname).filter(country=country).filter(date_of_birth = date_of_birth)
        # if sameUser:
        #     messages.error(request,"Person already exists")
        #     return redirect('/')

        # to check if password and conf password match
        if password==conf_pass:
            user_obj = PatientProfile(username = username, label = "patients", city = city, date_of_birth=date_of_birth, country = country)
            user_obj.save()
        else:
            messages.error(request,"Password not match")
            print("password not match")
        
        return redirect('/')

    if request.method=="GET":
        return render(request, "account/patient_signup.html")
    else:
        messages.error(request, "Invalid method")
    

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
    elif request.method=="GET":
        return render(request, "account/patient_login.html")


def user_logout(request):
    # logout process
    auth.logout(request)
    messages.success(request,"logged out")
    return redirect('/')
