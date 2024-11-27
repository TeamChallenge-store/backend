from rest_framework import status
from rest_framework.response import Response as rest_response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.apps.basket.models import (
    CartAnonymous,
    CartAnonymousItem,
)

from .models import (
    Address,
    Order,
    OrderItem,
    User,
    UserAddress,
)
from .serializers import (
    OrderAddressSerializer,
    OrderItemSerializer,
    OrderSerializer,
    OrderUserSerializer,
)

NOVA_POSHTA_DELIVERY = 70
UKR_POSHTA_DELIVERY = 70
COURIER = 150


class OrderView(APIView):
    """Операції з замовленням."""

    order_id = openapi.Parameter(
        "order_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
    )

    email = openapi.Parameter(
        "email", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        operation_description="specify the order number as 'order_id' to be showed",
        # '\n'\
        # SHIP_METHODS = [('NP', 'Nova Poshta'), ('UP', 'Ukr Poshta'), ('CR', 'Courier')]",
        manual_parameters=[order_id, email],
        responses={
            200: openapi.Response(description="Success", schema=OrderSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def get(self, request):
        """Отримання інформації про замовлення."""

        order_id = request.query_params.get("order_id")
        if not order_id:
            return rest_response(
                {"error": "missing parameter 'order_id'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.query_params.get("email")
        if not email:
            return rest_response(
                {"error": "missing parameter 'email'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return rest_response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND,
            )

        # Якщо незареєстрований користувач
        user = User.objects.get(id=order.user_id)

        if not email == user.email:
            return rest_response(
                {"error": f"This {email} have not order number {order_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        address = Address.objects.get(id=order.address_id)

        # session = request.session
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)
        serializer_address = OrderAddressSerializer(address)
        # ціна доставки
        delivery_price = UKR_POSHTA_DELIVERY
        if order.delivery_method == "Nova_Poshta":
            delivery_price = NOVA_POSHTA_DELIVERY
        elif order.delivery_method == "Courier":
            delivery_price = COURIER

        response_data = {
            "message": "Anonymous",
            # "session_key": session.session_key,
            "order_id": order.id,
            "time_create": order.time_create,
            "delivery_method": order.delivery_method,
            "delivery_price": delivery_price,
            "user": serializer_user.data,
            "address": serializer_address.data,
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
                "first_name": "Olexa",
                "last_name": "Dovbush",
                "phone_number": "098765432",
                "email": "example@test.ua",
                "city": "Ternopil",
                "address": {
                    "streetName": "string",
                    "houseNumber": "string",
                    "sectionNumber": "string",
                    "apartmentNumber": "string",
                },
                "department_NP": "3",
                "department_UP": "22222",
                "delivery_method": "Ukr_Poshta",
                "payment_method": "card_online",
            },
        ),
        responses={
            201: openapi.Response(description="Create", schema=OrderSerializer()),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def post(self, request):
        """Створення замовлення."""

        # Отримання інформації з запиту
        session = request.session
        data = request.data

        # Отримання інформації про кошик
        try:
            cart = CartAnonymous.objects.get(session=session.session_key)
        except CartAnonymous.DoesNotExist:
            return rest_response(
                {"error": "Basket does not exist"}, status=status.HTTP_404_NOT_FOUND,
            )

        cart_items = CartAnonymousItem.objects.filter(cart=cart)
        if not cart_items:
            return rest_response(
                {"error": "Basket is empty"}, status=status.HTTP_400_BAD_REQUEST,
            )

        # Створення нового користувача або пошук в базі
        if not data:
            first_name = "Test"
            last_name = "TestTest"
            phone = "111111111"
            email = "test@test.test"
            city = "Kyiv"
        else:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            phone = data.get("phone_number")
            email = data.get("email")
            city = data.get("city")

        if 0 == len(first_name) * len(last_name) * len(phone) * len(email) * len(city):
            return rest_response(
                {"error": "some fields is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except:
            user = User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email)

        # Створення адреси або пошук в базі
        address = Address.objects.create(city=city)

        address.address = data.get("address")
        address.np_department = data.get("department_NP")
        address.up_department = data.get("department_UP")
        address.save()
        user_address = UserAddress.objects.create(user=user, address=address)

        # Створення замовлення
        order = Order.objects.create(
            user=user,
            address=address,
            delivery_method=data.get("delivery_method"),
            payment_method=data.get("payment_method"),
        )
        # print(order.address)

        # Копіювання товарів з кошика до замовлення
        for item in cart_items:
            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        # Видалення кошика
        cart.delete()

        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        serializer_user = OrderUserSerializer(user)
        serializer_address = OrderAddressSerializer(address)
        delivery_price = UKR_POSHTA_DELIVERY
        if order.delivery_method == "Nova_Poshta":
            delivery_price = NOVA_POSHTA_DELIVERY
        elif order.delivery_method == "Courier":
            delivery_price = COURIER

        # Створення відповіді
        response_data = {
            "message": "Anonymous",
            "session_key": session.session_key,
            "order_id": order.id,
            "time_create": order.time_create,
            "payment_method": order.payment_method,
            "delivery_method": order.delivery_method,
            "delivery_price": delivery_price,
            "user": serializer_user.data,
            "address": serializer_address.data,
            "order_items": serializer.data,
            "total_items": sum(item.quantity for item in order_items),
            "total_price": sum(
                item.quantity * item.product.price for item in order_items
            )
                           + delivery_price,
        }

        return rest_response(response_data, status=status.HTTP_201_CREATED)
