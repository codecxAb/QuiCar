from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

def home(request):
    return render(request, 'home.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type (customer or dealer)
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is a dealer or customer
            if user_type == 'dealer':
                return redirect('dealer_dashboard')  # Redirect to the dealer dashboard
            else:
                return redirect('carList')  # Redirect to the customer car list
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type (customer or dealer)
        
        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # After successful signup, redirect to the appropriate page
        if user_type == 'dealer':
            # You can add extra fields for dealer like a business name etc. if needed
            messages.success(request, 'Account created successfully! Welcome to Our dealer community.')

            return redirect('dealer_dashboard')  # Redirect dealer to the dealer dashboard
        else:
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('signin')  # Redirect to sign-in page after successful sign-up
    
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('home')  # Redirect to sign-in page after logout


def dealer_dashboard(request):
    # This is where the dealer can manage cars (add, edit, delete)
    return render(request, 'dealer_dashboard.html')  # Create this template for the dealer dashboard

