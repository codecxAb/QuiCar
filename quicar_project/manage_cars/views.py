from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
# from .models import RentalCar
from .forms import RentalCarForm
from django.http import JsonResponse
from .models import Transaction, RentalCar
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Hello World manage car folder a achi")

@csrf_protect
@login_required
def carList(request):
    cars = RentalCar.objects.all()
    return render(request, 'carList.html', {'cars': cars})

def carDetails(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    if not request.user.is_authenticated:
        return redirect(f"{reverse('sign_in')}?next={request.path}")
    return render(request, 'car_details.html', {'car': car})

@csrf_protect
@login_required
def add_car(request):
    if request.method == 'POST':
        form = RentalCarForm(request.POST, request.FILES)
        if form.is_valid():
            new_car = form.save()
            messages.success(request, f'{new_car.name} has been added successfully!')
            return render(request,'dealer_Dashboard.html')
    else:
        form = RentalCarForm()
    return render(request, 'add_car.html', {'form': form})


@login_required
def initiate_transaction(request, car_id):
    """ Initiates a rental transaction. """
    try:
        car = RentalCar.objects.get(id=car_id)
    except RentalCar.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        rental_duration = request.POST.get('rental_duration')

        if not all([start_date, end_date, rental_duration]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            rental_duration = int(rental_duration)
        except ValueError:
            return JsonResponse({'error': 'Invalid rental duration'}, status=400)

        total_cost = car.rental_rate * rental_duration

        transaction = Transaction.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            rental_duration=rental_duration,
            total_cost=total_cost,
        )

        upi_id = transaction.initiate_payment()

        return JsonResponse({'upi_id': upi_id, 'transaction_id': transaction.id})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def confirm_payment(request, transaction_id):
    """ Confirms the payment once the user has made the payment manually via UPI. """
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)

    transaction.payment_status = 'Paid'
    transaction.status = 'Completed'

    car = RentalCar.objects.get(id=transaction.car.id)
    car.availability_status = False
    car.save()

    transaction.save()

    return redirect('transaction_success')