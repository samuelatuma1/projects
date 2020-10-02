#Make the necessary imports

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.loginPage, name='loginPage'),
    path('menu/', views.menu, name='menu'),
    path('getmenu/<str:names>/', views.getmenu, name='getmenu'),
    path('cart/', views.cart, name='cart'),
    path('purchased/', views.purchased, name='purchased'),
    path('bought/', views.bought, name='bought'),
    path('requested', views.requested, name='requested'),
    path('adminDetails/', views.adminDetails, name='adminDetails'),
    path('displaymsg/', views.displaymsg, name='displaymsg'),
    path('logoutView/', views.logoutView, name='logoutView'),
    path('pract/', views.pract, name='pract')
    
]