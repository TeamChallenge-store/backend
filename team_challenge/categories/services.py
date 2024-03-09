from collections import OrderedDict
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

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

def filter_products(products, search_query=None, min_price=None, max_price=None):
    """Фільтрація за ціною та пошук продуктів"""

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(brand__name__icontains=search_query))

    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    return products

def sort_products(products, sort_option):
    """Сортування продуктів"""

    if sort_option == 'price_up':
        return products.order_by('price')
    elif sort_option == 'price_down':
        return products.order_by('-price')
    elif sort_option == 'rate':
        return products.order_by('-rate')
    else:
        return products 
