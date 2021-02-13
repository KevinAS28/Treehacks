from django.shortcuts import render, redirect

def startup(request):
    return render(request, "common/startup.html")

def redirectUser(request):
  user = request.user

  return redirect('patient_health')
  
  