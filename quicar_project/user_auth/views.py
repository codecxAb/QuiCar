from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser

# Home page view
def home(request):
    return render(request, 'home.html')

# Sign in view (customer or dealer)
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type (customer or dealer)

        # Authenticate the user based on email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Successfully authenticated, check user type
            login(request, user)

            if user.user_type == "customer":
                # Redirect to the customer's dashboard or car list if user is a customer
                return redirect('carList')  # Replace with your customer-specific page URL

            elif user.user_type == "dealer":
                # Redirect to the dealer dashboard if user is a dealer
                return redirect('dealer_dashboard')  # Replace with your dealer dashboard URL

            else:
                # If the user_type is neither customer nor dealer, show error
                messages.error(request, "Invalid user type.")
                return render(request, 'signin.html')

        else:
            # If authentication fails, show error message
            messages.error(request, 'Invalid email or password')

    return render(request, 'signin.html')

# Sign-up view for both customers and dealers
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Get the user type (customer or dealer)
        
        if not email or not password or not user_type:
            messages.error(request, "Please fill all fields.")
            return render(request, 'signup.html')

        try:
            # Check if username already exists (assuming email as username)
            if CustomUser.objects.filter(username=email).exists():
                messages.error(request, "Username already exists. Please choose another one.")
                return redirect('signup')

            # Create the user
            user = CustomUser.objects.create_user(username=email, email=email, password=password, user_type=user_type)
            user.save()

            # Collect additional data based on user type
            name = request.POST.get('name')
            contact_number = request.POST.get('contact_number')

            # Check for required fields for customer or dealer
            if not name or not contact_number:
                messages.error(request, "Please fill all required fields.")
                return render(request, 'signup.html')

            # Save additional fields for both customer and dealer
            user.name = name
            user.contact_number = contact_number
            user.save()

            # After successful creation, redirect based on user type
            if user.user_type == "dealer":
                # Dealer-specific logic (e.g., redirect to dealer dashboard)
                messages.success(request, 'Dealer account created successfully! Welcome to our dealer community.')
                return redirect('dealer_dashboard')

            elif user.user_type == "customer":
                # Customer-specific logic (e.g., redirect to customer dashboard or car list)
                messages.success(request, 'Customer account created successfully! Please sign in.')
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
