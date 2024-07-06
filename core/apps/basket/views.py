from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response as rest_response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import (
    Cart,
    CartAnonymous,
    CartAnonymousItem,
    CartItem,
    Product,
)
from .serializers import (
    CartAnonymousItemSerializer,
    CartItemSerializer,
)

from .tasks import (
    delete_user_cart,
    remove_cart_item,
)

from .services import show_cart


class CartView(APIView):
    """Операції з кошиком."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Success", 
                schema=CartAnonymousItemSerializer(many=True),
            ),
        },
    )
    def get(self, request):
        """Отримання інформації про кошик."""

        # Отримання або створення кошика користувача
        user = request.user

        # Якщо незареєстрований користувач
        # if type(user) is AnonymousUser:
        if not request.user.is_authenticated:
            if not request.session.session_key:
                request.session.create()
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(
                session_id=session.session_key,
            )
            cart_items = CartAnonymousItem.objects.filter(cart=cart)
            serializer = CartAnonymousItemSerializer(cart_items, many=True)

            response_data = {"message": "Anonymous"}

        # Зареєстрований користувач
        else:
            # Отримання всіх товарів у кошику
            cart, created = Cart.objects.get_or_create(user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            # Серіалізація інформації про товари у кошику
            serializer = CartItemSerializer(cart_items, many=True)

            # Повернення відповіді з інформацією про товари у кошику
            response_data = {"message": user.first_name}

        # Повернення відповіді з інформацією про товари у кошику
        response_data = show_cart(request, serializer, response_data, cart_items)

        return rest_response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                description="Delete Success",
            ),
            404: openapi.Response(description="Not Found"),
        },
    )
    def delete(self, request):
        """Очищення кошика."""

        user = request.user

        # Якщо незареєстрований користувач
        if type(user) is AnonymousUser:
            session = request.session
            try:
                cart = CartAnonymous.objects.get(session_id=session.session_key)
            except CartAnonymous.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND,
                )
        # Зареєстрований користувач
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND,
                )

        delete_user_cart.delay(cart.id)
        return rest_response({"success": "Cart delete"}, status=status.HTTP_200_OK)

    pk = openapi.Parameter(
        'pk', in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        operation_description="specify the product number as 'pk' to be deleted",
        manual_parameters=[pk],
        responses={
            200: openapi.Response(
                description="Success", schema=CartItemSerializer(many=True),
            ),
            204: openapi.Response(description="No Content"),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def patch(self, request):
        """Видалення товару з кошика."""

        pk = request.query_params.get("pk")
        if not pk:
            return rest_response(
                {"error": "missing parameter 'pk'"}, status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return rest_response(
                {"error": "Product not found"}, status.HTTP_404_NOT_FOUND,
            )

        # Отримання кошика користувача
        user = request.user

        # Якщо незареєстрований користувач
        if type(user) is AnonymousUser:
            session = request.session
            try:
                cart = CartAnonymous.objects.get(session_id=session.session_key)
            except CartAnonymous.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND,
                )
            cart_items = CartAnonymousItem.objects.filter(cart=cart)
            serializer = CartAnonymousItemSerializer(cart_items, many=True)
            response_data = {"message": "Anonymous"}
            try:
                cart_item = cart_items.get(product=product)
            except CartAnonymousItem.DoesNotExist:
                return rest_response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # для зареєстрованого користувача
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND,
                )

            # Видалення товару з кошика
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(cart_items, many=True)
            response_data = {"message": user.first_name}
            try:
                # cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item = cart_items.get(product=product)

            except CartItem.DoesNotExist:
                return rest_response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        remove_cart_item.delay(cart.id, product.id)

        response_data.update(
            {"success": "Product '" + str(product.name) + "' removed from cart"},
        )

        response_data = show_cart(request, serializer, response_data, cart_items)
        return rest_response(
            response_data,
            status=status.HTTP_200_OK,
        )

    quantity = openapi.Parameter(
        "quantity", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        operation_description="Specify the product number as 'pk' and quantity to be added.\
        If quantity = 0 product removed from basket",
        manual_parameters=[pk, quantity],
        responses={
            201: openapi.Response(
                description="Create", schema=CartItemSerializer(many=True),
            ),
            200: openapi.Response(
                description="Product removed from cart",
                schema=CartItemSerializer(many=True),
            ),
            202: openapi.Response(
                description="Product added to cart",
                schema=CartItemSerializer(many=True),
            ),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def post(self, request):  # , pk, quantity
        """Додавання товару до кошика."""

        # Отримання інформації про товар
        pk = request.query_params.get("pk")
        if not pk:
            return rest_response(
                {"error": "missing parameter 'pk'"}, status=status.HTTP_400_BAD_REQUEST,
            )
        quantity = request.query_params.get("quantity")
        if not quantity:
            return rest_response(
                {"error": "missing parameter 'quantity'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return rest_response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND,
            )

        # Отримання або створення кошика користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:

            if not request.session.session_key:
                request.session.create()
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(
                session_id=session.session_key,
            )
            cart_item, created = CartAnonymousItem.objects.get_or_create(
                cart=cart, product=product,
            )
            response_data = {"message": "Anonymous"}

        # для зареєстрованого користувача
        else:
            cart, created = Cart.objects.get_or_create(user=user)

            # Отримання або створення елемента кошика для вказаного товару
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
            )
            response_data = {"message": user.first_name}

        # видалення товару з кошика, якщо кількість = 0
        if int(quantity) == 0:

            cart_item.delete()
            response_data.update({
                "success": "Product '"
                           + str(product.name)
                           + "' removed from cart",
            })

        # додавання товару до кошика, якщо кількість != 0
        else:
            cart_item.quantity = quantity
            cart_item.save()

        # Отримання всіх товарів у кошику та серіалізація їх у відповідь
        session = request.session
        if type(user) is AnonymousUser:
            cart_items = CartAnonymousItem.objects.filter(cart=cart)
            serializer = CartAnonymousItemSerializer(cart_items, many=True)

        else:
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(cart_items, many=True)

        response_data = show_cart(request, serializer, response_data, cart_items)
        if created:
            status1 = status.HTTP_201_CREATED
        else:
            if int(quantity) == 0:
                status1 = status.HTTP_200_OK
            else:
                status1 = status.HTTP_202_ACCEPTED  # SUCCESS_ADDED_PRODUCT
        return rest_response(
            response_data,
            status=status1,
        )
