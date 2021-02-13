from django.shortcuts import render, redirect
from patients.models import PatientProfile, Document, TreatmentsandMedicines, Allergies, Lifestyle, HealthConditions
from django.contrib.auth.models import User, auth
from .models import DoctorProfile
from django import forms

# Create your views here.

def startup(request):
    # startup page of the application
    return render(request,'account/doctor_signup.html')

class ProfileForm(forms.Form):
   doc = forms.FileField()

def signup(request):
    # signup process
    if request.method=='POST':
        # checks if request method is POST
        form = ProfileForm(request.FILES)
        if form.is_valid():
            proof = form.cleaned_data['doc']
            username = request.POST.get('username','')
            mail = request.POST.get('email','')
            medical_license_number = request.POST.get('medical_license_number','')
            fname = request.POST.get('fname','')
            lname = request.POST.get('lname','')
            password = request.POST.get('password','')
            conf_pass = request.POST.get('confpassword','')
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
                doctor_obj = DoctorProfile(user = user_obj, proof = proof, city = city, date_of_birth=date_of_birth, country = country, medical_license_number = medical_license_number)
                doctor_obj.save()
    return redirect('/')

class DocForm(forms.Form):
    doc = forms.FileField()

def prescribe(request):
    return render(request,'account/doctor_prescribe.html')

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