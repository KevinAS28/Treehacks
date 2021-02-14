from django.shortcuts import render, redirect

def startup(request):
  return render(request, "common/startup.html")

def redirectUser(request):
  user = request.user

  if user.groups.filter(name="Patient"):
    return redirect('patient_health')

  if user.groups.filter(name="Doctor"):
    return redirect('startup')

  if user.groups.filter(name="Administrator"):
    return redirect('startup')

  return redirect('login')