from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'doctors'

urlpatterns = [
    path('',views.startup,name="startup"),
    path('signup',views.signup,name="signup"),
    path('prescribe',views.prescribe,name="give_prescriptions"),
    path('give_prescriptions',views.give_prescriptions,name="give_prescriptions"),
]

