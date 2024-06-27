from django.urls import path

from .views import (
    CategoryDetail,
    CategoryList,
    SubcategoryDetail,
)


urlpatterns = [
    path('product-categories', CategoryList.as_view(), name='category-list'),
    path('product-categories/<slug:category_slug>', CategoryDetail.as_view(), name='category-detail'),
    path(
        'product-categories/<slug:category_slug>/<slug:subcategory_slug>',
         SubcategoryDetail.as_view(),
         name='subcategory-detail',
    ),
]
