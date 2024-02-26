from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination  
from .models import Category, Subcategory
from .serializers import CategorySerializer
from products.serializers import ProductListSerializer  
from products.models import Product

class CustomPageNumberPagination(PageNumberPagination):
    """Пагінація"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryList(APIView):
    """Список категорій"""
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class CategoryDetail(APIView):
    """Перехід на певну категорію"""

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        products = Product.objects.filter(category=category)

        # Пагінація продуктів
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        product_serializer = ProductListSerializer(paginated_products, many=True)

        # Додаємо дані про категорію та підкатегорії до відповіді
        response_data = serializer.data
        response_data['products'] = product_serializer.data  # Передаємо дані про продукти
        return paginator.get_paginated_response(response_data)

class SubcategoryDetail(APIView):
    """Перехід на підкатегорію"""

    def get_object(self, category_pk, subcategory_pk):
        try:
            # Отримати об'єкт підкатегорії за ідентифікатором
            subcategory = Subcategory.objects.get(pk=subcategory_pk, parent_category_id=category_pk)
            return subcategory
        except Subcategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, subcategory_pk, format=None):
        # Отримати об'єкт підкатегорії
        subcategory = self.get_object(pk, subcategory_pk)  # Оновлено, передаємо pk

        # Отримати товари, які належать до цієї підкатегорії
        products = Product.objects.filter(subcategory=subcategory)

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        # Серіалізація товарів
        serializer = ProductListSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
