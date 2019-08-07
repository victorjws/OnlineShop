from django.urls import path

from .views import CustomerLoginView
from .views import CustomerLogoutView
from .views import CustomerRegisterView

urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('logout/', CustomerLogoutView.as_view(), name='logout'),
    path('register/', CustomerRegisterView.as_view(),
         name='register'),
]
