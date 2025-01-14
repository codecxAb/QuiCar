from django.urls import path
from django.conf import settings
from . import views  # Assuming you're importing the views
from django.conf.urls.static import static
from django.urls import path
from .views import create_order

urlpatterns = [
    path("create_order/<int:car_id>/", views.create_order, name="create_order"),
    path('carlist/', views.carList, name='carList'),  # The URL path here is 'carlist/' (lowercase)
    path('car/<str:car_id>/', views.carDetails, name='car_details'),
    path('car_add/', views.car_add, name='car_add'),
    path('add_car/<str:car_id>/', views.add_car, name='add_car'),       
    path('payment_success/', views.payment_success, name='payment_success'),

    # path('initiate-transaction/<int:car_id>/', views.initiate_transaction, name='initiate_transaction'),
    # path('confirm-payment/<int:transaction_id>/', views.confirm_payment, name='confirm_payment'),

    # Other URL patterns
]
# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)