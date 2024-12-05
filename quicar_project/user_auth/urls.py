from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),   
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    path('dealer_dashboard/',views.dealer_dashboard,name='dealer_dashboard'),
    # path('dashboard/',views.dashboard,name='dashboard'),
    # path('carlist/',views.carList,name='carList'),
    # path('cars/', views.carList, name='car_list'),
    # path('car/<int:car_id>/', views.carDetails, name='car_details'),
    # path('car_grid/',views.car_grid,name='car_grid'),
]