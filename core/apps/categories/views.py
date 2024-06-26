from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.apps.products.serializers import ProductListSerializer
from core.apps.products.models import Product
from .models import Category, Subcategory
from .services import CustomPageNumberPagination, filter_products, sort_products
from .serializers import CategorySerializer, SubcategorySerializer
from .filters import ProductFilter


class CategoryList(APIView):
    """Список категорій"""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success'),
        }
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """Перехід на певну категорію"""

    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=CategorySerializer),
        }
    )
    def get(self, request, category_slug=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        products = Product.objects.filter(category=category).order_by('id')

        # Sorting and search
        search_query = request.query_params.get('search', None)
        sort_option = request.query_params.get('sort')
        products = filter_products(products, search_query=search_query)
        products = sort_products(products, sort_option)

        # Fileter
        product_filter = ProductFilter(request.query_params, queryset=products)
        products = product_filter.qs

        # Pagination
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serialization
        serialized_products = ProductListSerializer(paginated_products, many=True, context={'request': request})

        # Answer to the request
        response_data = serializer.data
        response_data['products'] = serialized_products.data
        return paginator.get_paginated_response(response_data)


class SubcategoryDetail(APIView):
    """Перехід на підкатегорію"""

    def get_object(self, category_slug, subcategory_slug):
        try:
            category = Category.objects.get(slug=category_slug)
            subcategory = Subcategory.objects.get(slug=subcategory_slug, parent_category_id=category)
            return subcategory
        except (Category.DoesNotExist, Subcategory.DoesNotExist):
            raise Http404

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=SubcategorySerializer),
        }
    )
    def get(self, request, category_slug, subcategory_slug):
        subcategory = self.get_object(category_slug, subcategory_slug)
        products = Product.objects.filter(subcategory=subcategory)

        # Sorting and search
        search_query = request.query_params.get('search', None)
        sort_option = request.query_params.get('sort')
        products = filter_products(products, search_query=search_query)
        products = sort_products(products, sort_option)

        # Fileter
        product_filter = ProductFilter(request.query_params, queryset=products)
        products = product_filter.qs

        # Pagination
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serialization
        serialized_products = ProductListSerializer(paginated_products, many=True, context={'request': request})

        # Answer to the request
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        return paginator.get_paginated_response(serialized_products.data)
