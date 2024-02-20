from django.urls import path
from .views import (ProductListView, 
                    ProductDetailView,
                    ProductListViewRate,
                    ProductListViewPriceDown,
                    ProductListViewPriceUp,)

urlpatterns = [
    path("products/", ProductListView.as_view(), name = "product-list"),
    path("products/price_up/", ProductListViewPriceUp.as_view(), name = "product-list-price-up"),
    path("products/price_down/", ProductListViewPriceDown.as_view(), name = "product-list-price-down"),
    path("products/rate/", ProductListViewRate.as_view(), name = "product-list-rate"),
    path("products/<int:id>/", ProductDetailView.as_view(), name = "product-detail"),
]