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

    # def update(self, instance, validated_data):
    #     customer_id = validated_data.pop('customer_id')
    #     instance.customer_id = customer_id
    #     return instance

    # def create(self, validated_data):
    #     quantity = validated_data.pop('quantity')
    #     customer = Customer.objects.get(pk=validated_data.pop('customer_id'))
    #     product = Product.objects.get(pk=validated_data.pop('product_id'))
    #     cart = Cart.objects.create(customer=customer, product=product,
    #                                quantity=quantity)
    #     return cart


class CartExistSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    result = serializers.BooleanField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    customer_id = serializers.IntegerField(write_only=True)
