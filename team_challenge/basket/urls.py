from django.urls import path
from .views import CartItemListView

urlpatterns = [
    path('cart/', CartItemListView.as_view(), name='cart-item-list'),
    # Додайте інші URL, якщо потрібно
]
