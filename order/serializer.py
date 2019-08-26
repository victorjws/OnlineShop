from rest_framework import serializers

from customer.models import Customer
from customer.serializer import CustomerSerializer
from product.models import Product
from product.serializer import ProductSerializer
from .models import Cart
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CartListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass


class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Customer.objects.all(),
        source='customer'
    )
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = Cart
        fields = '__all__'
        list_serializer_class = CartListSerializer


class CartExistSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    result = serializers.BooleanField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    customer_id = serializers.IntegerField(write_only=True)


class PaymentCompleteSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    imp_uid = serializers.CharField(write_only=True, max_length=255)
    status = serializers.CharField(read_only=True, max_length=255)
