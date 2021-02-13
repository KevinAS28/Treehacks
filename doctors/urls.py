from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.startup,name="startup"),
    path('signup',views.signup,name="signup"),
    path('give_prescriptions',views.give_prescriptions,name="give_prescriptions"),
]