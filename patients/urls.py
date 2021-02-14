from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "patients_app"

urlpatterns = [

    path('tester/', views.tester, name='test'),

    path('signup/',views.signup,name="patient_signup"),
    path('aboutus',views.services,name="about_us"),


    path('alertContacts/', views.alertContacts, name="alert_contacts"),

    path('health/info', views.healthRecord, name="patient_health"),
    path('health/info/edit', views.editHealthRecord, name="edit_health"),
    path('health/info/<int:page_section>', views.healthRecord, name="patient_health"),

    path('health/info/add_treatments', views.add_treatments, name="add_treatments"),
    path('health/info/add_health_condition', views.add_health_condition, name="add_health_condition"),
    path('health/info/add_allergies', views.add_allergies, name="add_allergies"),
    path('health/info/add_lifestyle', views.add_lifestyle, name="add_lifestyle"),

    path('health/emergency', views.emergency, name="patient_emergency"),
    path('health/emergency/add_contact', views.addEmergencyContact, name="emergency_contacts"),
    path('health/emergency/edit', views.editEmergency, name="edit_emergency"),
    path('health/emergency/<int:page_section>', views.emergency, name="patient_emergency"),

    path('health/files', views.documents, name="patient_files"), 
    path('health/upload_files', views.upload_doc, name="upload_doc"),

    path('shared/prescriptions', views.prescriptions, name="shared_prescriptions"),
    path('shared/tests', views.tests, name="shared_tests"),
    path('shared/other', views.otherFiles, name="shared_other"),

    path('add_face', views.add_face, name='add_face'),
    path('add_face_src', views.add_face_src, name='add_face_src'),
    # path('add_face', views.add_face, name='add_face'),
    # path('add_face_src', views.add_face_src, name='add_face_src'),
    # path('auth_face', views.auth_face, name='auth_face'),
    # path('auth_face_src', views.auth_face_src, name='auth_face_src'),


]