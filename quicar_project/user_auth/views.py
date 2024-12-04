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
    

# def carList(request):
#    return render(request,'carList.html')

def signout(request):
    logout(request)
    return redirect('signin')  # Redirect to sign-in page after logout



def carList(request):
    cars = [
        {
            "name": "Maruti Suzuki Ertiga 2024",
            "image": "https://images.unsplash.com/photo-1517271710308-aa99f1519490?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "rating": 4.24,
            "trips": 28,
            "price_per_hour": 348,
            "total_price": 1392,
            "features": ["Manual", "Petrol", "7 Seats"],
            "distance": "6.3 km away",
            "tag": "ACTIVE FASTAG",
        },
        {
            "name": "Maruti Suzuki Grand Vitara 2024",
            "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "rating": 4.44,
            "trips": 29,
            "price_per_hour": 570,
            "total_price": 2281,
            "features": ["Manual", "Petrol", "5 Seats"],
            "distance": "9.1 km away",
            "tag": "ACTIVE FASTAG",
        },
        # Add more car dictionaries here if needed
    ]

    return render(request, "carList.html", {"cars": cars * 8})  # Duplicate to make 16 cards



# def signout(request):
    # return HttpResponse("Hello World auth folder a achi")

# def dashboard(request):
    # return HttpResponse("Hello World auth folder a achi")