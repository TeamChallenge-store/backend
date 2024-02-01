from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, upload_to='product_images/')
    description = models.TextField()
    brand = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField()

    def __str__(self):
        return self.name
    
