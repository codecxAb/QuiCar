from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import RentalCar
from .forms import RentalCarForm

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