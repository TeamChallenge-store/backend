from .models import Product
from celery import shared_task


@shared_task
def count_products():
    return Product.objects.count()