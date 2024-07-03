from rest_framework import (
    status,
    viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.apps.categories.services import filter_products

from .models import (
    Brand,
    Comment,
    Product,
)
from .serializers import (
    BrandSerializer,
    CommentSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)
from .services import (
    filter_price_products,
    paginate_product_list,
)


class ProductListView(APIView):
    """"Вивід списку продуктів."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=ProductListSerializer(many=True)),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found'),
        },
    )
    def get(self, request):
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        sort = request.query_params.get('sort')
        search_query = request.query_params.get('search', None)

        filtered_products = filter_price_products(min_price, max_price)
        filtered_products = filter_products(filtered_products, search_query=search_query)

        if sort == 'price_up':
            filtered_products = filtered_products.order_by('price')
        elif sort == 'price_down':
            filtered_products = filtered_products.order_by('-price')
        elif sort == 'rate':
            filtered_products = filtered_products.order_by('-rate')
        elif sort == 'date':
            filtered_products = filtered_products.order_by('-date')

        return paginate_product_list(filtered_products, request)


class ProductDetailView(APIView):
    """Деталі продукту."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=ProductDetailSerializer()),
            404: openapi.Response(description='Not Found'),
        },
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class BrandListView(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CommentProductListView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)