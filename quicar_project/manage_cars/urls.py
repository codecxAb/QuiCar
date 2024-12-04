from django.urls import path
from . import views  # Assuming you're importing the views

urlpatterns = [
    path('carlist/', views.carList, name='carList'),  # The URL path here is 'carlist/' (lowercase)
    path('car/<int:car_id>/', views.carDetails, name='car_details'),
    # Other URL patterns
]
