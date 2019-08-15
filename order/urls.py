from django.urls import path
from django.views.generic import TemplateView

from .views import OrderListAPI
from .views import CartListAPI

app_name = 'order'
urlpatterns = [
    path('', TemplateView.as_view(template_name='order/checkout.html'),
         name='order-list'),
    path('cart/', TemplateView.as_view(template_name='order/cart.html'),
         name='cart'),
    path('cart-api/', CartListAPI.as_view(), name='cart-api'),
    path('order-api/', OrderListAPI.as_view(), name='order-api'),
]
