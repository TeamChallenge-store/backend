from django.urls import path
from .views import CartView, CartItemDelete, CartItemAdded

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:pk>", CartItemDelete.as_view(), name="cart-item-deleted"),
    path(
        "cart/<int:pk>/<int:quantity>/", CartItemAdded.as_view(), name="cart-item-added"
    ),
]
