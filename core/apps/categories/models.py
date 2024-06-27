from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    id = models.AutoField(primary_key=True) #noqa
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', default='default title')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True) #noqa
    slug = models.SlugField(unique=True, blank=True)
    parent_category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory_images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
