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
# from .manage_cars.views import carList
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login 
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

# from django.core.paginator import Paginator
# from django.shortcuts import render

# from django.shortcuts import render

# from django.shortcuts import render

# def carList(request):
#     # Hardcoded list of cars with details (name, image URL, price, and unique ID)
#     cars = [
#         {
#             'id': 1,
#             'name': 'Tesla Model S',
#             'image': 'https://www.tesla.com/sites/default/files/modelsx-new/social/model-s-hero-social.jpg',
#             'price': '$79,990'
#         },
#         {
#             'id': 2,
#             'name': 'Ford Mustang',
#             'image': 'https://static.overfuel.com/dealers/trust-auto/image/2020-ford-mustang-shelby-gt350-heritage-edition-3-1024x640.jpg',
#             'price': '$55,000'
#         },
#         {
#             'id': 3,
#             'name': 'Chevrolet Camaro',
#             'image': 'https://www.motortrend.com/uploads/sites/5/2017/06/2018-Chevrolet-Camaro-ZL1-1LE-front-three-quarter-in-motion-04-e1498503636653.jpg?w=768&width=768&q=75&format=webp',
#             'price': '$45,000'
#         },
#         {
#             'id': 4,
#             'name': 'BMW M3',
#             'image': 'https://cdn.motor1.com/images/mgl/1ZQrxK/s1/2023-bmw-m3-cs-first-drive-review.webp',
#             'price': '$70,000'
#         },
#         {
#             'id': 5,
#             'name': 'Audi A4',
#             'image': 'https://hips.hearstapps.com/hmg-prod/images/2021-audi-a4-45-tfsi-quattro-104-1607927016.jpg?crop=0.450xw:0.380xh;0.226xw,0.399xh&resize=2048:*',
#             'price': '$40,000'
#         },
#         {
#             'id': 6,
#             'name': 'Mercedes-Benz C-Class',
#             'image': 'https://images.indianexpress.com/2018/09/mercedes-c-class.jpg',
#             'price': '$43,000'
#         },
#         {
#             'id': 7,
#             'name': 'Porsche 911',
#             'image': 'https://economictimes.indiatimes.com/thumb/msid-110533985,width-1200,height-900,resizemode-4,imgsize-58280/porsche.jpg?from=mdr',
#             'price': '$100,000'
#         },
#         {
#             'id': 8,
#             'name': 'Lexus RX 350',
#             'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZH0TmHOnzaLJd5Sw1CXRiNBFhHKiuqht5Sg&s',
#             'price': '$45,000'
#         },
#     ]

#     # You can handle pagination here if needed

#     return render(request, 'carList.html', {'cars': cars})


# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse

# def carDetails(request, car_id):
#     # Hardcoded list of cars with full details
#     cars = [
#         {'id': 1, 'name': 'Tesla Model S', 'image': 'https://www.tesla.com/sites/default/files/modelsx-new/social/model-s-hero-social.jpg', 'price': '$79,990', 'description': 'The Tesla Model S is an all-electric luxury sedan with impressive range and acceleration.', 'year': '2023', 'engine': 'Electric', 'mileage': 'N/A'},
#         {'id': 2, 'name': 'Ford Mustang', 'image': 'https://static.overfuel.com/dealers/trust-auto/image/2020-ford-mustang-shelby-gt350-heritage-edition-3-1024x640.jpg', 'price': '$55,000', 'description': 'The Ford Mustang is an iconic American muscle car known for its powerful engines and sharp handling.', 'year': '2020', 'engine': '5.2L V8', 'mileage': '15,000 miles'},
#         {'id': 3, 'name': 'Chevrolet Camaro', 'image': 'https://www.motortrend.com/uploads/sites/5/2017/06/2018-Chevrolet-Camaro-ZL1-1LE-front-three-quarter-in-motion-04-e1498503636653.jpg?w=768&width=768&q=75&format=webp', 'price': '$45,000', 'description': 'The Chevrolet Camaro is a high-performance sports car with a strong legacy in motorsports and street racing.', 'year': '2018', 'engine': '6.2L V8', 'mileage': '20,000 miles'},
#         {'id': 4, 'name': 'BMW M3', 'image': 'https://cdn.motor1.com/images/mgl/1ZQrxK/s1/2023-bmw-m3-cs-first-drive-review.webp', 'price': '$70,000', 'description': 'The BMW M3 is a performance-oriented version of the BMW 3 Series, known for its exceptional handling and power.', 'year': '2023', 'engine': '3.0L I6', 'mileage': '10,000 miles'},
#         {'id': 5, 'name': 'Audi A4', 'image': 'https://hips.hearstapps.com/hmg-prod/images/2021-audi-a4-45-tfsi-quattro-104-1607927016.jpg?crop=0.450xw:0.380xh;0.226xw,0.399xh&resize=2048:*', 'price': '$40,000', 'description': 'The Audi A4 is a luxury compact sedan with a stylish design and advanced technology features.', 'year': '2021', 'engine': '2.0L I4', 'mileage': '12,000 miles'},
#         {'id': 6, 'name': 'Mercedes-Benz C-Class', 'image': 'https://images.indianexpress.com/2018/09/mercedes-c-class.jpg', 'price': '$43,000', 'description': 'The Mercedes-Benz C-Class is a luxury sedan offering a comfortable ride, premium interior, and strong performance.', 'year': '2019', 'engine': '2.0L I4', 'mileage': '30,000 miles'},
#         {'id': 7, 'name': 'Porsche 911', 'image': 'https://economictimes.indiatimes.com/thumb/msid-110533985,width-1200,height-900,resizemode-4,imgsize-58280/porsche.jpg?from=mdr', 'price': '$100,000', 'description': 'The Porsche 911 is a legendary sports car known for its exceptional driving dynamics and iconic design.', 'year': '2022', 'engine': '3.0L I6', 'mileage': '5,000 miles'},
#         {'id': 8, 'name': 'Lexus RX 350', 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZH0TmHOnzaLJd5Sw1CXRiNBFhHKiuqht5Sg&s', 'price': '$45,000', 'description': 'The Lexus RX 350 is a luxury SUV offering a smooth ride, a high-quality interior, and plenty of tech features.', 'year': '2020', 'engine': '3.5L V6', 'mileage': '25,000 miles'},
#     ]
    
#     # Get the car object by ID or return a 404 if not found
#     car = get_object_or_404(cars, id=car_id)

#     if not request.user.is_authenticated:
#         # Redirect to sign-in page and include the current URL as 'next'
#         return redirect(f"{reverse('sign_in')}?next={request.path}")

#     # Render the car details page if authenticated
#     return render(request, 'car_details.html', {'car': car})
