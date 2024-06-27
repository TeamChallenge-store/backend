from django.urls import path

from .views import CartView  # , CartItemDelete, CartItemAdded


urlpatterns = [
    path("cart", CartView.as_view(), name="cart"),
]
