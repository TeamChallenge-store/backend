from rest_framework import serializers
from .models import CartItem, CartAnonymousItem
from products.serializers import ProductDetailSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source="product.id")
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = serializers.ImageField(source="product.image")

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "quantity",
            "product_price",
            "product_image",
        ]


class CartAnonymousItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()
    # product_id = serializers.ReadOnlyField(source="product.id")
    # product_name = serializers.ReadOnlyField(source="product.name")
    # product_price = serializers.ReadOnlyField(source="product.price")
    # product_image = serializers.ImageField(source="product.image")

    class Meta:
        model = CartAnonymousItem
        fields = [
            "id",
            "product",
            # "product_id",
            # "product_name",
            "quantity",
            # "product_price",
            # "product_image",
        ]
