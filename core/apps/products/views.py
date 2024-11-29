from django.db.models import Q
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.generics import ListAPIView
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
from .filters import ProductFilter


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['price', 'rate']

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.query_params.get('sort', None)

        if sort == 'price_up':
            return queryset.order_by('price')
        elif sort == 'price_down':
            return queryset.order_by('-price')
        elif sort == 'rate':
            return queryset.order_by('-rate')

        return queryset


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
