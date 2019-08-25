from django.db import transaction
from django.db.models import Case
from django.db.models import F
from django.db.models import Sum
from django.db.models import When
from iamporter import Iamporter
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

from config.settings import imp_key
from config.settings import imp_secret
from .models import Cart
from .models import Order
from .serializer import CartSerializer
from .serializer import OrderSerializer
from .serializer import CartExistSerializer
from .serializer import PaymentCompleteSerializer


class OrderListAPI(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.auth
        customer = jwt_decode_handler(customer)
        customer = customer.get('email')

        queryset = Order.objects.filter(customer__email=customer)
        return queryset


class CartListAPI(ListCreateAPIView, mixins.UpdateModelMixin):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.pk
        queryset = Cart.objects.filter(customer=customer)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data['customer_id'] = request.user.pk
        return self.create(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def update(self, request, *args, **kwargs):
    #     instance = Cart.objects.filter(customer=request.user.pk)
    #     serializer = CartSerializer(instance=instance, data=request.data,
    #                                 many=True)
    #     serializer.customer_id = request.user.pk
    #     print(serializer)
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.is_valid())
    #     serializer.save()
    #     return Response(serializer.data)

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
        return Response(serializer.data)


class PaymentComplete(GenericAPIView):
    serializer_class = PaymentCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client = Iamporter(imp_key=imp_key,
                           imp_secret=imp_secret)
        imp_uid = request.data['imp_uid']
        customer_id = request.user.pk
        payment_info = client.find_payment(imp_uid=imp_uid)
        queryset = Cart.objects.filter(customer=customer_id).aggregate(
            total_amount=Sum(
                Case(
                    When(
                        product__is_discount=True,
                        then=F('product__discount_price')
                    ),
                    default=F('product__price')
                )
            )
        )
        if payment_info['amount'] == queryset['total_amount']:
            with transaction.atomic():
                Order.objects.bulk_create(
                    Cart.objects.filter(customer=customer_id))
                Cart.objects.filter(customer=customer_id).delete()
            instance = {'status': 'success'}
        else:

            instance = {'status': 'failed'}
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
