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

    pk = openapi.Parameter("pk", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="specify the order number as 'pk' to be showed",
        manual_parameters=[pk],
        responses={
            200: openapi.Response(description="Success", schema=OrderItemSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def get(self, request):
        """Отримання інформації про замовлення"""

        pk = request.query_params.get("pk")
        if  not pk:
            return rest_response(
                {"error": "missing parameter 'pk'"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(pk=pk)
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
            "first_name": user.first_name,
            "phone": user.phone,
            "email": user.email,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="creating an order based on the basket data",
        responses={
            201: openapi.Response(description="Create", schema=OrderItemSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )

    def post(self, request):
        """Створення замовлення"""

        # Отримання інформації про кошик
        cart = CartAnonymous.objects.get(session_id=session.session_key)
        cart_items = CartAnonymousItem.objects.filter(cart=cart)

        # Отримання інформації з запиту
        session = request.session
        data = request.data
        if not (data and data["First Name"] and data["Last Name"]
                and data["Phone number"] and data["Email"] and data["Address"]):
            return rest_response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
        # if not data:
        #     first_name = "First Name"
        #     last_name = "Last Name"
        #     phone = "Phone number"
        #     email = "Email"
        #     address = "Address"
        else:
            first_name = data["First Name"]
            last_name = data["Last Name"]
            phone = data["Phone number"]
            email = data["Email"]
            address = data["Address"]
        # user = request.user
        user = User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address)
        # user.save()

        order = Order.objects.create(user=user)
        # order.save()

        for item in cart_items:
            order_item, created = OrderItem.objects.update_or_create(order=order,product=item.product)
        # order_item.save()

        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "first_name": user.first_name,
            "phone": user.phone,
            "email": user.email,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_201_CREATED)
