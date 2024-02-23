from rest_framework import serializers
from .models import Category, Subcategory

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'parent_category_id', 'name', 'image')

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(source='subcategory_set', many=True)  

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'subcategories')
