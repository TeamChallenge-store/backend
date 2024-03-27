from django.db import models

# Create your models here.

from django.contrib.sessions.models import Session
from products.models import Product


SHIP_METHODS = [('NP', 'Nova Poshta'), ('UP', 'Ukr Poshta'), ('CR', 'Courier')]
ORDER_STATUS = [("IN", "In the works"), ("SN", "Sent"), ("RC", "Received"), ("CL", "Closed")]

class User(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    adress = models.CharField(max_length=64)


class Order(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through="OrderItem")
    time_create = models.DateTimeField(auto_now_add=True)
    ship_method = models.CharField(max_length=2, choices=SHIP_METHODS, default="UP")
    payment = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default="IN")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
