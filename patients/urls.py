from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "patients_app"

urlpatterns = [
    path('',views.startup,name="patientstartup"),
    path('signup/', views.signup, name="patientsignup")
]