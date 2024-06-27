from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.apps.categories.factories import (
    BrandFactory,
    CategoryFactory,
    ColorFactory,
    ProductFactory,
    SubcategoryFactory,
)


class CategoryListTests(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.subcategory = SubcategoryFactory(parent_category_id=self.category)
        self.brand = BrandFactory()
        self.color = ColorFactory()
        self.product = ProductFactory(
            category=self.category,
            subcategory=self.subcategory,
            brand=self.brand,
            color=self.color,
        )

    def test_get(self):
        self.url = reverse('category-list')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
