from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductDetailSerializer
from .services import *

class ProductListView(APIView):
    """"Вивід списку продуктів"""
    def get(self, request):
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)

        filtered_products = filter_price_products(min_price, max_price)

        return paginate_product_list(filtered_products, request)

class ProductDetailView(APIView):
    """"Вивід детального списку продуктів"""
    def get(self, request, id):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

class ProductListViewPriceUp(APIView):
    """Вивід списку продуктів за зростанням ціни"""
    def get(self, request):
        category = request.query_params.get("category", None)

        sorted_products = sort_price_up(category)

        return paginate_product_list(sorted_products, request)


class ProductListViewPriceDown(APIView):
    """Вивід списку продуктів за спаданням ціни"""

    def get(self, request):
        category = request.query_params.get("category", None)

        sorted_products = sort_price_down(category)

        return paginate_product_list(sorted_products, request)


class ProductListViewRate(APIView):
    """Вивід списку продуктів за рейтингом"""

    def get(self, request):
        category = request.query_params.get("category", None)
        make_rate()
        sorted_products = sort_rate(category)

        return paginate_product_list(sorted_products, request)
