from django.db import transaction
from django.db.models import Case
from django.db.models import F
from django.db.models import Sum
from django.db.models import When
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler
from iamporter import Iamporter

from config.settings import imp_key
from config.settings import imp_secret
from product.models import Product
from .models import Cart
from .models import Order
from .serializer import CartSerializer
from .serializer import OrderSerializer
from .serializer import CartExistSerializer
from .serializer import PaymentCompleteSerializer


class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.auth
        customer = jwt_decode_handler(customer)
        customer = customer.get('email')
        queryset = Order.objects.filter(customer__email=customer).order_by(
            '-pk')
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

    def patch(self, request, *args, **kwargs):
        result = "update failed"
        data = {
            i['product_id']: {k: v for k, v in i.items() if k != 'product_id'}
            for i in request.data
        }
        with transaction.atomic():
            for inst in self.get_queryset().filter(product_id__in=data.keys()):
                serializer = self.get_serializer(inst,
                                                 data=data[inst.product_id],
                                                 partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            result = "update complete"
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        result = "delete failed"
        deleted, _ = self.get_queryset().filter(
            product_id=request.data['product_id']).delete()
        if deleted > 0:
            result = "delete complete"
        return Response(result, status=status.HTTP_200_OK)


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
                        then=F('product__discount_price') * F('quantity')
                    ),
                    default=F('product__price') * F('quantity')
                )
            )
        )
        instance = {'status': 'failed'}
        if payment_info['amount'] == queryset['total_amount']:
            with transaction.atomic():
                ordered = Order.objects.bulk_create(
                    Cart.objects.filter(customer=customer_id))
                Cart.objects.filter(customer=customer_id).delete()
                for i in ordered:
                    product = Product.objects.get(name=i.product)
                    product.stock -= i.quantity
                    product.save()
                instance = {'status': 'success'}
        else:
            client.cancel_payment(imp_uid=imp_uid, reason="amount mismatch")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
