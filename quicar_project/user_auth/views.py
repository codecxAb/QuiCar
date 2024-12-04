from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'home.html')

# def signin(request):
#     return render(request,'signin.html')

# def signup(request):
#    return render(request,'signup.html')

# user_auth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib import messages

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard after successful sign-in
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('signin')  # Redirect to sign-in page after successful sign-up
    
    return render(request, 'signup.html')
    
   return render(request,'signup.html')

def carList(request):
   return render(request,'carList.html')

def signout(request):
    logout(request)
    return redirect('signin')  # Redirect to sign-in page after logout



# def signout(request):
    # return HttpResponse("Hello World auth folder a achi")

# def dashboard(request):
    # return HttpResponse("Hello World auth folder a achi")