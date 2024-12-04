from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),   
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    # path('dashboard/',views.dashboard,name='dashboard'),
    path('carlist/',views.carList,name='carList'),
    # path('car_grid/',views.car_grid,name='car_grid'),
]