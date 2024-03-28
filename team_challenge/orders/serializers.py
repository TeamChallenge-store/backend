from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    # user_name =  serializers.ReadOnlyField(source="user.name"),
    # user_phone = serializers.ReadOnlyField(source="user.phone"),
    # user_email = serializers.ReadOnlyField(source="user.email"),
    product_id = serializers.ReadOnlyField(source="product.id")
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = serializers.ImageField(source="product.image")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            # "user_name",
            # "user_phone",
            # "user_email",
            "product_id",
            "product_name",
            "quantity",
            "product_price",
            "product_image",
        ]
