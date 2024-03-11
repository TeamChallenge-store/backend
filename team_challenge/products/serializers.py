from rest_framework import serializers
from .models import Product, Brand

class ProductListSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'subcategory', 'name', 'price', 'image', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        if request is not None:
            product_id = obj.id
            href = request.build_absolute_uri(f"/api/v1/products/{product_id}/")
            return {
                "self": {
                    "href": href,
                    "title": f"Get product item page for product {product_id}"
                }
            }
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"