from rest_framework import serializers

from core.apps.products.serializers import ProductDetailSerializer

from .models import (
    CartAnonymousItem,
    CartItem,
)


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
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartAnonymousItem
        fields = [
            "id",
            "product",
            "quantity",
            "total_price"
        ]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
