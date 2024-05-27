from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.views import status

from categories.factories import CategoryFactory, SubcategoryFactory
from categories.views import CategoryList, CategoryDetail, SubcategoryDetail


class CategoryAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = CategoryFactory()

    def test_category_list(self):
        request = self.factory.get('/api/v1/product-categories/')
        view = CategoryList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        request = self.factory.get(f'/api/v1/product-categories/{self.category.slug}/')
        view = CategoryDetail.as_view()
        response = view(request, category_slug=self.category.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subcategory_detail(self):
        subcategory = SubcategoryFactory(parent_category_id=self.category)
        request = self.factory.get(f'/api/v1/product-categories/{self.category.slug}/{subcategory.slug}/')
        view = SubcategoryDetail.as_view()
        response = view(request, category_slug=self.category.slug, subcategory_slug=subcategory.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
