from rest_framework import serializers

from .models import (
    Brand,
    Color,
    Product,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at', 'updated_at']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['name', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(source='brand.name')
    color = serializers.StringRelatedField(source='color.name')
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'subcategory', 'name', 'price', 'old_price', 'image', 'quantity_in_stock', 'brand',
            'color', 'rate', 'subtitle', 'subscription', 'features', 'created_at', 'updated_at', '_links',
        ]

    def get__links(self, obj):
        request = self.context.get('request')
        if request is not None:
            product_id = obj.id
            href = request.build_absolute_uri(f"/api/v1/products/{product_id}/")
            return {
                "self": {
                    "href": href,
                    "title": f"Get product item page for product {product_id}",
                },
            }
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
