from rest_framework import serializers
from .models import Category, Subcategory
from products.models import Product
from products.serializers import ProductListSerializer

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'parent_category_id', 'name', 'image')

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(source='subcategory_set', many=True)
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'subcategories', 'products')

    def get_products(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, 'resolver_match') and 'pk' in request.resolver_match.kwargs:
            pk = request.resolver_match.kwargs['pk']
            category = Category.objects.filter(pk=pk).first()
            if category:
                products = Product.objects.filter(category=category)
                serializer = ProductListSerializer(products, many=True)
                return serializer.data
        return []