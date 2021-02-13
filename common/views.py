from django.shortcuts import render

def startup(request):
    return render(request, "common/startup.html")

