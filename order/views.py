from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework_jwt.utils import jwt_decode_handler

from .models import Cart
from .models import Order
from .serializer import CartSerializer
from .serializer import OrderSerializer


class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.auth
        customer = jwt_decode_handler(customer)
        customer = customer.get('email')

        queryset = Order.objects.filter(customer__email=customer)
        return queryset


class CartListAPI(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # print(self.request.auth)
        customer = self.request.user.pk
        # print(customer)
        queryset = Cart.objects.filter(customer=customer)
        return queryset
