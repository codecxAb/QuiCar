from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'index.html')

def signin(request):
    return HttpResponse("Hello World auth folder a achi")

def signup(request):
    return HttpResponse("Hello World auth folder a achi")

def signout(request):
    return HttpResponse("Hello World auth folder a achi")

def dashboard(request):
    return HttpResponse("Hello World auth folder a achi")