from collections import OrderedDict
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

    def get(self, request, pk=None, format=None, sort=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)

        if sort == 'price_up':
            products = Product.objects.filter(category=category).order_by('price')  # Sort by price ascending
        elif sort == 'price_down':
            products = Product.objects.filter(category=category).order_by('-price')  # Sort by price descending
        elif sort == 'rate':
            products = Product.objects.filter(category=category).order_by('-rate')  # Sort by rating descending
        else:
            products = Product.objects.filter(category=category)  # Default sorting

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        product_serializer = ProductListSerializer(paginated_products, many=True)

        response_data = serializer.data
        response_data['products'] = product_serializer.data
        return paginator.get_paginated_response(response_data)

class SubcategoryDetail(APIView):
    """Перехід на підкатегорію"""

    def get_object(self, category_pk, subcategory_pk):
        try:
            subcategory = Subcategory.objects.get(pk=subcategory_pk, parent_category_id=category_pk)
            return subcategory
        except Subcategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, subcategory_pk, sort=None):
        subcategory = self.get_object(pk, subcategory_pk)  
        products = Product.objects.filter(subcategory=subcategory)

        if sort == 'price_up':
            products = Product.objects.filter(subcategory=subcategory).order_by('price')
        elif sort == 'price_down':
            products = Product.objects.filter(subcategory=subcategory).order_by('-price')
        elif sort == 'rate':
            products = Product.objects.filter(subcategory=subcategory).order_by('-rate')


        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
