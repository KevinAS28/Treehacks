from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'doctors'

urlpatterns = [
    path('signup',views.signup,name="doctor_signup"),
    path('search', views.searchPatients, name="search_patients"),
    path('view', views.viewPatient, name="view_patient"),
    path('view/<int:page_section>', views.viewPatient, name="view_patient"),
    path('emergency', views.view_emergency, name="view_emergency"),
    path('emergency/<int:page_section>', views.view_emergency, name="view_emergency"),
    path('files', views.documents, name="patient_files"), 

    path('prescribe',views.prescribe,name="give_prescriptions"),
    path('give_prescriptions',views.give_prescriptions,name="give_prescriptions"),
]

