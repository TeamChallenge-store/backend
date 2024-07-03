from rest_framework import serializers

from .models import (
    Brand,
    Color,
    Comment,
    Product,
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'rating', 'product', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at', 'updated_at']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['name', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'subcategory', 'name', 'price', 'old_price', 'image', 'quantity_in_stock', 'brand',
            'color', 'rate', 'subtitle', 'subscription', 'features', 'created_at', 'updated_at', 'comments', 'links',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'comments', 'links']

    def get_links(self, obj):
        request = self.context.get('request')
        if request is not None:
            product_id = obj.id
            href = request.build_absolute_uri(f"/api/v1/products/{product_id}/")
            return href
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
