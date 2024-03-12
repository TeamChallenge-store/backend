import django_filters
from products.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='iexact')
    color = django_filters.CharFilter(field_name='color', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'brand', 'color']
