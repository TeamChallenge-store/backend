from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.models import Session
from .models import Product, Cart, CartItem, CartAnonymous, CartAnonymousItem
from .serializers import (
    ProductDetailSerializer,
    CartItemSerializer,
    CartAnonymousItemSerializer,
)
from .services import *


class ProductListViewPriceUp(generics.ListAPIView):
    """Вивід списку продуктів за зростанням ціни"""

    def get(self, request):
        category = request.query_params.get("category", None)

        sorted_products = sort_price_up(category)

        return paginate_product_list(sorted_products, request)


class ProductListViewPriceDown(APIView):
    """Вивід списку продуктів за спаданням ціни"""

    def get(self, request):
        category = request.query_params.get("category", None)

        sorted_products = sort_price_down(category)

        return paginate_product_list(sorted_products, request)


class ProductListViewRate(APIView):
    """Вивід списку продуктів за рейтингом"""

    def get(self, request):

        category = request.query_params.get("category", None)
        make_rate()
        sorted_products = sort_rate(category)

        return paginate_product_list(sorted_products, request)


class ProductListView(APIView):
    """ "Вивід списку продуктів"""

    def get(self, request):
        min_price = request.query_params.get("min_price", None)
        max_price = request.query_params.get("max_price", None)

        filtered_products = filter_price_products(min_price, max_price)

        return paginate_product_list(filtered_products, request)


class ProductDetailView(APIView):
    """ "Вивід детального списку продуктів"""

    def get(self, request, id):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class CartView(APIView):
    """Операції з корзиною"""

    def post(self, request):
        """Додавання товару до корзини"""

        # Отримання інформації про товар з запиту
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Отримання або створення корзини користувача
        user = request.user

        # для анонімного користавача
        if type(user) is AnonymousUser:
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(session=session.session_key)
            cart_item, created = CartAnonymousItem.objects.get_or_create(
                cart=cart, product=product
            )
            cart_item.quantity = int(quantity)
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
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            cart_item.quantity = int(quantity)
            cart_item.save()

            # Отримання всіх товарів у корзині та серіалізація їх у відповідь
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(cart_items, many=True)

            return Response(
                {
                    "cart_items": serializer.data,
                    "total_items": sum(item.quantity for item in cart_items),
                },
                status=status.HTTP_201_CREATED,
            )


    def patch(self, request):
        """Видалення товару з корзини"""
        product_id = request.data.get("product_id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
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
                cart_item = CartAnonymousItem.objects.get(
                    cart=cart, product=product
                )
                cart_item.delete()
            except CartAnonymousItem.DoesNotExist:
                return Response(
                    {"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND
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
                    {"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"success": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT
            )
        

    def get(self, request):
        """Отримання інформації про корзину"""

        # Отримання або створення корзини користувача
        user = request.user

        # Якщо незареєстрований користувач
        if type(user) is AnonymousUser:
            if not request.session.session_key:
                request.session.create()
                print("create")
            session = request.session

            cart, created = CartAnonymous.objects.get_or_create(
                session_id=session.session_key
            )
            print('***', cart)
            # if created:
            #     print('Create cart anonymous')
            # UserSession.objects.get_or_create(
            #     user=user, session_id=request.session.session_key
            # )
            cart_items = CartAnonymousItem.objects.filter(cart=cart)
            serializer = CartAnonymousItemSerializer(cart_items, many=True)
            response_data = {
                "message": 'Anonymous',
                "session_key": session.session_key,
                "cart_items": serializer.data,
                "total_items": sum(item.quantity for item in cart_items),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        # Зареєстрований користувач
        else:
            session = request.session
            cart, created = Cart.objects.get_or_create(user=user)  # session_id=session.session_key,
            if created:
                print('Create cart user')
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

            return Response(response_data, status=status.HTTP_200_OK)
