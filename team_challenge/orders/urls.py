from django.urls import path
from .views import OrderView  # , CartItemDelete, CartItemAdded

urlpatterns = [
    path("orders/<int:order_id>/", OrderView.as_view(), name="orders"),
]
