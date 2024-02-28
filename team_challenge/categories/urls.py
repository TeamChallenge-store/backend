from django.urls import path
from .views import CategoryList, CategoryDetail, SubcategoryDetail

urlpatterns = [
    path('product-categories/', CategoryList.as_view(), name='category-list'),
    path('product-categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('product-categories/<int:pk>/<int:subcategory_pk>/', SubcategoryDetail.as_view(), name='subcategory-detail'),


    # Sorting for category views
    path('product-categories/<int:pk>/price_up/', 
         CategoryDetail.as_view(), {'sort': 'price_up'}, name='category-price-up'),

    path('product-categories/<int:pk>/price_down/',
          CategoryDetail.as_view(), {'sort': 'price_down'}, name='category-price-down'),

    path('product-categories/<int:pk>/rate/', 
         CategoryDetail.as_view(), {'sort': 'rate'}, name='category-rate'),


    # Sorting for subcategory views
    path('product-categories/<int:pk>/<int:subcategory_pk>/price_up/', 
         SubcategoryDetail.as_view(), {'sort': 'price_up'}, name='subcategory-price-up'),

    path('product-categories/<int:pk>/<int:subcategory_pk>/price_down/',
          SubcategoryDetail.as_view(), {'sort': 'price_down'}, name='subcategory-price-down'),

    path('product-categories/<int:pk>/<int:subcategory_pk>/rate/',
          SubcategoryDetail.as_view(), {'sort': 'rate'}, name='subcategory-rate'),
]