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

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'subcategories', 'products')

    def get_products(self, instance):
        products = Product.objects.filter(category=instance)
        serializer = ProductListSerializer(products, many=True)
        return serializer.data

    products = serializers.SerializerMethodField(method_name='get_products')
