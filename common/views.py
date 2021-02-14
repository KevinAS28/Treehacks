from django.shortcuts import render, redirect
from .models import Question, Answer
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

def contact_us(request):
  return render(request, "common/contact_us.html")

def forum(request):
  qna = Question.objects.all().order_by('-pk')
  objs = []
  for question in qna:
      answers = Answer.objects.filter(question = question).order_by('-pk')
      objs.append({'question':question,'answers':answers})
  # for obj in objs:
  #   print(obj.question.text)
  return render(request, 'common/forum.html',{'objs':objs})

def question(request, questionId):
  print(questionId)
  ques = Question.objects.get(id = int(questionId))
  # answers = Answer.objects.filter(question = question)
  return render(request, 'common/question.html',{'question':ques}) 
  # return redirect('/')