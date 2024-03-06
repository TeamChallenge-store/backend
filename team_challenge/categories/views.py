from collections import OrderedDict
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination  
from .models import Category, Subcategory
from .serializers import CategorySerializer
from products.serializers import ProductListSerializer  
from products.models import Product
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CategorySerializer, SubcategorySerializer
from rest_framework import filters
from django.db.models import Q
class CustomPageNumberPagination(PageNumberPagination):
    """Пагінація"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['page_size'] = self.page_size

        total_pages = self.page.paginator.num_pages
        response.data['total_pages'] = total_pages

        response.data = OrderedDict([
            ('count', response.data['count']),
            ('page_size', response.data['page_size']),
            ('total_pages', response.data['total_pages']),
            ('next', response.data['next']),
            ('previous', response.data['previous']),
            ('results', response.data['results']),
        ])
        return response

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

    def get(self, request, category_slug=None, format=None):
        sort = request.GET.get('sort')
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)

        search_query = request.query_params.get('search', None)
        products = Product.objects.filter(category=category)

        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(brand__name__icontains=search_query))

        # Фільтрація за ціною
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        # Сортування
        if sort == 'price_up':
            products = products.order_by('price')  
        elif sort == 'price_down':
            products = products.order_by('-price') 
        elif sort == 'rate':
            products = products.order_by('-rate')  
            
        # Пагінація
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        product_serializer = ProductListSerializer(paginated_products, many=True)

        response_data = serializer.data
        response_data['products'] = product_serializer.data
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
    
    def get(self, request, category_slug, subcategory_slug, format=None):
        sort = request.GET.get('sort')
        subcategory = self.get_object(category_slug, subcategory_slug)  
        products = Product.objects.filter(subcategory=subcategory)

        search_query = request.query_params.get('search', None)


        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(brand__name__icontains=search_query))

        # Фільтрація за ціною
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        if sort == 'price_up':
            products = products.order_by('price')
        elif sort == 'price_down':
            products = products.order_by('-price')
        elif sort == 'rate':
            products = products.order_by('-rate')

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
