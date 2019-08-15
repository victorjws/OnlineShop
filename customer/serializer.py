from rest_framework import serializers

from customer.models import Customer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'nickname', 'shipping_address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            shipping_address=validated_data['shipping_address'],
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer


class TokenSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    token = serializers.CharField(max_length=255)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'nickname', 'shipping_address']
