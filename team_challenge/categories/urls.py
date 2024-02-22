from django.urls import path
from .views import CategoryList, CategoryDetail

urlpatterns = [
    path('product-categories/', CategoryList.as_view(), name='category-list'),
    path('product-categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]