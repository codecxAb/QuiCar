from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import Dealer
from django.db import IntegrityError

# Home page view
def home(request):
    return render(request, 'home.html')

# Sign in view (customer or dealer)
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            # Check if the user is a dealer or customer
            try:
                dealer = Dealer.objects.get(user=user)
                # Redirect to dealer dashboard if user is a dealer
                return redirect('dealer_dashboard')
            except Dealer.DoesNotExist:
                # Redirect to the customer car list if user is a customer
                return redirect('carList')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'signin.html')

# Signup view (create user and handle dealer logic)
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type (customer or dealer)
        
        try:
            # Check if username already exists (assuming email as username)
            if User.objects.filter(username=email).exists():
                messages.error(request, "Username already exists. Please choose another one.")
                return redirect('signup')  # Redirect back to the signup page
            
            # Create the user
            if user_type!="dealer":
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()

            # Handle user type and create a Dealer instance if needed
            if user_type == "dealer":
                upi_id = request.POST['upi_id']  # UPI ID field for dealer
                contact_number = request.POST['contact_number']  # Contact number field for dealer

                # Create the Dealer object
                dealer = Dealer.objects.create(
                    # user=user,
                    upi_id=upi_id,
                    name=request.POST.get('name'),  
                    contact_number=contact_number
                )
                dealer.save()
                # Check for custom error messages (from the clean() method in Dealer)
                if hasattr(dealer, 'upi_id_error'):
                    messages.warning(request, dealer.upi_id_error)
                messages.success(request, 'Dealer account created successfully! Welcome to our dealer community.')
                return redirect('dealer_dashboard')  # Redirect dealer to the dealer dashboard
            else:
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('signin')  # Redirect to sign-in page after successful sign-up

        except IntegrityError:
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('signup')
    
    return render(request, 'signup.html')

# Sign out view
def signout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

# Dealer dashboard (manage cars, etc.)
def dealer_dashboard(request):
    # This is where the dealer can manage cars (add, edit, delete)
    return render(request, 'dealer_dashboard.html')  # Create this template for the dealer dashboard
