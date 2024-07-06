from celery import shared_task
from .models import Cart
from ..products.models import Product
from .models import CartItem


@shared_task
def delete_user_cart(cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        return {'success': 'Cart deleted'}
    except Cart.DoesNotExist:
        return {'success': 'Cart does not exist'}


@shared_task
def remove_cart_item(cart_id, product_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        product = Product.objects.get(id=product_id)

        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return {'success': 'CartItem deleted'}
    except (Cart.DoesNotExist, Product.DoesNotExist, CartItem.DoesNotExist) as e:
        return {'error': str(e)}
