from rest_framework import serializers
from .models import OrderItem, User, Order

class OrderUserSerializer(serializers.ModelSerializer):

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name =serializers.ReadOnlyField(source="user.last_name")
    phone = serializers.ReadOnlyField(source="user.phone")
    email = serializers.ReadOnlyField(source="user.email")
    address = serializers.ReadOnlyField(source="user.address")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "address",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
   
    product_id = serializers.ReadOnlyField(source="product.id")
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = serializers.ImageField(source="product.image")

    class Meta:
        model = OrderItem
        fields = [
            "id",            
            "product_id",
            "product_name",
            "quantity",
            "product_price",
            "product_image",
        ]

class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerializer()
    item = OrderItemSerializer()

    class Meta:
        model = Order
        fields = [
            "user",
            "item",
        ]
