from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import  Response as rest_response
from rest_framework import status
from django.http import HttpResponse
from .models import Product, Cart, CartItem, CartAnonymous, CartAnonymousItem
from .serializers import CartItemSerializer, CartAnonymousItemSerializer
from products.services import *

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi


class CartView(APIView):
    """Операції з кошиком"""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Success", schema=CartItemSerializer(many=True)
            ),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        }
    )

    def get(self, request):
        """Отримання інформації про кошик"""

        # Отримання або створення кошика користувача
        user = request.user

        # Якщо незареєстрований користувач
        if type(user) is AnonymousUser:
            if not request.session.session_key:
                request.session.create()
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(
                session_id=session.session_key
            )

            cart_items = CartAnonymousItem.objects.filter(cart=cart)
            serializer = CartAnonymousItemSerializer(cart_items, many=True)
            response_data = {
                "message": "Anonymous",
                "session_key": session.session_key,
                "cart_items": serializer.data,
                "total_items": sum(item.quantity for item in cart_items),
                "total_price": sum(item.quantity*item.product.price for item in cart_items)
            }

            return rest_response(response_data, status=status.HTTP_200_OK)

        # Зареєстрований користувач
        else:
            session = request.session
            cart, created = Cart.objects.get_or_create(user=user)

            # Отримання всіх товарів у кошику
            cart_items = CartItem.objects.filter(cart=cart)

            # Серіалізація інформації про товари у кошику
            serializer = CartItemSerializer(cart_items, many=True)

            # Повернення відповіді з інформацією про товари у кошику
            response_data = {
                "session_key": request.session.session_key,
                "cart_items": serializer.data,
                "total_items": sum(item.quantity for item in cart_items),
                "total_price": sum(
                    item.quantity * item.product.price for item in cart_items
                ),
            }

            return rest_response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                description="Success"),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        }
    )

    def delete(self, request):
        """Очищення кошика"""

        user = request.user

        if type(user) is AnonymousUser:
            session = request.session

            try:
                cart = CartAnonymous.objects.get(session=session.session_key)
            except CartAnonymous.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                )
            cart.delete()

        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
            cart.delete()

        return rest_response(
            {"success": "Cart delete"}, status=status.HTTP_204_NO_CONTENT
        )

    pk = openapi.Parameter('pk', in_=openapi.IN_QUERY, 
                           type= openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="specify the product number as 'pk' to be deleted",
        manual_parameters=[pk],
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     # properties={"product_id": openapi.Schema(type=openapi.TYPE_INTEGER)},
        #     # required=["product_id"],
        # ),
        responses={
            200: openapi.Response(description="Success"),
            204: openapi.Response(description="No Content"),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def patch(self, request):
        """Видалення товару з кошика"""

        pk = request.query_params.get("pk")

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return rest_response(
                {"error": "Product not found"}, status.HTTP_404_NOT_FOUND
            )

        # Отримання кошика користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:
            session = request.session
            try:
                cart = CartAnonymous.objects.get(session=session.session_key)
            except CartAnonymous.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                )
            try:
                cart_item = CartAnonymousItem.objects.get(cart=cart, product=product)
                cart_item.delete()
            except CartAnonymousItem.DoesNotExist:
                return rest_response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return rest_response(
                    {"success": "Product '"+ str(product.name) +"' removed from cart"},
                    status=status.HTTP_204_NO_CONTENT,
                )

        # для зареєстрованого користувача
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return rest_response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Видалення товару з кошика
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
            except CartItem.DoesNotExist:
                return rest_response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return rest_response(
                {"success": "Product '" + str(product.name) + "' removed from cart"},
                status=status.HTTP_204_NO_CONTENT,
            )

    quantity = openapi.Parameter(
        "quantity", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(
        operation_description="specify the product number as 'pk' and quantity to be added",
        manual_parameters=[pk, quantity],
        responses={
            201: openapi.Response(
                description="Create", schema=CartItemSerializer(many=True)
            ),
            204: openapi.Response(description="Product removed from cart"),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def post(self, request):  # , pk, quantity):
        """Додавання товару до кошика"""

        # Отримання інформації про товар
        pk = request.query_params.get("pk")
        quantity = request.query_params.get("quantity")
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return rest_response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            quantity = int(quantity)
        except:
            return rest_response(
                {
                    "error": "'quantity' must be integer",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Отримання або створення кошика користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(
                session=session.session_key
            )
            cart_item, created = CartAnonymousItem.objects.get_or_create(
                cart=cart, product=product
            )

            # видалення товару з кошика, якщо кількість = 0
            if not quantity:

                self.patch(request)
                return rest_response(
                    {"success": "Product '"+ str(product.name) +"' removed from cart"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            # додавання товару до кошика, якщо кількість != 0
            else:
                cart_item.quantity = quantity
                cart_item.save()

                # Отримання всіх товарів у кошику та серіалізація їх у відповідь
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

        # для зареєстрованого користувача
        else:
            cart, created = Cart.objects.get_or_create(user=user)
            session = request.session

            # Отримання або створення елемента кошика для вказаного товару
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            # видалення товару з кошика, якщо кількість = 0
            if not quantity:

                self.patch(request)
                return rest_response(
                    {"success": "Product removed from cart"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            # додавання товару до кошика, якщо кількість != 0
            else:
                cart_item.quantity = quantity
                cart_item.save()

                # Отримання всіх товарів у кошику та серіалізація їх у відповідь
                cart_items = CartItem.objects.filter(cart=cart)
                serializer = CartItemSerializer(cart_items, many=True)
                response_data = {
                    "session_key": session.session_key,
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                    "total_price": sum(
                        item.quantity * item.product.price for item in cart_items
                    ),
                }

                return rest_response(response_data, status=status.HTTP_201_CREATED)
