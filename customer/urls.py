from django.urls import path
from django.views.generic import TemplateView

from .views import CustomerRegisterView

app_name = 'customer'
urlpatterns = [
    path('login/', TemplateView.as_view(template_name='customer/login.html'),
         name='login'),
    path('register/', CustomerRegisterView.as_view(),
         name='register'),
]
