from django.db import models
from django.contrib.sessions.models import Session
from products.models import Product
import team_challenge.settings


class Cart(models.Model):
    user = models.OneToOneField(team_challenge.settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                blank=True)
    products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class CartAnonymous(models.Model):
    session = models.OneToOneField(
        Session, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    products = models.ManyToManyField(Product, through="CartAnonymousItem")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


class CartAnonymousItem(models.Model):
    cart = models.ForeignKey(CartAnonymous, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
