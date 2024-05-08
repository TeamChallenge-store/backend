from django.db import models

# Create your models here.

from django.contrib.sessions.models import Session
from products.models import Product

DELIVERY_METHODS = [('Nova Poshta', 1), ('Ukr Poshta', 2), ('Courier', 3)]
ORDER_STATUS = [("IN", "In the works"), ("SN", "Sent"), ("RC", "Received"), ("CL", "Closed")]
PAYMENT_METHOD = [
    ("card online", 1),
    ("Google Pay", 2),
    ("Apple Pay", 3),
    ("upon receipt", 4),
]
CITY = [
    ("Simferopol", 1),
    ("Vinnytsia", 2),
    ("Lutsk", 3),
    ("Dnipro", 4),
    ("Donetsk", 5),
    ("Zhytomyr", 6),
    ("Uzhhorod", 7),
    ("Zaporizhzhia", 8),
    ("Ivano-Frankivsk", 9),
    ("Kyiv", 10),
    ("Kropyvnytskyi", 11),
    ("Luhansk", 12),
    ("Lviv", 13),
    ("Mykolaiv", 14),
    ("Odesa", 15),
    ("Poltava", 16),
    ("Rivne", 17),
    ("Sumy", 18),
    ("Ternopil", 19),
    ("Kharkiv", 20),
    ("Khmelnytskyi", 21),
    ("Cherkasy", 22),
    ("Chernivtsі", 23),
    ("Chernihiv", 24),
    ("Sevastopol", 25)
]

class Address(models.Model):
    city = models.CharField(max_length=15, choices=CITY, default="Kyiv")
    address = models.CharField(max_length=64, null=True, blank=True)
    np_department = models.CharField(max_length=64, null=True, blank=True)
    up_department = models.CharField(max_length=64, null=True, blank=True)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.ManyToManyField(Address, through="UserAddress")

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through="OrderItem")
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    time_create = models.DateTimeField(auto_now_add=True)    
    delivery_method = models.CharField(
        max_length=11, choices=DELIVERY_METHODS, default="Ukr Poshta"
    )
    payment_method = models.CharField(
        max_length=12, choices=PAYMENT_METHOD, default="upon receipt"
    )
    payment = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default="IN")

    # def __str__(self):
    #     return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
