from rest_framework import serializers

from .models import (
    Address,
    Order,
    OrderItem,
    User,
)


class OrderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
        ]


class OrderAddressSerializer(serializers.ModelSerializer):
    # city = serializers.ReadOnlyField(source="address.city")

    class Meta:
        model = Address
        fields = [
            "id",
            "city",
            "address",
            "np_department",
            "up_department",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source="product.id")
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = serializers.ImageField(source="product.image")

    class Meta:
        model = OrderItem
        # fields = "__all__"
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
    address = OrderAddressSerializer()
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "time_create",
            "delivery_method",
            "payment_method",
            "user",
            "address",
            "products",
        ]
