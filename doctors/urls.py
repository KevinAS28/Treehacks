from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'doctors'

urlpatterns = [
    path('signup',views.signup,name="doctor_signup"),
    path('prescribe',views.prescribe,name="give_prescriptions"),
    path('give_prescriptions',views.give_prescriptions,name="give_prescriptions"),
]

