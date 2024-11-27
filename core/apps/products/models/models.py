from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from core.apps.categories.models import (
    Category,
    Subcategory,
)
from core.apps.common.models import TimedBaseModel


class Brand(TimedBaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Бренд'


class Color(TimedBaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Колір'


class Product(TimedBaseModel):
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
    subtitle = models.CharField(max_length=255)
    subscription = models.CharField(max_length=255)
    features = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True, verbose_name='Відображення продукту в каталозі')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = 'Продукти'


class Comment(TimedBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = 'Коментарі'
