from django.shortcuts import render, redirect
from .models import Question, Answer
from django.urls import reverse

def startup(request):
  return render(request, "common/startup.html")

def redirectUser(request):
  user = request.user

  if user.groups.filter(name="Patient"):
    return redirect(reverse('patient:patient_health'))

  if user.groups.filter(name="Doctor"):
    return redirect(reverse('startup'))

  if user.groups.filter(name="Administrator"):
    return redirect(reverse('startup'))

  return redirect(reverse('login'))

def contact_us(request):
  return render(request, "common/contact_us.html")

def forum(request):
  qna = Question.objects.all().order_by('-pk')
  objs = []
  for question in qna:
      answers = Answer.objects.filter(question_id = question.id).order_by('-pk')
      objs.append({'question':question,'answers':answers})
  # for obj in objs:
  #   print(obj.question.text)
  return render(request, 'common/forum.html',{'objs':objs})

# def question(request, questionId):
#   print(questionId)
#   ques = Question.objects.get(id = int(questionId))
#   answers = Answer.objects.filter(question_id = ques.id)
#   return render(request, 'common/question.html',{'question':ques, 'answers':answers}) 
#   # return redirect('/')
  