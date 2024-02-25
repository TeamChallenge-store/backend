from django.db import models
from categories.models import Category


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    # category = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    brand = models.ForeignKey(Brand, blank=True, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.name
