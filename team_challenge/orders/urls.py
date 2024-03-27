from django.urls import path
from .views import OrderView  # , CartItemDelete, CartItemAdded

urlpatterns = [
    path("orders/", OrderView.as_view(), name="orders"),
    
]
