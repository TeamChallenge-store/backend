from collections import OrderedDict
import random
from requests import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductListSerializer
from .models import Product


def paginate_product_list(products, request):

    class CustomPageNumberPagination(PageNumberPagination):
        """Custom pagination class for product list."""
        page_size = 12
        page_size_query_param = 'page_size'
        max_page_size = 100

        def get_paginated_response(self, data):
            response = super().get_paginated_response(data)
            response.data['page_size'] = self.page_size

            # Отримання загальної кількості сторінок
            total_pages = self.page.paginator.num_pages
            response.data['total_pages'] = total_pages

            # Переупорядкування полів у відповіді
            response.data = OrderedDict([
                ('count', response.data['count']),
                ('page_size', response.data['page_size']),
                ('total_pages', response.data['total_pages']),
                ('next', response.data['next']),
                ('previous', response.data['previous']),
                ('results', response.data['results']),
            ])
            return response

    paginator = CustomPageNumberPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductListSerializer(paginated_products, many=True, context={'request': request})

    # Захоплення пагінованої відповіді
    paginated_data = paginator.get_paginated_response(serializer.data)

    return paginated_data

def filter_price_products(min_price, max_price):
    """Фільтрація за ціною"""
    products = Product.objects.all()

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    return products

def sort_price_up(category):
    """Сортування за зростанням ціни"""
    products = Product.objects.all()

    if category is not None:
        products = products.filter(category=category)

    return products.order_by('price')


def sort_price_down(category):
    """Сортування за спаданням ціни"""
    products = Product.objects.all()

    if category is not None:
        products = products.filter(category=category)
    return products.order_by("-price")


def sort_rate(category):
    """Сортування за рейтингом"""
    products = Product.objects.all()

    if category is not None:
        products = products.filter(category=category)

    return products.order_by("-rate")


def make_rate():
    """Випдковий(рандомний) рейтинг для товарів иід 1 до 99"""
    products = Product.objects.all().filter(rate=0)
    if products:
        for product in products:
            product.rate = random.randint(1, 99)
            product.save()
