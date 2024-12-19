from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from .forms import RentalCarForm
from .models import Transaction, RentalCar
from user_auth.models import CustomUser  # Using CustomUser instead of Dealer now
from django.utils import timezone

# Home view (just a placeholder for now)
def home(request):
    return HttpResponse("Hello World, manage car folder is a great feature!")

def car_add(request):
    return render(request, 'add_car.html')

# List all cars
@csrf_protect
@login_required
def carList(request):
    cars = RentalCar.objects.all()
    return render(request, 'carList.html', {'cars': cars})

# Car details view
def carDetails(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    if not request.user.is_authenticated:
        return redirect(f"{reverse('sign_in')}?next={request.path}")
    return render(request, 'car_details.html', {'car': car})

# Add car view (for dealers)
@csrf_protect
@login_required
def add_car(request):
    try:
        # Check if the logged-in user is a dealer (based on user_type)
        if request.user.user_type != 'dealer':
            messages.error(request, 'You must be a dealer to add cars.')
            return redirect('home')  # Redirect to home if not a dealer
    except CustomUser.DoesNotExist:
        messages.error(request, 'Dealer account not found.')
        return redirect('home')

    if request.method == 'POST':
        form = RentalCarForm(request.POST, request.FILES)  # Make sure to handle FILES for image

        if form.is_valid():
            # Debugging output
            print("Form is valid, saving car...")

            new_car = form.save(commit=False)  # Don't save yet, to add extra fields
            new_car.dealer = request.user  # Link the car to the logged-in user (dealer)
            new_car.save()

            # Debugging output
            print(f"Car {new_car.name} has been added to the database.")

            messages.success(request, f'{new_car.name} has been added successfully!')
            return redirect('dealer_dashboard')  # Redirect to dealer's dashboard after adding the car
        else:
            # If the form is not valid, log the errors
            print("Form errors:", form.errors)
            messages.error(request, "There was an error in your form.")
    else:
        print("Creating a new form... because it is not post")
        form = RentalCarForm()

    return render(request, 'add_car.html', {'form': form})
# # Rent a car and create a transaction
# @login_required
# @csrf_protect
# def initiate_transaction(request, car_id):
#     try:
#         car = RentalCar.objects.get(id=car_id)
#     except RentalCar.DoesNotExist:
#         return JsonResponse({'error': 'Car not found'}, status=404)

#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         # Ensure rental duration is specified
#         if not all([start_date, end_date]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         # Ensure the car is available during the requested period
#         if not Transaction.is_car_available(car, start_date, end_date):
#             return JsonResponse({'error': 'Car is not available for the selected dates'}, status=400)

#         # Calculate rental duration and total cost
#         rental_duration = (timezone.datetime.strptime(end_date, '%Y-%m-%d') - timezone.datetime.strptime(start_date, '%Y-%m-%d')).days
#         if rental_duration <= 0:
#             return JsonResponse({'error': 'Invalid rental duration'}, status=400)

#         total_cost = car.rental_rate * rental_duration

#         # Create the transaction
#         transaction = Transaction.objects.create(
#             user=request.user,
#             car=car,
#             start_date=start_date,
#             end_date=end_date,
#             rental_duration=rental_duration,
#             total_cost=total_cost,
#         )
#         transaction.save()

#         # Initiate payment (UPI ID from dealer)
#         upi_id = transaction.initiate_payment()

#         return JsonResponse({'upi_id': upi_id, 'transaction_id': transaction.id})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

# # Confirm the payment after the user completes it manually
# @login_required
# @csrf_protect
# def confirm_payment(request, transaction_id):
#     try:
#         transaction = Transaction.objects.get(id=transaction_id)
#     except Transaction.DoesNotExist:
#         return JsonResponse({'error': 'Transaction not found'}, status=404)

#     if transaction.payment_status == 'Paid':
#         return JsonResponse({'error': 'Payment already confirmed'}, status=400)

#     # Confirm the payment
#     transaction.payment_status = 'Paid'
#     transaction.status = 'Completed'

#     # Mark car as unavailable
#     car = RentalCar.objects.get(id=transaction.car.id)
#     car.availability_status = False
#     car.save()

#     transaction.save()

#     # Redirect to transaction success page
#     return redirect('transaction_success', transaction_id=transaction.id)
