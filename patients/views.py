from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions

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

def documents(request):
    patient_id = request.POST.get('patient_id')
    patient = PatientProfile.object.get(id = patient_id)
    all_docs = Document.objects.filter(patient = patient)
    return render(request, "prescriptions/documents.html", all_docs)

def records(request):
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

