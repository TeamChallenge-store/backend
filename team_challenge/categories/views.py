from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination  # Імпорт пагінації
from .models import Category
from .serializers import CategorySerializer
from products.serializers import ProductListSerializer  # Виправлення імпорту
from products.models import Product

class CustomPageNumberPagination(PageNumberPagination):
    """Власний клас пагінації"""
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
    """Список підкатегорій та продуктів певної категорії"""

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
