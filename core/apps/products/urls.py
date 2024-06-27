from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from .views import (
    BrandListView,
    ProductDetailView,
    ProductListView,
)


router = DefaultRouter()
router.register(r'brands', BrandListView, basename='brands')
                    

urlpatterns = [
    path("products", ProductListView.as_view(), name = "product-list"),
    path("products/<int:product_id>", ProductDetailView.as_view(), name = "product-detail"),
    path('', include(router.urls)),
]
