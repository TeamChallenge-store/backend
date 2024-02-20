from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Cart, CartItem
from .serializers import CartItemSerializer
from products.services import *

class CartView(APIView):
    """Операції з корзиною"""
  
    def post(self, request):
        """Додавання товару до корзини"""

        # Отримання інформації про товар з запиту
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Отримання або створення корзини користувача
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        # Отримання або створення елемента корзини для вказаного товару
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        # Отримання всіх товарів у корзині та серіалізація їх у відповідь
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response({'cart_items': serializer.data, 'total_items': cart_items.count()}, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        """Видалення товару з корзини"""

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Отримання корзини користувача
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Видалення товару з корзини
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': 'Product removed from cart'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        """Отримання інформації про корзину"""

        # Отримання або створення корзини користувача
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        # Отримання всіх товарів у корзині
        cart_items = CartItem.objects.filter(cart=cart)

        # Серіалізація інформації про товари у корзині
        serializer = CartItemSerializer(cart_items, many=True)

        # Повернення відповіді з інформацією про товари у корзині
        response_data = {
            'cart_items': serializer.data,
            'total_items': sum(item.quantity for item in cart_items)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
