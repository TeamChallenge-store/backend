from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response as rest_response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order, OrderItem, User, Address, UserAddress
from .serializers import OrderItemSerializer, OrderUserSerializer, OrderSerializer
from basket.models import CartAnonymous, CartAnonymousItem

NOVA_POSHTA_DELIVERY = 70
UKR_POSHTA_DELIVERY = 70
COURIER = 150

class OrderView(APIView):
    """Операції з замовленням"""

    order_id = openapi.Parameter(
        "order_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(
        operation_description="specify the order number as 'order_id' to be showed",
            # '\n'\
            # SHIP_METHODS = [('NP', 'Nova Poshta'), ('UP', 'Ukr Poshta'), ('CR', 'Courier')]",
        manual_parameters=[order_id],
        responses={
            200: openapi.Response(description="Success", schema=OrderSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def get(self, request):
        """Отримання інформації про замовлення"""
        
        order_id = request.query_params.get("order_id")
        if not order_id:

            return rest_response(
                {"error": "missing parameter 'order_id'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return rest_response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # print(type(order.products))

        # user = request.user
        # Якщо незареєстрований користувач

        user = User.objects.get(id=order.user_id)

        session = request.session
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)
        delivery_price = UKR_POSHTA_DELIVERY
        if order.delivery_method == "Nova Poshta":
            delivery_price = NOVA_POSHTA_DELIVERY
        elif order.delivery_method == "Courier":
            delivery_price = COURIER

        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "order_id": order.id,
            "time_create": order.time_create,
            "delivery_method": order.delivery_method,
            "delivery_price": delivery_price,
            "user": serializer_user.data,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            )
            + delivery_price,
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
                "City": openapi.Schema(type=openapi.TYPE_STRING),
                "Address": openapi.Schema(type=openapi.TYPE_STRING),
                "NP_department": openapi.Schema(type=openapi.TYPE_STRING),
                "UP_department": openapi.Schema(type=openapi.TYPE_STRING),
                "Delivery_method": openapi.Schema(type=openapi.TYPE_STRING),
                "Payment_method": openapi.Schema(type=openapi.TYPE_STRING),
            },
            # enum=['1','2','3','4']
            example={
                "First Name": "Olexa",
                "Last Name": "Dovbush",
                "Phone number": "098765432",
                "Email": "example@test.ua",
                "City": "Ternopil",
                "Address": "Test_example",
                "NP_department": "3",
                "UP_department": "22222",
                "Delivery_method": "Ukr Poshta",
                "Payment_method": "card online",
            },
        ),
        responses={
            201: openapi.Response(description="Create", schema=OrderSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def post(self, request):
        """Створення замовлення"""

        # Отримання інформації з запиту
        session = request.session
        data = request.data

        # Створення нового користувача
        if not data:
            first_name = "Test"
            last_name = "TestTest"
            phone = "111111111"
            email = "test@test.test"
            city = "Kyiv"
        else:
            first_name = data["First Name"]
            last_name = data["Last Name"]
            phone = data["Phone number"]
            email = data["Email"]
            city = data["City"]

        user = User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email) 
        # user.save()
        address = Address.objects.create(city=city)
        if data["Address"]:
            address.address = data["Address"]
        if data["NP_department"]:
            address.np_department = data["NP_department"]
        if data["UP_department"]:
            address.up_department = data["UP_department"]

        user_address = UserAddress.objects.create(user=user, address=address)


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
            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        # order_item.save()
        # Видалення кошика
        cart.delete()

        session = request.session
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)
        delivery_price = UKR_POSHTA_DELIVERY
        if order.delivery_method == "Nova Poshta":
            delivery_price = NOVA_POSHTA_DELIVERY
        elif order.delivery_method == "Courier":
            delivery_price = COURIER


        # Створення відповіді
        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "order_id": order.id,
            "time_create": order.time_create,
            "delivery_method": order.delivery_method,
            "delivery_price": delivery_price,
            "user": serializer_user.data,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            )
            + delivery_price,
        }

        return rest_response(response_data, status=status.HTTP_201_CREATED)
