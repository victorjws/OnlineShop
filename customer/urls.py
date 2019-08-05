from django.contrib import admin
from django.urls import path

from customer.views import CustomerLoginView
from customer.views import CustomerLogoutView
from customer.views import CustomerRegisterView

urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('logout/', CustomerLogoutView.as_view(), name='logout'),
    path('register/', CustomerRegisterView.as_view(),
         name='register'),
]
