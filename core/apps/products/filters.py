import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    subcategory = django_filters.CharFilter(field_name='subcategory__slug', lookup_expr='iexact')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    color = django_filters.CharFilter(field_name='color__name', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'brand', 'color', 'min_price', 'max_price']
