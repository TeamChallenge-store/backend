from rest_framework import serializers

from core.apps.products.models import Product
from core.apps.products.serializers import ProductListSerializer

from .models import (
    Category,
    Subcategory,
)


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'slug', 'parent_category_id', 'name', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(source='subcategory_set', many=True)
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = Category
        fields = ('id', 'slug', 'name', 'image', 'subcategories', 'products')

    def get_products(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, 'resolver_match') and 'category_slug' in request.resolver_match.kwargs:
            category_slug = request.resolver_match.kwargs['category_slug']
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                products = Product.objects.filter(category=category)
                serializer = ProductListSerializer(products, many=True)
                return serializer.data
        return []
