from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'home.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
   return render(request,'signup.html')

def signout(request):
    return HttpResponse("Hello World auth folder a achi")

def dashboard(request):
    return HttpResponse("Hello World auth folder a achi")