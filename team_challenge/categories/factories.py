import factory
from django.utils.text import slugify
from .models import Category, Subcategory
from products.models import Product, Brand, Color
from django.utils import timezone


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Category 1'
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    image = 'path/to/test/image.jpg'


class SubcategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subcategory

    name = 'Subcategory 1'
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    parent_category_id = factory.SubFactory(CategoryFactory)
    image = 'path/to/test/subcategory_image.jpg'


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = 'Brand 1'
    description = 'Test description for Brand 1'


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Color

    name = 'Color 1'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = 'Product 1'
    category = factory.SubFactory(CategoryFactory)
    subcategory = factory.SubFactory(SubcategoryFactory)
    price = 100.00
    old_price = 120.00
    image = 'path/to/test/product_image.jpg'
    description = 'Test description for Product 1'
    brand = factory.SubFactory(BrandFactory)
    quantity_in_stock = 10
    rate = 5
    color = factory.SubFactory(ColorFactory)
    date = factory.LazyFunction(timezone.now)
    subtitle = 'Test subtitle for Product 1'
    subscription = 'Test subscription for Product 1'
    features = 'Test features for Product 1'
