from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.startup,name="patient_startup"),
    path('signup',views.signup,name="patient_signup"),
    # path('/mydocuments',views.documents,name="patientstartup"),
]