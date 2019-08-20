from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_decode_handler

from customer.models import Customer
from order.serializer import CartExistSerializer
from product.models import Product
from .models import Cart
from .models import Order
from .serializer import CartSerializer
from .serializer import OrderSerializer


class OrderListAPI(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.auth
        customer = jwt_decode_handler(customer)
        customer = customer.get('email')

        queryset = Order.objects.filter(customer__email=customer)
        return queryset


class CartListAPI(ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.pk
        queryset = Cart.objects.filter(customer=customer)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data['customer_id'] = request.user.pk
        return self.create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     request.data['product'] = Product.object.get(
    #         pk=request.data['product'])
    #
    #     request.data['customer'] = Customer.objects.get(
    #         pk=request.data['customer'])
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer.is_valid(raise_exception=True))
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                     headers=headers)


class CartExistCheckAPI(GenericAPIView):
    serializer_class = CartExistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.pk
        product = self.request.query_params.get('product_id', None)
        queryset = Cart.objects.filter(customer=customer, product=product)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            instance = {'result': 1}
        else:
            instance = {'result': 0}
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(serializer.data)


# class CartRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         customer = self.request.user.pk
#         product = self.request.query_params.get('product_id', None)
#         queryset = Cart.objects.filter(customer=customer, product=product)
#         return queryset
