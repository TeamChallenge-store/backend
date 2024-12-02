import django_filters
from django.db.models import Q
from django.db.models.functions import Upper
from django_filters import filters, CharFilter, BaseInFilter
from .models import Product


class CharInFilter(BaseInFilter, CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        # Prepare the values by converting them to uppercase
        values = [v.upper() for v in value]
        # Create a Q object for case-insensitive filtering with OR logic
        query = Q()
        for v in values:
            query |= Q(**{f"{self.field_name}__iexact": v})
        return qs.filter(query)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    subcategory = django_filters.CharFilter(field_name='subcategory__slug', lookup_expr='iexact')
    brand = CharInFilter(field_name='brand__name')
    color = CharInFilter(field_name='color__name')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'brand', 'color', 'min_price', 'max_price']
