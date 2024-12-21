from django.db import models

from core.apps.products.models import Product


class Address(models.Model):
    city = models.CharField(max_length=25, default="Kyiv")
    address = models.JSONField(max_length=64, null=True, blank=True)
    # street_name = models.CharField(max_length=64, null=True, blank=True)
    # house_number = models.CharField(max_length=64, null=True, blank=True)
    # section_number = models.CharField(max_length=64, null=True, blank=True)
    # apartment_number = models.CharField(max_length=64, null=True, blank=True)
    np_department = models.CharField(max_length=64, null=True, blank=True)
    up_department = models.CharField(max_length=64, null=True, blank=True)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.ManyToManyField(Address, through="UserAddress")

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Order(models.Model):
    DELIVERY_METHODS = [('Nova_Poshta', 1), ('Ukr_Poshta', 2), ('Courier', 3)]
    ORDER_STATUS = [("IN", "In_the_works"), ("SN", "Sent"), ("RC", "Received"), ("CL", "Closed")]
    PAYMENT_METHOD = [
        ("card_online", 1),
        ("Google_Pay", 2),
        ("Apple_Pay", 3),
        ("upon_receipt", 4),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #, null=True, blank=True)
    products = models.ManyToManyField(Product, through="OrderItem")
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True,
    )
    time_create = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(
        max_length=11, choices=DELIVERY_METHODS, default="Ukr_Poshta",
    )
    payment_method = models.CharField(
        max_length=12, choices=PAYMENT_METHOD, default="upon_receipt",
    )
    payment = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default="IN")

    # def __str__(self):
    #     return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
