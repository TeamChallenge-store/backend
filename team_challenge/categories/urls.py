from django.urls import path
from .views import CategoryList, CategoryDetail, SubcategoryDetail

urlpatterns = [
    path('product-categories/', CategoryList.as_view(), name='category-list'),
    path('product-categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('product-categories/<int:pk>/<int:subcategory_pk>/', SubcategoryDetail.as_view(), name = 'subcategory-detail')
]