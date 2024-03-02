from rest_framework.views import APIView
from rest_framework.response import Response as responce
from rest_framework import status
from .models import Product
from .serializers import ProductDetailSerializer
from .services import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ProductListView(APIView):
    """"Вивід списку продуктів"""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=ProductListSerializer(many=True)),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found')
        }
    )

    def get(self, request):
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        sort = request.query_params.get('sort')

        filtered_products = filter_price_products(min_price, max_price)

        if sort == 'price_up':
            filtered_products = filtered_products.order_by('price')
        elif sort == 'price_down':
            filtered_products = filtered_products.order_by('-price')
        elif sort == 'rate':
            filtered_products = filtered_products.order_by('-rate')

        return paginate_product_list(filtered_products, request)

class ProductDetailView(APIView):
    """Деталі продукту"""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=ProductDetailSerializer()),
            404: openapi.Response(description='Not Found')
        }
    )
    def get(self, request, product_id, format=None):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductDetailSerializer(product)
            return responce(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return responce({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

