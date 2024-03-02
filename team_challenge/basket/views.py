from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import  Response as responce
from rest_framework import status
from .models import Product, Cart, CartItem, CartAnonymous, CartAnonymousItem
from .serializers import CartItemSerializer, CartAnonymousItemSerializer
from products.services import *

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi

class CartView(APIView):
    """Операції з корзиною"""
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            },
            required=['product_id']
        ),
        responses={
            200: openapi.Response(description='Success'),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found')
        }
    )

    def patch(self, request):
        """Видалення товару з корзини"""
        product_id = request.data.get("product_id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status.HTTP_404_NOT_FOUND
            )

        # Отримання корзини користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:
            session = request.session
            try:
                cart = CartAnonymous.objects.get(session=session.session_key)
            except CartAnonymous.DoesNotExist:
                return Response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                )
            try:
                cart_item = CartAnonymousItem.objects.get(cart=cart, product=product)
                cart_item.delete()
            except CartAnonymousItem.DoesNotExist:
                return Response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"success": "Product removed from cart"},
                status=status.HTTP_204_NO_CONTENT,
            )

        # для зареєстрованого користувача
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Видалення товару з корзини
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
            except CartItem.DoesNotExist:
                return Response(
                    {"error": "Product not found in cart"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {"success": "Product removed from cart"},
                status=status.HTTP_204_NO_CONTENT,
            )
    


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: openapi.Response(description='Success'),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found')
        }
    )

    def post(self, request):
        """Додавання товару до кошика"""

        # Отримання інформації про товар з запиту
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Отримання або створення кошика користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(session=session.session_key)
            cart_item, created = CartAnonymousItem.objects.get_or_create(
                cart=cart, product=product
            )

            quantity = int(quantity)

            # видалення товару з кошика, якщо кількість = 0
            if not quantity:

                self.patch(request)

                cart_items = CartAnonymousItem.objects.filter(cart=cart)
                serializer = CartAnonymousItemSerializer(cart_items, many=True)
                response_data = {
                    "session_key": session.session_key,
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                }

                return Response(response_data, status=status.HTTP_201_CREATED) # status???

            # додавання товару до кошика, якщо кількість != 0
            else:
                cart_item.quantity = quantity
                cart_item.save()

                # Отримання всіх товарів у корзині та серіалізація їх у відповідь
                cart_items = CartAnonymousItem.objects.filter(cart=cart)
                serializer = CartAnonymousItemSerializer(cart_items, many=True)
                response_data = {
                    "session_key": session.session_key,
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

        # для зареєстрованого користувача
        else:
            cart, created = Cart.objects.get_or_create(user=user)

            # Отримання або створення елемента корзини для вказаного товару
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            quantity = int(quantity)
            # видалення товару з кошика, якщо кількість = 0
            if not quantity:
                self.patch(request)

                cart_items = CartItem.objects.filter(cart=cart)
                serializer = CartItemSerializer(cart_items, many=True)
                response_data = {
                    "session_key": session.session_key,
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                }

                return Response(response_data, status=status.HTTP_201_CREATED) # status???

            # додавання товару до кошика, якщо кількість != 0
            else:
                cart_item.quantity = quantity
                cart_item.save()

                # Отримання всіх товарів у корзині та серіалізація їх у відповідь
                cart_items = CartItem.objects.filter(cart=cart)
                serializer = CartItemSerializer(cart_items, many=True)
                response_data = {
                    "session_key": session.session_key,
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=CartItemSerializer(many=True)),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found')
        }
    )

    def get(self, request):
        """Отримання інформації про корзину"""

        # Отримання або створення корзини користувача
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
            }

            return responce(response_data, status.HTTP_200_OK)

        # Зареєстрований користувач
        else:
            session = request.session
            cart, created = Cart.objects.get_or_create(user=user)

            # Отримання всіх товарів у корзині
            cart_items = CartItem.objects.filter(cart=cart)

            # Серіалізація інформації про товари у корзині
            serializer = CartItemSerializer(cart_items, many=True)

            # Повернення відповіді з інформацією про товари у корзині
            response_data = {
                "session_key": request.session.session_key,
                "cart_items": serializer.data,
                "total_items": sum(item.quantity for item in cart_items),
            }

            return responce(response_data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            },
            required=['product_id']
        ),
        responses={
            200: openapi.Response(description='Success'),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found')
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
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
            cart.delete()

        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
            cart.delete()

        return Response({'success': 'Cart delete'}, status=status.HTTP_204_NO_CONTENT)

