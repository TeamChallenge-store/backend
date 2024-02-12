from django.urls import path
from .views import (ProductListView, 
                    ProductDetailView,
                    CartView,)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/', CartView.as_view(), name='cart-delete'),
]