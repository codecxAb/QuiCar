from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("Hello World manage car folder a achi")

def carList(request):
    # Hardcoded list of cars with details (name, image URL, price, and unique ID)
    cars = [
        {
            'id': 1,
            'name': 'Tesla Model S',
            'image': 'https://www.tesla.com/sites/default/files/modelsx-new/social/model-s-hero-social.jpg',
            'price': '$79,990'
        },
        {
            'id': 2,
            'name': 'Ford Mustang',
            'image': 'https://static.overfuel.com/dealers/trust-auto/image/2020-ford-mustang-shelby-gt350-heritage-edition-3-1024x640.jpg',
            'price': '$55,000'
        },
        {
            'id': 3,
            'name': 'Chevrolet Camaro',
            'image': 'https://www.motortrend.com/uploads/sites/5/2017/06/2018-Chevrolet-Camaro-ZL1-1LE-front-three-quarter-in-motion-04-e1498503636653.jpg?w=768&width=768&q=75&format=webp',
            'price': '$45,000'
        },
        {
            'id': 4,
            'name': 'BMW M3',
            'image': 'https://cdn.motor1.com/images/mgl/1ZQrxK/s1/2023-bmw-m3-cs-first-drive-review.webp',
            'price': '$70,000'
        },
        {
            'id': 5,
            'name': 'Audi A4',
            'image': 'https://hips.hearstapps.com/hmg-prod/images/2021-audi-a4-45-tfsi-quattro-104-1607927016.jpg?crop=0.450xw:0.380xh;0.226xw,0.399xh&resize=2048:*',
            'price': '$40,000'
        },
        {
            'id': 6,
            'name': 'Mercedes-Benz C-Class',
            'image': 'https://images.indianexpress.com/2018/09/mercedes-c-class.jpg',
            'price': '$43,000'
        },
        {
            'id': 7,
            'name': 'Porsche 911',
            'image': 'https://economictimes.indiatimes.com/thumb/msid-110533985,width-1200,height-900,resizemode-4,imgsize-58280/porsche.jpg?from=mdr',
            'price': '$100,000'
        },
        {
            'id': 8,
            'name': 'Lexus RX 350',
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZH0TmHOnzaLJd5Sw1CXRiNBFhHKiuqht5Sg&s',
            'price': '$45,000'
        },
    ]

    # You can handle pagination here if needed

    return render(request, 'carList.html', {'cars': cars})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import RentalCar  # Import the RentalCar model

def carDetails(request, car_id):
    # Fetch the car object from the database
    car = get_object_or_404(RentalCar, id=car_id)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to sign-in page and include the current URL as 'next'
        return redirect(f"{reverse('sign_in')}?next={request.path}")

    # Render the car details page if authenticated
    return render(request, 'car_details.html', {'car': car})


from django.shortcuts import render, redirect
from .forms import RentalCarForm
from django.shortcuts import render, redirect
from .models import RentalCar
from django.contrib import messages

def add_car(request):
    if request.method == 'POST':
        # Extract form data from request
        name = request.POST['name']
        image = request.FILES['image']
        price = request.POST['price']
        description = request.POST['description']
        year = request.POST['year']
        engine = request.POST['engine']
        # mileage = request.POST['mileage']
        location = request.POST['location']
        rental_rate = request.POST.get('rental_rate', None)
        rental_duration = request.POST.get('rental_duration', None)
        car_type = request.POST['car_type']

        # Create a new RentalCar object
        new_car = RentalCar(
            name=name,
            image=image,
            price=price,
            description=description,
            year=year,
            engine=engine,
            # mileage=mileage,
            location=location,
            rental_rate=rental_rate,
            rental_duration=rental_duration,
            car_type=car_type,
            
        )

        # Save to database
        new_car.save()

        # Show a success message
        messages.success(request, f'{new_car.name} has been added successfully!')

        return redirect('car_list')  # Redirect to a car listing page after saving the car

    return render(request, 'add_car.html')
