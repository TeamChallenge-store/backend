import random
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductListSerializer
from .models import Product

def paginate_product_list(products, request):
    """Пагінація"""
    paginator = PageNumberPagination()
    paginator.page_size = 12 

    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

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
