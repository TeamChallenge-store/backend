from django.urls import path
from .views import CartView #, CartItemDelete, CartItemAdded

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    # path(
    #     "cart/?pk=pk&quantity=quantity/", CartItemAdded.as_view(), name="cart-item-added"
    # ),
    # path("cart/?pk=pk/", CartItemDelete.as_view(), name="cart-item-deleted"),
    
    # path(
    #     "cart/<int:pk>/<int:quantity>/", CartItemAdded.as_view(), name="cart-item-added"
    # ),
]
