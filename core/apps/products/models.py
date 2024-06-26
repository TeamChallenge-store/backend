from django.db import models
from core.apps.categories.models import Category, Subcategory
from django.utils import timezone


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, upload_to='images/')
    description = models.CharField(max_length=255, blank=True)
    brand = models.ForeignKey(Brand, blank=True, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()
    rate = models.IntegerField(default=0)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, auto_now_add=False)
    subtitle = models.CharField(max_length=255)
    subscription = models.CharField(max_length=255)
    features = models.CharField(max_length=255)

    def __str__(self):
        return self.name
