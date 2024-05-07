from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response as rest_response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order, OrderItem, User
from .serializers import OrderItemSerializer, OrderUserSerializer, OrderSerializer
from basket.models import CartAnonymous, CartAnonymousItem


class OrderView(APIView):
    """Операції з замовленням"""

    pk = openapi.Parameter("pk", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="specify the order number as 'pk' to be showed",
        manual_parameters=[pk],
        responses={
            200: openapi.Response(description="Success", schema=OrderSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def get(self, request):
        """Отримання інформації про замовлення"""

        pk = request.query_params.get("pk")
        if not pk:
            return rest_response(
                {"error": "missing parameter 'pk'"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return rest_response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        # Якщо незареєстрований користувач
        # print(type(user))

        user = User.objects.get(pk=order.user_id)
        # print(type(user))
        session = request.session
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)

        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "order_id": order.id,
            "user": serializer_user.data,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="creating an order based on the basket data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "First Name": openapi.Schema(type=openapi.TYPE_STRING),
                "Last Name": openapi.Schema(type=openapi.TYPE_STRING),
                "Phone number": openapi.Schema(type=openapi.TYPE_STRING),
                "Email": openapi.Schema(type=openapi.TYPE_STRING),
                "Address": openapi.Schema(type=openapi.TYPE_STRING),
            },
            # enum=['1','2','3','4']
            example={
                "First Name": "Olexa",
                "Last Name": "Dovbush",
                "Phone number": "098765432",
                "Email": "example@test.ua",
                "Address": "Ternopil",
            },
        ),
        responses={
            201: openapi.Response(
                description="Create", schema=OrderSerializer()
            ),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def post(self, request):
        # Отримання інформації з запиту
        session = request.session
        data = request.data

        # Створення нового користувача
        if not data:
            first_name = "Test"
            last_name = "TestTest"
            phone = "111111111"
            email = "test@test.test"
            address = "Test___Test"
        else:
            first_name = data.get("First Name", "")
            last_name = data.get("Last Name", "")
            phone = data.get("Phone number", "")
            email = data.get("Email", "")
            address = data.get("Address", "")

        user = User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                   address=address)

        # Отримання інформації про кошик
        try:
            cart = CartAnonymous.objects.get(session=session.session_key)
        except CartAnonymous.DoesNotExist:
            return rest_response(
                {"error": "Basket does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartAnonymousItem.objects.filter(cart=cart)
        if not cart_items:
            return rest_response(
                {"error": "Basket is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Створення замовлення
        order = Order.objects.create(user=user)

        # Копіювання товарів з кошика до замовлення
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Видалення кошика
        cart.delete()

        # Отримання інформації про товари у замовленні
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)

        # Створення відповіді
        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "order_id": order.id,
            "user": serializer_user.data,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            ),
        }

        return rest_response(response_data, status=status.HTTP_201_CREATED)
