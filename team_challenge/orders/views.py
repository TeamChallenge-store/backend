# Create your views here.
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response as rest_response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order, OrderItem, User
from .serializers import OrderItemSerializer
from basket.models import CartAnonymous, CartAnonymousItem
from basket.serializers import CartItemSerializer, CartAnonymousItemSerializer


class OrderView(APIView):
    """Операції з замовленням"""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Success", schema=OrderItemSerializer()),
            404: openapi.Response(description="Not Found"),
        }
    )
    def get(self, request, order_id):
        """Отримання інформації про замовлення"""

        try:
            order = Order.objects.get(pk=order_id)

        except Order.DoesNotExist:
            return rest_response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = User.objects.get(pk=order.user_id)
        session = request.session
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_200_OK)


    def post(self, request):  # , pk, quantity):
        """Створення замовлення"""

        # Отримання інформації про кошик
        session = request.session
        cart = CartAnonymous.objects.get(session_id=session.session_key)
        cart_items = CartAnonymousItem.objects.filter(cart=cart)

        serializer = CartAnonymousItemSerializer(cart_items, many=True)
        response_data = {
            "session_key": session.session_key,
            "cart_items": serializer.data,
            "total_items": sum(item.quantity for item in cart_items),
            "total_price": sum(
                item.quantity * item.product.price for item in cart_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_201_CREATED)
