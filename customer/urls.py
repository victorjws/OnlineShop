from django.urls import path
from django.views.generic import TemplateView

# from .views import LoginView
# from .views import CustomerLoginView
from .views import CustomerLogoutView
from .views import CustomerRegisterView

app_name = 'customer'
urlpatterns = [
    # path('login/', CustomerLoginView.as_view(), name='login'),
    path('login/', TemplateView.as_view(template_name='customer/login.html'),
         name='login'),
    path('logout/', CustomerLogoutView.as_view(), name='logout'),
    path('register/', CustomerRegisterView.as_view(),
         name='register'),
]
