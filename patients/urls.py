from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.startup,name="patientstartup"),
    path('services',views.services,name="patientservices"),
    path('health',views.healthRecord,name="patient_health"),
    path('health/<int:page_section>',views.healthRecord,name="patient_health_var"),
    path('test',views.healthRecord,name="test"),
]